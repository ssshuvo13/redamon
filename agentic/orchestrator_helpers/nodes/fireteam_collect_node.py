"""Fireteam collect node.

Runs after fireteam_deploy_node completes. Merges member results back into
parent AgentState: target_info deltas, chain_findings_memory appends, and a
human-readable summary message injected into parent's conversation.

Findings are NOT extracted here — members write ChainFinding rows inline
to Neo4j during their own think nodes with proper agent attribution. This
node rolls them up into the parent's chain_findings_memory so the next root
think sees them in its conversation context.

If any member escalated a dangerous tool, surface the first one as a
regular tool_confirmation so the existing approval flow pauses the parent.
"""

import logging
from typing import Iterable, Optional

from langchain_core.messages import SystemMessage

from state import AgentState

logger = logging.getLogger(__name__)


def _merge_target_info(base: dict, delta: dict) -> None:
    """In-place merge of delta into base; list fields are de-duped extended."""
    for k, v in (delta or {}).items():
        if isinstance(v, list):
            existing = base.get(k) or []
            merged = list(existing)
            for item in v:
                if item not in merged:
                    merged.append(item)
            base[k] = merged
        elif isinstance(v, dict):
            existing = base.get(k) or {}
            if isinstance(existing, dict):
                merged = dict(existing)
                merged.update(v)
                base[k] = merged
            else:
                base[k] = v
        else:
            # Scalars: take delta's value only if base's is empty/None.
            if not base.get(k):
                base[k] = v


def _render_summary(fireteam_id: str, results: list, wall_s: float | None = None) -> str:
    lines = [f"[Fireteam {fireteam_id} completed]"]
    if wall_s is not None:
        lines[0] = f"[Fireteam {fireteam_id} completed in {wall_s:.1f}s]"
    for r in results:
        status = r.get("status", "unknown")
        name = r.get("name", "(unnamed)")
        iters = r.get("iterations_used", 0)
        tokens = r.get("tokens_used", 0)
        findings = r.get("findings") or []
        lines.append("")
        lines.append(f"Member: {name} ({r.get('member_id')})")
        lines.append(f"  Status: {status} ({iters} iterations, {tokens} tokens)")
        if r.get("completion_reason") and status != "success":
            lines.append(f"  Reason: {r['completion_reason']}")
        if r.get("error_message"):
            lines.append(f"  Error: {r['error_message']}")
        if findings:
            lines.append(f"  Findings: {len(findings)}")
            for f in findings[:6]:
                sev = f.get("severity", "info")
                title = f.get("title", "(untitled)")
                lines.append(f"    - [{sev}] {title}")
        else:
            lines.append(f"  Findings: 0")
    return "\n".join(lines)


async def fireteam_collect_node(
    state: AgentState,
    config,
    *,
    llm=None,
    neo4j_creds=None,
    streaming_callbacks=None,
) -> dict:
    """Merge fireteam member results into parent state and extract findings."""
    results: list = state.get("_current_fireteam_results") or []
    fireteam_id = state.get("_fireteam_id") or "unknown"
    user_id = state.get("user_id") or ""
    project_id = state.get("project_id") or ""
    session_id = state.get("session_id") or ""
    phase = state.get("current_phase", "informational")

    # ---- Observability: collect header ----
    logger.info(f"\n{'=' * 80}")
    logger.info(
        "[%s] FIRETEAM COLLECT wave=%s members=%d",
        session_id, fireteam_id, len(results),
    )
    for r in results:
        logger.info(
            "[%s]   member=%s (%s) status=%s iter=%s tokens=%s findings=%d delta_keys=%s",
            session_id, r.get("member_id"), r.get("name"), r.get("status"),
            r.get("iterations_used", 0), r.get("tokens_used", 0),
            len(r.get("findings") or []),
            list((r.get("target_info_delta") or {}).keys()),
        )
    logger.info(f"{'=' * 80}")

    merged_target_info = dict(state.get("target_info") or {})
    target_info_before_keys = set(merged_target_info.keys())
    for r in results:
        _merge_target_info(merged_target_info, r.get("target_info_delta") or {})
    new_target_keys = set(merged_target_info.keys()) - target_info_before_keys
    if new_target_keys:
        logger.info("[%s] target_info NEW keys merged: %s", session_id, sorted(new_target_keys))

    # Findings were written inline to Neo4j by each member's think node
    # (fireteam_member_think_node writes ChainFinding rows with agent_id,
    # source_agent, fireteam_id, anchored to the member's ChainStep in real
    # time). Collect just rolls them up into parent chain_findings_memory
    # and injects them into the summary — no second LLM pass here.
    chain_findings = list(state.get("chain_findings_memory") or [])
    findings_before = len(chain_findings)
    for r in results:
        source = r.get("name") or r.get("member_id") or "unknown"
        member_id = r.get("member_id") or "unknown"
        for f in r.get("findings") or []:
            chain_findings.append({
                **f,
                "source_agent": source,
                "agent_id": member_id,
                "fireteam_id": fireteam_id,
            })
    findings_added = len(chain_findings) - findings_before
    logger.info(
        "[%s] merged %d new findings into chain_findings_memory (total now %d)",
        session_id, findings_added, len(chain_findings),
    )

    summary = _render_summary(fireteam_id, results)

    # Collect every member that escalated. Per FIRETEAM.md §20 Q3, v1 surfaces
    # each one sequentially (not coalesced) so the operator decides each in
    # turn. We queue all of them now; the first drains into
    # tool_confirmation_pending below, the rest stay in _pending_escalations
    # and are drained either here (after a single-member redeploy completes)
    # or by process_fireteam_confirmation_node after a rejection.
    fresh_escalations: list[dict] = []
    for r in results:
        if r.get("status") != "needs_confirmation":
            continue
        pc = r.get("pending_confirmation") or {}
        if not pc:
            continue
        # Ensure agent_id is carried on the envelope so the UI can match the
        # confirmation back to the member panel.
        pc = dict(pc)
        pc.setdefault("agent_id", r.get("member_id"))
        pc.setdefault("agent_name", r.get("name"))
        fresh_escalations.append(pc)

    # Pre-existing queue from an earlier wave in the same escalation chain.
    queue: list[dict] = list(state.get("_pending_escalations") or [])
    queue.extend(fresh_escalations)

    update: dict = {
        "target_info": merged_target_info,
        "chain_findings_memory": chain_findings,
        "_current_fireteam_plan": None,
        "_current_fireteam_results": None,
        "messages": [SystemMessage(content=summary)],
    }

    if queue:
        pending = queue.pop(0)
        update["_pending_escalations"] = queue or None
        update["_escalated_fireteam_confirmation"] = pending
        update["_escalated_member_id"] = pending.get("agent_id")
        # Hand off to the existing tool confirmation machinery by setting the
        # same flags await_tool_confirmation uses.
        update["awaiting_tool_confirmation"] = True
        update["tool_confirmation_pending"] = pending
        update["_tool_confirmation_mode"] = "fireteam_escalation"
        logger.info(
            "[fireteam] escalation surfaced from member %s (%d more queued)",
            pending.get("agent_id"), len(queue),
        )
    else:
        update["_pending_escalations"] = None

    return update


