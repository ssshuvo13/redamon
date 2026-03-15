# RedAmon — Developer Guide

**Everything you need to understand, develop, and extend RedAmon.**

This guide is the single entry point for developers. It covers the technology stack, system architecture, project layout, how each subsystem works, and the exact commands you need to apply your changes. For deep dives into specific components, follow the links to the dedicated documentation pages listed in the [Documentation Index](#9-documentation-index) at the end.

> **Legal**: This tool is for authorized security testing only. See [DISCLAIMER.md](../DISCLAIMER.md).

---

## Table of Contents

1. [Technology Stack](#1-technology-stack)
2. [Architecture at a Glance](#2-architecture-at-a-glance)
3. [Project Filesystem Overview](#3-project-filesystem-overview)
4. [How the System Works](#4-how-the-system-works)
   - [Agent System (agentic/)](#41-agent-system-agentic)
   - [CypherFix Agents](#42-cypherfix-agents)
   - [Reconnaissance Pipeline (recon/)](#43-reconnaissance-pipeline-recon)
   - [Webapp (webapp/)](#44-webapp-webapp)
   - [Settings Architecture](#45-settings-architecture)
5. [Development Workflow](#5-development-workflow)
   - [Prerequisites](#51-prerequisites)
   - [First-Time Setup](#52-first-time-setup)
   - [Hot-Reload vs Rebuild](#53-hot-reload-vs-rebuild)
   - [Common Commands](#54-common-commands)
   - [Important Rules](#55-important-rules)
   - [AI-Assisted Coding](#56-ai-assisted-coding)
6. [Feature Development Checklists](#6-feature-development-checklists)
7. [Debugging & Testing](#7-debugging--testing)
8. [Environment Variables](#8-environment-variables)
9. [Documentation Index](#9-documentation-index)

---

## 1. Technology Stack

Every technology used in RedAmon, organized by layer. Each entry links to its **official documentation** so you can learn how it works.

> For detailed role descriptions of each technology within RedAmon, see [TECH_STACK.md](TECH_STACK.md).

### Frontend

| Technology | Role | Official Docs |
|-----------|------|---------------|
| **Next.js** (v16) | Full-stack React framework — SSR, API routes, webapp | [nextjs.org/docs](https://nextjs.org/docs) |
| **React** (v19) | Component-based UI library | [react.dev](https://react.dev) |
| **TypeScript** | Static typing across the frontend | [typescriptlang.org/docs](https://www.typescriptlang.org/docs) |
| **Prisma** | TypeScript ORM for PostgreSQL | [prisma.io/docs](https://www.prisma.io/docs) |
| **TanStack React Query** | Server state management and caching | [tanstack.com/query](https://tanstack.com/query/latest/docs/framework/react/overview) |
| **TanStack React Table** | Headless table UI primitives | [tanstack.com/table](https://tanstack.com/table/latest/docs/introduction) |
| **React Force Graph** (2D & 3D) | Interactive attack surface graph visualization | [github.com/vasturiano/react-force-graph](https://github.com/vasturiano/react-force-graph) |
| **Three.js** | 3D rendering engine behind 3D graph view | [threejs.org/docs](https://threejs.org/docs) |
| **D3 Force** | Force-directed graph layout algorithms | [d3js.org/d3-force](https://d3js.org/d3-force) |
| **Recharts** | Charting library for analytics dashboards | [recharts.org](https://recharts.org/en-US/api) |
| **Lucide React** | Icon system | [lucide.dev](https://lucide.dev/guide) |
| **React Markdown** | Markdown rendering in agent chat | [github.com/remarkjs/react-markdown](https://github.com/remarkjs/react-markdown) |
| **React Syntax Highlighter** | Code block highlighting | [github.com/react-syntax-highlighter](https://github.com/react-syntax-highlighter/react-syntax-highlighter) |

### AI & Agent

| Technology | Role | Official Docs |
|-----------|------|---------------|
| **LangChain** | LLM application framework — prompts, tool binding, chains | [python.langchain.com/docs](https://python.langchain.com/docs/introduction/) |
| **LangGraph** | State machine engine for the ReAct agent loop | [langchain-ai.github.io/langgraph](https://langchain-ai.github.io/langgraph/) |
| **LangChain MCP Adapters** | Bridges LangChain tools with MCP server endpoints | [github.com/langchain-ai/langchain-mcp-adapters](https://github.com/langchain-ai/langchain-mcp-adapters) |
| **MCP** (Model Context Protocol) | Standardized protocol for tool integration | [modelcontextprotocol.io](https://modelcontextprotocol.io) |
| **Tree-sitter** | AST parsing for CodeFix agent code navigation | [tree-sitter.github.io](https://tree-sitter.github.io/tree-sitter/) |
| **PyGithub** | GitHub API client for CodeFix PR creation | [pygithub.readthedocs.io](https://pygithub.readthedocs.io) |
| **Tavily** | AI-powered web search for CVE research | [docs.tavily.com](https://docs.tavily.com) |
| **LangChain AWS** | AWS Bedrock integration (`ChatBedrockConverse`) | [python.langchain.com/docs/integrations/providers/aws](https://python.langchain.com/docs/integrations/providers/aws/) |

### Backend

| Technology | Role | Official Docs |
|-----------|------|---------------|
| **Python** (3.11) | Core language for all backend services | [docs.python.org/3.11](https://docs.python.org/3.11/) |
| **FastAPI** | Async Python web framework (agent + recon orchestrator) | [fastapi.tiangolo.com](https://fastapi.tiangolo.com) |
| **Uvicorn** | ASGI server for FastAPI services | [uvicorn.org](https://www.uvicorn.org) |
| **Pydantic** | Data validation and settings management | [docs.pydantic.dev](https://docs.pydantic.dev) |
| **Docker SDK for Python** | Programmatic container lifecycle management | [docker-py.readthedocs.io](https://docker-py.readthedocs.io) |
| **HTTPX** | Async HTTP client for inter-service communication | [www.python-httpx.org](https://www.python-httpx.org) |

### Databases

| Technology | Role | Official Docs |
|-----------|------|---------------|
| **PostgreSQL** (v16) | Relational DB — users, projects, settings, conversations | [postgresql.org/docs/16](https://www.postgresql.org/docs/16/) |
| **Neo4j** (v5 Community) | Graph DB — attack surface knowledge graph | [neo4j.com/docs](https://neo4j.com/docs/) |
| **Neo4j APOC** | Advanced graph procedures and functions | [neo4j.com/labs/apoc](https://neo4j.com/labs/apoc/) |
| **Neo4j Python Driver** | Python client for Cypher queries | [neo4j.com/docs/python-manual](https://neo4j.com/docs/python-manual/current/) |
| **Redis** | In-memory cache within the GVM scanning stack | [redis.io/docs](https://redis.io/docs/) |

### Security & Penetration Testing Tools

| Tool | Category | Official Docs |
|------|----------|---------------|
| **Metasploit Framework** | Exploitation & post-exploitation | [docs.metasploit.com](https://docs.metasploit.com) |
| **Nmap** | Network scanning & service detection | [nmap.org/docs](https://nmap.org/docs.html) |
| **Nuclei** | Template-based vulnerability scanning | [docs.projectdiscovery.io/nuclei](https://docs.projectdiscovery.io/tools/nuclei/overview) |
| **Naabu** | Fast SYN/CONNECT port scanner | [docs.projectdiscovery.io/naabu](https://docs.projectdiscovery.io/tools/naabu/overview) |
| **Httpx** | HTTP/HTTPS probing & tech detection | [docs.projectdiscovery.io/httpx](https://docs.projectdiscovery.io/tools/httpx/overview) |
| **Katana** | Web crawler with JS rendering | [docs.projectdiscovery.io/katana](https://docs.projectdiscovery.io/tools/katana/overview) |
| **GAU** (GetAllUrls) | Passive URL discovery | [github.com/lc/gau](https://github.com/lc/gau) |
| **Kiterunner** | API endpoint brute-forcer | [github.com/assetnote/kiterunner](https://github.com/assetnote/kiterunner) |
| **GVM / OpenVAS** | Network vulnerability scanner (170k+ NVTs) | [greenbone.github.io/docs](https://greenbone.github.io/docs/) |
| **Hydra** | Brute-force credential testing | [github.com/vanhauser-thc/thc-hydra](https://github.com/vanhauser-thc/thc-hydra) |
| **SQLMap** | Automated SQL injection detection | [sqlmap.org](https://sqlmap.org) |
| **Interactsh** | Out-of-band vulnerability detection | [github.com/projectdiscovery/interactsh](https://github.com/projectdiscovery/interactsh) |
| **Knockpy** | Active subdomain brute-forcing | [github.com/guelfoweb/knock](https://github.com/guelfoweb/knock) |
| **Wappalyzer** | Technology fingerprinting (6000+ rules) | [github.com/chorsley/python-Wappalyzer](https://github.com/chorsley/python-Wappalyzer) |

### LLM Providers

Configured **per-user** in the webapp UI (`/settings`), not in `.env`.

| Provider | Official Docs |
|----------|---------------|
| **OpenAI** (GPT-5.2, GPT-5, GPT-4.1) | [platform.openai.com/docs](https://platform.openai.com/docs) |
| **Anthropic** (Claude Opus 4.6, Sonnet 4.5, Haiku 4.5) | [docs.anthropic.com](https://docs.anthropic.com) |
| **AWS Bedrock** (Claude, Titan, Llama, Cohere) | [docs.aws.amazon.com/bedrock](https://docs.aws.amazon.com/bedrock/) |
| **OpenRouter** (300+ models via single API key) | [openrouter.ai/docs](https://openrouter.ai/docs) |
| **Ollama** (local models) | [ollama.com](https://ollama.com) |
| **vLLM** (local models) | [docs.vllm.ai](https://docs.vllm.ai) |
| **LM Studio** (local models) | [lmstudio.ai](https://lmstudio.ai) |
| **OpenAI-Compatible** (any endpoint) | Supports any server implementing the OpenAI API format |

### Infrastructure

| Technology | Role | Official Docs |
|-----------|------|---------------|
| **Docker** | Container runtime — every component is containerized | [docs.docker.com](https://docs.docker.com) |
| **Docker Compose** (v2) | Multi-container orchestration (15+ containers) | [docs.docker.com/compose](https://docs.docker.com/compose/) |
| **Node.js** (v22) | JavaScript runtime for the Next.js webapp | [nodejs.org/docs](https://nodejs.org/docs/latest-v22.x/api/) |
| **Go** (1.22) | Build environment for ProjectDiscovery tools (compiled from source) | [go.dev/doc](https://go.dev/doc/) |

---

## 2. Architecture at a Glance

RedAmon is a fully Dockerized system with 15+ containers communicating over two internal networks.

### Service Topology

```
Browser ──→ Webapp (Next.js :3000) ──WebSocket──→ Agent (FastAPI :8080, exposed :8090)
                │                                       │
                │ REST+SSE                              │ MCP Protocol
                ▼                                       ▼
        Recon Orchestrator (:8010)              Kali Sandbox (MCP Servers)
                │                               ├── Network Recon (:8000)
                │ Docker SDK                    ├── Nuclei (:8002)
                ▼                               ├── Metasploit (:8003)
        Ephemeral Containers                    └── Nmap (:8004)
        ├── Recon Pipeline
        ├── GVM/OpenVAS Scanner
        └── GitHub Secret Hunter

                    ┌─────────────┐     ┌──────────────┐
                    │ PostgreSQL  │     │    Neo4j      │
                    │   :5432     │     │ :7474 / :7687 │
                    └──────┬──────┘     └──────┬───────┘
                           │                   │
            Used by: Webapp (Prisma)    Used by: Recon, Agent, Webapp
            Stores: users, projects,    Stores: attack surface graph
            settings, conversations,    (17 node types, 20+ relationships)
            remediations, reports
```

### Networks

| Network | Subnet | Purpose |
|---------|--------|---------|
| **`redamon`** | bridge (default) | All inter-service communication |
| **`pentest-net`** | 172.28.0.0/16 | Isolated scanning network — Kali sandbox, MCP tools, and target containers (guinea pigs) |

### Docker Compose Services

| Service | Container Name | Port | Role |
|---------|---------------|------|------|
| `webapp` | redamon-webapp | 3000 | Next.js frontend + backend API |
| `agent` | redamon-agent | 8090 (→8080 internal) | AI agent (LangGraph + FastAPI WebSocket) |
| `recon-orchestrator` | redamon-recon-orchestrator | 8010 | Spawns recon/GVM/GitHub containers via Docker SDK |
| `kali-sandbox` | redamon-kali | 8000, 8002–8004 | MCP tool servers (nmap, nuclei, metasploit, network-recon) |
| `postgres` | redamon-postgres | 5432 | PostgreSQL database |
| `neo4j` | redamon-neo4j | 7474, 7687 | Neo4j graph database |
| `gvmd` | redamon-gvm-gvmd | internal | GVM daemon (vulnerability scanner) |
| `gvm-ospd` | redamon-gvm-ospd | internal | OpenVAS scanner engine |
| `recon` | (profile: tools) | — | Recon pipeline image (spawned dynamically, not always running) |

> For full Mermaid diagrams, container architecture, and data flow pipelines, see [ARCHITECTURE.md](ARCHITECTURE.md).

---

## 3. Project Filesystem Overview

```
redamon/
├── agentic/                        # AI agent orchestrator (Python 3.11 / LangGraph / FastAPI)
│   ├── api.py                      #   FastAPI entry point, mounts WebSocket endpoints
│   ├── orchestrator.py             #   Main ReAct agent loop: think → select tool → observe → repeat
│   ├── state.py                    #   LangGraph AgentState (execution trace, todos, phases, messages)
│   ├── tools.py                    #   Tool managers: MCP, Neo4j (Cypher), WebSearch, Shodan, GoogleDork
│   ├── websocket_api.py            #   Session management, streaming events, approval flow
│   ├── project_settings.py         #   Fetches settings from webapp API, falls back to DEFAULT_AGENT_SETTINGS
│   ├── model_providers.py          #   Multi-provider LLM routing (OpenAI, Anthropic, Bedrock, OpenRouter, local)
│   ├── guardrail.py                #   Scope guardrail — prevents scanning unauthorized targets
│   ├── chat_persistence.py         #   Saves conversation history to PostgreSQL via webapp API
│   ├── report_summarizer.py        #   Generates pentest report summaries from agent sessions
│   ├── logging_config.py           #   Structured logging setup for the agent container
│   ├── utils.py                    #   Shared utility functions
│   ├── prompts/                    #   All LLM prompt templates
│   │   ├── base.py                 #     Core system prompt + tool availability tables
│   │   ├── classification.py       #     Attack path classification (CVE, brute force, phishing, etc.)
│   │   ├── tool_registry.py        #     Single source of truth for tool definitions
│   │   ├── cve_exploit_prompts.py  #     CVE research & exploitation guidance
│   │   ├── brute_force_credential_guess_prompts.py  # Credential attack strategy
│   │   ├── phishing_social_engineering_prompts.py   # Social engineering tactics
│   │   ├── post_exploitation.py    #     Post-exploitation phase guidance
│   │   ├── stealth_rules.py        #     Stealth mode constraints
│   │   └── unclassified_prompts.py #     Generic/unclassified attack prompts
│   ├── orchestrator_helpers/       #   Supporting modules for the orchestrator
│   │   ├── nodes/                  #     LangGraph node implementations
│   │   │   ├── initialize_node.py  #       Session + LLM + MCP initialization
│   │   │   ├── think_node.py       #       LLM reasoning step
│   │   │   ├── execute_tool_node.py #      Tool execution + result handling
│   │   │   ├── execute_plan_node.py #      Multi-step plan execution
│   │   │   ├── generate_response_node.py # Final response formatting
│   │   │   └── approval_nodes.py   #      Human-in-the-loop approval + question gates
│   │   ├── llm_setup.py            #     LLM initialization with project settings
│   │   ├── streaming.py            #     WebSocket event emission (status, thoughts, tool output)
│   │   ├── phase.py                #     Phase classification & transition logic
│   │   ├── chain_graph_writer.py   #     Neo4j attack chain recording (EvoGraph)
│   │   ├── parsing.py              #     LLM output parsing (JSON extraction)
│   │   ├── config.py               #     Orchestrator configuration constants
│   │   ├── json_utils.py           #     JSON serialization helpers
│   │   └── debug.py                #     Debug utilities
│   ├── cypherfix_triage/           #   Vulnerability triage agent
│   │   ├── orchestrator.py         #     Hybrid orchestrator: static Cypher + ReAct analysis
│   │   ├── state.py                #     TriageFinding, RemediationDraft, TriageState
│   │   ├── tools.py                #     Neo4j query manager + Tavily web search
│   │   ├── websocket_handler.py    #     WebSocket endpoint + streaming callback
│   │   ├── project_settings.py     #     CypherFix-specific settings loader
│   │   └── prompts/                #     Triage system prompt + 9 Cypher queries
│   └── cypherfix_codefix/          #   Automated code fix agent
│       ├── orchestrator.py         #     Pure ReAct while-loop (Claude Code pattern)
│       ├── state.py                #     DiffBlock, CodeFixSettings, CodeFixState
│       ├── websocket_handler.py    #     WebSocket endpoint + streaming callback
│       ├── project_settings.py     #     CodeFix settings loader
│       ├── prompts/                #     Dynamic system prompt + diff format instructions
│       └── tools/                  #     11 code-aware tools (read, edit, grep, glob, bash, symbols, etc.)
│
├── recon_orchestrator/             # Container lifecycle manager (Python 3.11 / FastAPI)
│   ├── api.py                      #   /recon, /gvm, /github-hunt endpoints with SSE streaming
│   ├── container_manager.py        #   Docker SDK: spawn containers, health checks, log streaming, cleanup
│   └── models.py                   #   Pydantic request/response models (ReconState, GvmState, etc.)
│
├── recon/                          # 6-phase reconnaissance pipeline (runs in ephemeral Kali container)
│   ├── main.py                     #   Pipeline entry point — runs phases sequentially
│   ├── entrypoint.sh               #   Docker entrypoint script
│   ├── domain_recon.py             #   Phase 1: DNS, crt.sh, HackerTarget, Knockpy subdomain enumeration
│   ├── whois_recon.py              #   WHOIS lookups (called by domain_recon)
│   ├── port_scan.py                #   Phase 2: Naabu SYN/CONNECT scan + Shodan InternetDB passive
│   ├── http_probe.py               #   Phase 3: Httpx probing, Wappalyzer tech detection, TLS inspection
│   ├── resource_enum.py            #   Phase 4: Katana web crawling, Kiterunner API discovery, GAU passive URLs
│   ├── vuln_scan.py                #   Phase 5: Nuclei template scanning (9000+ templates)
│   ├── shodan_enrich.py            #   Phase 6: Shodan host lookup, reverse DNS, passive CVEs
│   ├── add_mitre.py                #   MITRE CWE/CAPEC enrichment for discovered CVEs
│   ├── project_settings.py         #   Fetches scan settings from webapp API
│   ├── helpers/                    #   Shared helper modules
│   │   ├── target_helpers.py       #     Target parsing and validation
│   │   ├── katana_helpers.py       #     Katana crawl output processing
│   │   ├── nuclei_helpers.py       #     Nuclei result parsing
│   │   ├── security_checks.py      #     Security header analysis
│   │   ├── cve_helpers.py          #     CVE lookup and enrichment
│   │   ├── docker_helpers.py       #     Container-aware path resolution
│   │   ├── iana_services.py        #     IANA port/service mapping
│   │   ├── anonymity.py            #     Tor/proxy support
│   │   └── resource_enum/          #     Resource enumeration sub-helpers
│   ├── tests/                      #   Recon test suite
│   ├── data/                       #   Static data files (wordlists, templates)
│   └── Dockerfile                  #   Kali-based recon container image
│
├── webapp/                         # Next.js frontend + backend API (TypeScript)
│   ├── src/
│   │   ├── app/                    #   Next.js App Router — pages and API routes
│   │   │   ├── api/                #     Backend REST endpoints
│   │   │   │   ├── projects/       #       CRUD for projects, settings, recon/GVM/github-hunt triggers
│   │   │   │   ├── conversations/  #       Conversation + chat message management
│   │   │   │   ├── remediations/   #       CypherFix remediation CRUD + batch operations
│   │   │   │   ├── reports/        #       Pentest report generation and retrieval
│   │   │   │   ├── models/         #       Available LLM model listing
│   │   │   │   ├── users/          #       User management and settings
│   │   │   │   ├── analytics/      #       Project analytics data
│   │   │   │   ├── graph/          #       Neo4j graph query endpoints
│   │   │   │   ├── agent/          #       Agent-related API endpoints
│   │   │   │   ├── cypherfix/      #       CypherFix-specific API endpoints
│   │   │   │   ├── recon/          #       Recon status and control
│   │   │   │   ├── gvm/            #       GVM scanner status and control
│   │   │   │   ├── github-hunt/    #       GitHub secret hunt control
│   │   │   │   ├── guardrail/      #       Scope guardrail validation
│   │   │   │   ├── roe/            #       Rules of Engagement management
│   │   │   │   ├── ws/             #       WebSocket proxy endpoints
│   │   │   │   └── health/         #       Health check
│   │   │   ├── projects/           #     Project dashboard pages
│   │   │   ├── graph/              #     Attack surface graph visualization (2D/3D)
│   │   │   ├── settings/           #     Global settings (LLM keys, API keys)
│   │   │   ├── cypherfix/          #     CypherFix remediation dashboard
│   │   │   ├── reports/            #     Report listing and viewing
│   │   │   └── insights/           #     Analytics, charts, reporting
│   │   ├── components/             #   React UI components
│   │   │   ├── layout/             #     App shell, sidebar, header
│   │   │   ├── projects/           #     Project-specific UI (settings panels, agent drawer, graph view)
│   │   │   ├── settings/           #     Global settings forms
│   │   │   ├── ui/                 #     Shared primitives (buttons, modals, badges, tables)
│   │   │   └── icons/              #     Custom icon components
│   │   ├── lib/                    #   Shared utilities
│   │   │   ├── prisma.ts           #     Prisma client singleton
│   │   │   ├── websocket-types.ts  #     WebSocket message type definitions
│   │   │   ├── cypherfix-types.ts  #     CypherFix TypeScript types
│   │   │   ├── recon-types.ts      #     Recon pipeline TypeScript types
│   │   │   ├── llmProviderPresets.ts #   LLM provider configuration presets
│   │   │   ├── validation.ts       #     Input validation utilities
│   │   │   └── report/             #     Report generation utilities
│   │   └── hooks/                  #   React hooks
│   │       ├── useAgentWebSocket.ts #    Agent chat WebSocket connection
│   │       ├── useCypherFixTriageWS.ts # Triage agent WebSocket
│   │       ├── useCypherFixCodeFixWS.ts # CodeFix agent WebSocket
│   │       ├── useReconSSE.ts      #     Recon progress SSE stream
│   │       ├── useGvmSSE.ts        #     GVM scan progress SSE stream
│   │       ├── useGithubHuntSSE.ts #     GitHub hunt progress SSE stream
│   │       ├── useProjects.ts      #     Project CRUD operations
│   │       ├── useConversations.ts #     Conversation management
│   │       ├── useRemediations.ts  #     CypherFix remediation data
│   │       ├── useReports.ts       #     Report management
│   │       ├── useSession.ts       #     User session management
│   │       ├── useUsers.ts         #     User management
│   │       ├── useActiveSessions.ts #    Track active agent sessions
│   │       ├── useReconStatus.ts   #     Recon pipeline status polling
│   │       ├── useGvmStatus.ts     #     GVM scanner status polling
│   │       ├── useGithubHuntStatus.ts #  GitHub hunt status polling
│   │       ├── useChatPersistence.ts #   Chat history persistence
│   │       └── useTheme.ts         #     Dark/light theme toggle
│   ├── server_actions/             #   Next.js server actions
│   │   └── graph_queries.ts        #     Neo4j Cypher queries for graph visualization
│   └── prisma/                     #   Prisma schema (push-based, NOT migration-based)
│       └── schema.prisma           #     Database schema with 190+ project settings
│
├── mcp/                            # MCP tool infrastructure
│   ├── kali-sandbox/               #   Kali Linux Docker image for MCP servers
│   │   └── Dockerfile              #     Kali image with all security tools pre-installed
│   ├── servers/                    #   MCP server implementations
│   │   ├── network_recon_server.py #     HTTP probing + Naabu port scanning (:8000)
│   │   ├── nuclei_server.py        #     Nuclei vulnerability scanning (:8002)
│   │   ├── metasploit_server.py    #     Metasploit Framework RPC (:8003)
│   │   ├── nmap_server.py          #     Nmap network scanning (:8004)
│   │   └── run_servers.py          #     Supervisor that starts all MCP servers
│   ├── nuclei-templates/           #   Nuclei template collection
│   └── docker-compose.yml          #   MCP-specific compose overrides
│
├── graph_db/                       # Neo4j graph utilities and schema helpers
├── gvm_scan/                       # OpenVAS/GVM vulnerability scanner Python wrapper
├── github_secret_hunt/             # GitHub credential scanner (40+ regex patterns + Shannon entropy)
├── guinea_pigs/                    # Intentionally vulnerable test applications
│   ├── apache_2.4.49/              #   Apache CVE-2021-41773 (path traversal + RCE)
│   ├── apache_2.4.25/              #   Apache CVE-2017-3167 (auth bypass)
│   └── node_serialize_1.0.0/       #   Node.js deserialization RCE
│
├── readmes/                        # All documentation (you are here)
├── .github/                        # GitHub Actions CI/CD workflows
├── docker-compose.yml              # Full stack orchestration — all containers, networks, volumes
├── .env.example                    # Environment variable template
├── CONTRIBUTING.md                 # Contribution guidelines and contributor ranks
├── CHANGELOG.md                    # Release history
├── DISCLAIMER.md                   # Legal disclaimer
└── SECURITY.md                     # Security vulnerability reporting
```

---

## 4. How the System Works

### 4.1 Agent System (agentic/)

The agent is an autonomous AI pentester built on **LangGraph** implementing the **ReAct (Reasoning and Acting)** pattern.

**How the ReAct loop works:**

1. **Think** — The LLM analyzes the current state, reasons about what to do next, and selects a tool (or generates a final response).
2. **Execute** — The orchestrator executes the selected tool (MCP call, Neo4j query, web search, etc.) and captures the output.
3. **Observe** — The tool result is fed back to the LLM as context for the next reasoning step.
4. This cycle repeats until the task is complete or the max iteration limit is reached (default: 100).

**LangGraph state machine:**

The orchestrator is built as a LangGraph graph with these nodes:

- **`initialize_node`** — Sets up the LLM, loads project settings, establishes MCP connections to the Kali sandbox.
- **`think_node`** — LLM reasoning step. Outputs either a tool call, a multi-step plan, or a text response.
- **`execute_tool_node`** — Runs the selected tool and records the result. Supports parallel execution of independent tools via `asyncio.gather()`.
- **`execute_plan_node`** — Executes a multi-step plan the LLM has produced.
- **`generate_response_node`** — Formats the final response for the user.
- **`approval_nodes`** — Pauses execution and asks the user for approval before dangerous operations. Also handles agent-initiated questions to the user.

Conditional edges route between nodes based on the current phase, tool requirements, and whether approval is needed.

**Phase-based execution:**

The agent operates in three phases, each with its own tool availability and approval requirements:

| Phase | Tools Available | Approval Required |
|-------|----------------|-------------------|
| **Reconnaissance** | Neo4j queries, web search, Shodan, Google Dork, Deep Think | No |
| **Exploitation** | All recon tools + MCP tools (Nmap, Nuclei, Metasploit, Network Recon) | Yes (configurable) |
| **Post-Exploitation** | All tools + Metasploit post modules | Yes (configurable) |

Phase transitions happen automatically — the agent classifies its own actions using the classification prompt and shifts phases when the task requires it.

**Tool execution:**

- **MCP tools** — Security tools (Nmap, Nuclei, Metasploit, Network Recon) run in the `kali-sandbox` container and are accessed via the MCP protocol through `langchain-mcp-adapters`. The connection URL is `http://kali-sandbox:8000/sse`.
- **Native tools** — Neo4j Cypher queries (text-to-Cypher via LLM), Tavily web search, Shodan API, and Google Dork are implemented directly in Python within `tools.py`.

**WebSocket streaming:**

The agent streams events to the frontend in real-time via WebSocket (`/ws/agent`): status updates, reasoning thoughts (including streaming chunks), tool calls with arguments, tool results, approval requests, questions, and final responses.

**Multi-objective support:**

Multiple agent sessions can run in parallel against the same target, each pursuing different attack paths (e.g., one brute-forcing SSH while another exploits a web CVE). Sessions are isolated by `session_id`.

> For the complete WebSocket protocol spec, state diagrams, multi-objective support, RoE guardrails, and EvoGraph attack chain recording, see [README.PENTEST_AGENT.md](README.PENTEST_AGENT.md).

### 4.2 CypherFix Agents

CypherFix bridges the gap between discovering vulnerabilities and fixing them in code. It consists of two independent agents that run inside the same `agent` container:

**Triage Agent** (`cypherfix_triage/`):

Uses a hybrid architecture — deterministic data collection followed by LLM-powered analysis:

1. **Static Collection** (no LLM) — Runs 9 hardcoded Cypher queries against Neo4j to collect the full attack surface: vulnerabilities, CVE chains, secrets, exploits, assets, attack chain findings, certificates, and security checks. Progress: 5%–70%.
2. **ReAct Analysis** (LLM) — A single ReAct loop (max 10 iterations) correlates findings across data sources, deduplicates them, applies a weighted priority scoring algorithm (exploit success = 1200 pts, confirmed exploit = 1000 pts, CISA KEV = 800 pts, etc.), and outputs structured remediation entries. The LLM can also run follow-up Cypher queries or web searches if it needs more context.
3. **Persistence** — Batch-saves remediations to PostgreSQL via `POST /api/remediations/batch`.

**CodeFix Agent** (`cypherfix_codefix/`):

Replicates **Claude Code's agentic design** — a pure ReAct while-loop where the LLM is the sole controller:

1. Clones the target repository (shallow clone, `--depth 50`), creates a fix branch (`cypherfix/{remediation_id}`).
2. Explores the codebase using 11 code-aware tools: `github_read`, `github_edit`, `github_grep`, `github_glob`, `github_bash`, `github_symbols`, `github_find_definition`, `github_find_references`, `github_repo_map`, `github_write`, `github_list_dir`.
3. Implements targeted fixes with diff blocks sent to the frontend for user approval. Users can accept, reject (with reason), or send guidance messages mid-loop.
4. Commits, pushes (force, to allow reruns), and opens a GitHub pull request (or updates an existing one).

The CodeFix agent ships with a full polyglot runtime: Node.js 20, Python 3.11, Go 1.22, Ruby, Java 17, PHP, .NET 8 — so it can build and test any target repository.

> For the full architecture, tool specs, diff approval flow, and WebSocket protocols, see [README.CYPHERFIX_AGENTS.md](README.CYPHERFIX_AGENTS.md).

### 4.3 Reconnaissance Pipeline (recon/)

The recon pipeline runs a 6-phase sequential scan inside an ephemeral Docker container:

| Phase | Module | What it does |
|-------|--------|-------------|
| 1 | `domain_recon.py` + `whois_recon.py` | WHOIS lookup, DNS resolution, subdomain enumeration (crt.sh, HackerTarget, Knockpy) |
| 2 | `port_scan.py` | Naabu SYN/CONNECT port scanning + Shodan InternetDB passive data |
| 3 | `http_probe.py` | Httpx HTTP/HTTPS probing, Wappalyzer tech detection, TLS certificate extraction, security header checks |
| 4 | `resource_enum.py` | Katana web crawling, Kiterunner API discovery, GAU passive URL collection |
| 5 | `vuln_scan.py` + `add_mitre.py` | Nuclei template scanning (9000+ templates) + MITRE CWE/CAPEC enrichment |
| 6 | `shodan_enrich.py` | Shodan host lookup, reverse DNS, passive CVE discovery |

**Container lifecycle:**

1. User clicks "Start Recon" in the webapp.
2. Webapp calls the recon API route, which proxies to the recon orchestrator (`:8010`).
3. The `container_manager.py` uses Docker SDK to spawn an ephemeral container from the `recon` image with host network access. It auto-detects the host mount paths from its own mounts (no hardcoded paths).
4. The recon container runs all phases sequentially. Progress is streamed to the webapp via SSE.
5. Results are written to JSON files (`recon/output/`) and to the Neo4j graph incrementally per phase.
6. The container is cleaned up after completion.

The recon orchestrator also manages **GVM scanner** (`vuln-scanner` service) and **GitHub Secret Hunter** (`github-secret-hunter` service) containers using the same lifecycle pattern.

> For per-phase details, see [README.RECON.md](README.RECON.md) and the individual phase READMEs ([PORT_SCAN](README.PORT_SCAN.md), [HTTP_PROBE](README.HTTP_PROBE.md), [RESOURCE_ENUM](README.RESOURCE_ENUM.md), [VULN_SCAN](README.VULN_SCAN.md), [MITRE](README.MITRE.md)).

### 4.4 Webapp (webapp/)

The webapp is a **Next.js 16** application that serves as both the frontend UI and the backend API.

**Backend (API routes):**

All REST endpoints live in `webapp/src/app/api/`. There are 17 route groups:

| Route Group | Purpose |
|-------------|---------|
| `projects/` | CRUD for projects + all project settings (190+ fields) |
| `conversations/` | Agent conversation + chat message management |
| `remediations/` | CypherFix remediation CRUD + batch operations |
| `reports/` | Pentest report generation and retrieval |
| `models/` | Available LLM model listing based on configured providers |
| `users/` | User management and per-user settings |
| `analytics/` | Project analytics data aggregation |
| `graph/` | Neo4j graph query proxy endpoints |
| `agent/` | Agent-related API endpoints |
| `cypherfix/` | CypherFix-specific API |
| `recon/` | Recon pipeline status and control |
| `gvm/` | GVM scanner status and control |
| `github-hunt/` | GitHub secret hunt control |
| `guardrail/` | Scope guardrail validation |
| `roe/` | Rules of Engagement management |
| `ws/` | WebSocket proxy to agent container |
| `health/` | Health check |

**Frontend pages:**

| Page | URL | Purpose |
|------|-----|---------|
| Home | `/` | Landing / project selector |
| Projects | `/projects/[id]` | Project dashboard with agent drawer, settings, recon controls |
| Graph | `/graph` | 2D/3D attack surface graph visualization |
| CypherFix | `/cypherfix` | Remediation dashboard and CodeFix agent |
| Reports | `/reports` | Pentest report listing and viewing |
| Settings | `/settings` | Global settings (LLM providers, API keys) |
| Insights | `/insights` | Analytics charts and project metrics |

**Database access:**

- **PostgreSQL** via Prisma ORM — all user, project, conversation, and remediation data. Uses **push-based schema management** (`prisma db push`), NOT migrations.
- **Neo4j** via the official driver — read-only queries for attack surface visualization. Graph queries live in `server_actions/graph_queries.ts`.

**Real-time communication:**

- **WebSocket** — Agent chat connections are proxied to the agent container (internal `:8080`, host `:8090`) via the `/api/ws` route.
- **SSE** — Recon, GVM, and GitHub hunt progress is streamed from the recon orchestrator (`:8010`).

**Internal service URLs** (for inter-container communication within Docker network):

| Service | Internal URL |
|---------|-------------|
| Agent | `http://agent:8080` |
| Recon Orchestrator | `http://recon-orchestrator:8010` |
| Webapp | `http://webapp:3000` |
| Kali Sandbox (MCP) | `http://kali-sandbox:8000/sse` |
| Neo4j | `bolt://neo4j:7687` |
| PostgreSQL | `postgresql://redamon:redamon_secret@postgres:5432/redamon` |

**React hooks:**

The webapp exposes 19 custom hooks in `src/hooks/` that encapsulate all real-time communication and data fetching logic. Each SSE/WebSocket connection has its own dedicated hook (e.g., `useAgentWebSocket`, `useReconSSE`, `useCypherFixTriageWS`).

> For the component tree and page structure, see [README.WEBAPP.md](README.WEBAPP.md).

### 4.5 Settings Architecture

RedAmon has **190+ project settings** that control everything from Katana crawl depth to Metasploit payload configuration.

**Where settings live:**

```
User edits in Webapp UI (/projects/[id] → Settings panels)
        │
        ▼
PostgreSQL (Project model, via Prisma)
        │
        ▼
Agent/Recon fetch at runtime via GET /api/projects/:id
        │
        ▼
Merged with DEFAULT_AGENT_SETTINGS (project_settings.py)
        │
        ▼
Applied during execution
```

**Multi-layer defaults:**

Settings have defaults defined in **four layers** that must stay in sync:

1. **Prisma schema** (`webapp/prisma/schema.prisma`) — Database column default value
2. **Python defaults** (`agentic/project_settings.py` → `DEFAULT_AGENT_SETTINGS` dict) — Fallback when the webapp API is unavailable or returns null
3. **Frontend fallback** — `onChange` handler in the settings UI component provides a client-side default
4. **Existing DB rows** — Must be backfilled via SQL `UPDATE` when adding a new setting with a non-null default

> **Critical**: When changing a default value, you MUST update ALL four layers and restart agent + webapp. See the [Adding a New Project Setting](#61-adding-a-new-project-setting) checklist.

---

## 5. Development Workflow

### 5.1 Prerequisites

- **Docker** & **Docker Compose v2+** ([install guide](https://docs.docker.com/get-docker/))
- **Git**
- A code editor (VS Code recommended)
- At least one LLM API key — configured in the webapp UI at `/settings`, NOT in `.env`
- Recommended: **8 GB RAM minimum** (GVM stack is memory-hungry)

### 5.2 First-Time Setup

```bash
git clone https://github.com/samugit83/redamon.git
cd redamon
cp .env.example .env          # Edit: set NVD_API_KEY if you have one
docker compose up -d           # Start all services
```

- **First run**: GVM feed sync takes **~10–15 minutes**. All other services are ready immediately.
- Access the webapp at **http://localhost:3000**.
- Create a user account.
- Configure your LLM provider API key in the webapp at `/settings` (Global Settings page).
- Create a project, set a target domain, and you're ready to go.

**Verify everything is running:**

```bash
docker compose ps              # All services should show "running" or "healthy"
docker compose logs webapp --tail=5   # Should show "Ready in X ms"
docker compose logs agent --tail=5    # Should show "Uvicorn running on 0.0.0.0:8080"
```

### 5.3 Hot-Reload vs Rebuild

This is the most important table for day-to-day development. It tells you exactly what to do after changing any file:

| What you changed | Action needed | Why |
|---|---|---|
| `webapp/src/**` | **Nothing** — automatic | Next.js HMR detects changes instantly |
| `webapp/server_actions/**` | **Nothing** — automatic | Next.js HMR |
| `agentic/**/*.py` | `docker compose restart agent` | Python caches modules at import time; restart forces re-import |
| `recon_orchestrator/**/*.py` | **Nothing** — automatic | Uvicorn watches the mounted source directory |
| `recon/**/*.py` | **Nothing** — automatic | Each recon run spawns a new container that picks up the volume-mounted code |
| `mcp/servers/**/*.py` | `docker compose restart kali-sandbox` | MCP servers cache modules at startup |
| `webapp/package.json` (new dep) | `docker compose build webapp && docker compose up -d webapp` | New npm packages require image rebuild |
| `agentic/requirements.txt` (new dep) | `docker compose build agent && docker compose up -d agent` | New pip packages require image rebuild |
| `recon_orchestrator/requirements.txt` | `docker compose build recon-orchestrator && docker compose up -d recon-orchestrator` | Same |
| `recon/requirements.txt` | `docker compose build recon && docker compose up -d recon-orchestrator` | Recon image rebuild; orchestrator spawns new containers from it |
| `mcp/requirements.txt` | `docker compose build kali-sandbox && docker compose up -d kali-sandbox` | Same |
| Any `Dockerfile` | `docker compose build <service> && docker compose up -d <service>` | Dockerfile changes always need rebuild |
| `docker-compose.yml` | `docker compose up -d` | Compose detects config changes and recreates affected containers |
| `webapp/prisma/schema.prisma` | `docker compose exec webapp npx prisma db push` | Push schema changes to PostgreSQL |
| New default value | Update ALL 4 layers + restart agent & webapp | See [checklist](#61-adding-a-new-project-setting) |

### 5.4 Common Commands

```bash
# ─── Logs ────────────────────────────────────────────────────────────────
docker compose logs -f agent                    # Follow agent logs (live)
docker compose logs -f webapp                   # Follow webapp logs
docker compose logs -f recon-orchestrator       # Follow recon orchestrator
docker compose logs --tail=200 agent            # Last 200 lines

# ─── Shell Access ────────────────────────────────────────────────────────
docker compose exec agent bash                  # Shell into agent container
docker compose exec webapp sh                   # Shell into webapp (Alpine, no bash)
docker compose exec kali-sandbox bash           # Shell into Kali sandbox
docker compose exec postgres psql -U redamon    # PostgreSQL interactive shell

# ─── Rebuild ─────────────────────────────────────────────────────────────
docker compose build webapp                     # Rebuild webapp image only
docker compose build agent                      # Rebuild agent image only
docker compose build                            # Rebuild ALL images
docker compose up -d                            # Recreate containers with new images

# ─── Database (PostgreSQL) ──────────────────────────────────────────────
docker compose exec webapp npx prisma db push   # Apply Prisma schema changes
docker compose exec webapp npx prisma studio    # Visual DB browser (http://localhost:5555)
docker compose exec postgres psql -U redamon -c "SELECT * FROM \"Project\" LIMIT 5;"

# ─── Database (Neo4j) ───────────────────────────────────────────────────
# Browser UI:  http://localhost:7474
# Bolt URL:    bolt://localhost:7687
# Credentials: neo4j / changeme123 (or your NEO4J_PASSWORD from .env)

# ─── Service Management ─────────────────────────────────────────────────
docker compose ps                               # Check all container statuses
docker compose restart agent                    # Restart single service (no rebuild)
docker compose restart agent webapp             # Restart multiple services
docker compose down && docker compose up -d     # Full restart (preserves data)
docker compose down -v && docker compose up -d  # DANGER: deletes ALL data (volumes)
```

### 5.5 Important Rules

1. **Never use `prisma migrate`** — The project uses `prisma db push` (push-based workflow). Migrations are not tracked.
2. **Never build the webapp locally** with `npx` or `npm run build` — Always use `docker compose build webapp`. The local `node_modules` may differ from the container image.
3. **Never add Python imports** to `agentic/` without ensuring the package is listed in `requirements.txt` and the image has been rebuilt — Otherwise the container will crash-loop on startup.
4. **LLM API keys are per-user** — They are configured in the webapp UI at `/settings` and stored in PostgreSQL. They are NOT environment variables.
5. **Docker timestamps** use RFC3339Nano format with nanoseconds — If you parse them in Python, truncate to 6 fractional digits before passing to `datetime.fromisoformat()`.
6. **Source code is volume-mounted** — The `agentic/` and `recon_orchestrator/` directories are mounted into their containers at `/app`. You edit files on the host and the container sees changes immediately. But Python still caches modules, so **always restart the agent** after editing `.py` files in `agentic/`.

### 5.6 AI-Assisted Coding

AI-assisted development is welcome and encouraged. RedAmon is a large, multi-language, multi-container codebase — AI coding tools can significantly speed up development and help you navigate unfamiliar subsystems.

**Recommended model:** We recommend **Anthropic Claude Opus 4.6** (`claude-opus-4-6`) given the complexity of this repository. Opus handles large context windows, multi-file reasoning, and architectural decisions better than smaller models. You can use it through [Claude Code](https://claude.com/claude-code), Cursor, Windsurf, or any editor that supports Anthropic models.

Other capable models (GPT-5, Gemini 2.5 Pro) can also work, but Opus 4.6 has been tested extensively on this codebase and provides the most reliable results.

**Ground rules for AI-assisted contributions:**

1. **Understand before committing** — Always review and understand the code your AI generates before submitting a PR. You are responsible for every line you push, not the AI.
2. **Read the relevant files first** — Point your AI tool at the specific files and subsystems it needs to understand. Blind generation without context produces hallucinated imports, wrong API signatures, and broken integrations.
3. **Respect the architecture** — RedAmon has clear boundaries between subsystems (webapp, agent, recon, MCP). Don't let AI tools blur these boundaries by generating cross-cutting shortcuts that bypass the established communication patterns (REST, WebSocket, MCP protocol).
4. **Test inside Docker** — AI tools often generate code that works locally but fails in the container. Always verify your changes inside the Docker stack, not just in your editor's preview.
5. **Don't blindly add dependencies** — If the AI suggests a new `import` or `require`, check that the package exists in the relevant `requirements.txt` or `package.json` first. Adding an uninstalled dependency will crash-loop the container.
6. **Keep diffs minimal** — Resist the temptation to let AI refactor, reformat, or "improve" surrounding code. PRs should only contain changes relevant to the task. Large AI-generated diffs that touch unrelated files are hard to review and will be rejected.
7. **No AI-generated comments or docs unless requested** — Don't let AI litter the code with docstrings, inline comments, or type annotations that weren't there before. Follow the existing code style.
8. **Validate Cypher queries and Prisma schemas** — AI models frequently hallucinate Neo4j node labels, relationship types, and Prisma field names. Always cross-check generated queries against [GRAPH.SCHEMA.md](GRAPH.SCHEMA.md) and the actual Prisma schema.

---

## 6. Feature Development Checklists

### 6.1 Adding a New Project Setting

1. Add the field to the Prisma schema (`webapp/prisma/schema.prisma`) with a default value.
2. Push the schema:
   ```bash
   docker compose exec webapp npx prisma db push
   ```
3. Add the same default to `DEFAULT_AGENT_SETTINGS` in `agentic/project_settings.py` (and/or `recon/project_settings.py` if the recon pipeline uses it).
4. Add the UI control in the appropriate webapp settings component. Include a fallback value in the `onChange` handler.
5. Backfill existing database rows if needed:
   ```bash
   docker compose exec postgres psql -U redamon -c \
     "UPDATE \"Project\" SET \"newField\" = 'default_value' WHERE \"newField\" IS NULL;"
   ```
6. Restart affected services:
   ```bash
   docker compose restart agent webapp
   ```

### 6.2 Adding a New Agent Tool

1. Define the tool schema (name, description, parameters) in `agentic/prompts/tool_registry.py`.
2. Implement the tool manager — either add to `agentic/tools.py` or create a dedicated file.
3. Register the tool in the orchestrator's tool binding (in `orchestrator.py` or the relevant node file).
4. If the tool should only be available in certain phases, add it to the phase-tool mapping in `prompts/base.py`.
5. Restart:
   ```bash
   docker compose restart agent
   ```

### 6.3 Adding a New Webapp API Route

1. Create the route handler at `webapp/src/app/api/<your-route>/route.ts`.
2. Follow existing patterns: validate input with TypeScript types, use `prisma` from `lib/prisma.ts` for DB access, return `NextResponse.json()`.
3. If you need to call other services, use the internal Docker network URLs (see the [Internal service URLs](#44-webapp-webapp) table):
   - Agent: `http://agent:8080` (NOT `:8090` — that's the host-mapped port)
   - Recon Orchestrator: `http://recon-orchestrator:8010`
   - Webapp itself: `http://webapp:3000` (for inter-route calls)
4. No restart needed — Next.js HMR picks up new files automatically.

### 6.4 Adding a New Recon Phase

1. Create the phase module in `recon/` (e.g., `new_phase.py`).
2. Add the phase call to the pipeline in `recon/main.py`.
3. If the phase writes to Neo4j, add the Cypher queries using the existing Neo4j driver pattern (see other phase modules for examples).
4. Add any new settings to `project_settings.py` (both `recon/` and `webapp/` layers via Prisma).
5. The next recon run will automatically use the new phase — source is volume-mounted.

### 6.5 Adding a New Frontend Hook

1. Create the hook in `webapp/src/hooks/` following the naming convention: `useYourFeature.ts`.
2. Export it from `webapp/src/hooks/index.ts`.
3. For WebSocket hooks, follow the pattern in `useAgentWebSocket.ts` (connect, message handling, cleanup).
4. For SSE hooks, follow `useReconSSE.ts` (EventSource, reconnection, progress tracking).
5. For data fetching hooks, use TanStack React Query (see `useProjects.ts` for examples).

---

## 7. Debugging & Testing

### Debugging the Agent

The agent logs to stdout inside the container. All reasoning steps, tool calls, and errors are logged.

```bash
# Live agent logs (most useful for debugging)
docker compose logs -f agent

# Check if the agent container is healthy
docker compose ps agent

# Shell in and inspect the running process
docker compose exec agent bash
ps aux | grep uvicorn
```

**Common agent issues:**

| Symptom | Cause | Fix |
|---------|-------|-----|
| Container keeps restarting | Missing Python package or import error | Check logs: `docker compose logs agent --tail=50`, then fix the import and rebuild if needed |
| WebSocket connection refused | Agent not ready yet | Wait a few seconds; check logs for "Uvicorn running" |
| Tool execution timeout | MCP server (Kali sandbox) not responding | `docker compose restart kali-sandbox`, then `docker compose restart agent` |
| "Settings fetch failed" | Webapp not reachable from agent | Ensure webapp is running: `docker compose ps webapp` |
| LLM API error (401/429) | Invalid or rate-limited API key | Check/update API key in webapp `/settings` |

### Debugging the Webapp

```bash
docker compose logs -f webapp               # Live logs (Next.js + API)
docker compose exec webapp sh               # Shell into webapp container
```

**Prisma debugging:**

```bash
# Open Prisma Studio for visual DB inspection
docker compose exec webapp npx prisma studio

# Check current schema state
docker compose exec webapp npx prisma db pull

# Validate schema without pushing
docker compose exec webapp npx prisma validate
```

### Debugging Neo4j

```bash
# Open Neo4j Browser at http://localhost:7474
# Run Cypher queries directly:
MATCH (n) RETURN labels(n), count(n) ORDER BY count(n) DESC;

# Check graph size
MATCH (n) RETURN count(n) AS nodes;
MATCH ()-[r]-() RETURN count(r) AS relationships;
```

### Testing with Guinea Pigs

The `guinea_pigs/` folder contains intentionally vulnerable applications you can use to test the full pipeline locally:

| Guinea Pig | Vulnerability | How to use |
|-----------|---------------|------------|
| `apache_2.4.49` | CVE-2021-41773 (path traversal + RCE) | `docker compose -f guinea_pigs/apache_2.4.49/docker-compose.yml up -d` |
| `apache_2.4.25` | CVE-2017-3167 (auth bypass) | `docker compose -f guinea_pigs/apache_2.4.25/docker-compose.yml up -d` |
| `node_serialize_1.0.0` | Node.js deserialization RCE | `docker compose -f guinea_pigs/node_serialize_1.0.0/docker-compose.yml up -d` |

These containers join the `pentest-net` network, so the agent and MCP tools can reach them. Point your project target at the guinea pig's IP to test reconnaissance, exploitation, and post-exploitation flows end-to-end.

> For details on available guinea pigs, see [README.GPIGS.md](README.GPIGS.md).

### Running Recon Tests

The recon `tests/` directory is mounted into the recon-orchestrator container at `/app/recon/tests/`:

```bash
docker compose exec recon-orchestrator bash
cd /app/recon && python -m pytest tests/ -v
```

Alternatively, you can run the recon container directly:

```bash
docker compose run --rm recon python -m pytest tests/ -v
```

---

## 8. Environment Variables

All infrastructure variables are defined in `.env` (copied from `.env.example`). The `.env.example` file is intentionally minimal — only infrastructure and scanner variables belong here.

> **Note**: LLM API keys (OpenAI, Anthropic, Tavily, Shodan, etc.) are configured **per-user** in the webapp UI at `/settings` and stored in PostgreSQL. They are NOT set via environment variables.

### Variables in `.env.example`

| Variable | Default | Description |
|----------|---------|-------------|
| `NVD_API_KEY` | — | NIST NVD API key (optional — enables higher rate limits for CVE lookups) |
| `NGROK_AUTHTOKEN` | — | Ngrok auth token (option 1 for reverse shell tunneling — free, single port) |
| `CHISEL_SERVER_URL` | — | Chisel VPS URL (option 2 for tunneling — requires VPS, multi-port) |
| `CHISEL_AUTH` | — | Chisel authentication credentials |

### Variables in `docker-compose.yml` (with defaults)

These use Docker Compose's `${VAR:-default}` syntax. Override them in `.env` if needed.

| Variable | Default | Description |
|----------|---------|-------------|
| `POSTGRES_USER` | `redamon` | PostgreSQL username |
| `POSTGRES_PASSWORD` | `redamon_secret` | PostgreSQL password |
| `POSTGRES_DB` | `redamon` | PostgreSQL database name |
| `NEO4J_PASSWORD` | `changeme123` | Neo4j password |
| `POSTGRES_PORT` | `5432` | Host port for PostgreSQL |
| `NEO4J_HTTP_PORT` | `7474` | Host port for Neo4j Browser UI |
| `NEO4J_BOLT_PORT` | `7687` | Host port for Neo4j Bolt protocol |
| `WEBAPP_PORT` | `3000` | Host port for the webapp |
| `AGENT_PORT` | `8090` | Host port for the agent API (maps to internal :8080) |
| `RECON_ORCH_PORT` | `8010` | Host port for the recon orchestrator |

> MCP server ports (8000, 8002–8004) are hardcoded in `docker-compose.yml`. To change them, edit the `ports:` section directly.

---

## 9. Documentation Index

All deep-dive documentation lives in the `readmes/` folder alongside this file.

> The project also maintains a **[GitHub Wiki](https://github.com/samugit83/redamon/wiki)** with additional guides and walkthroughs.

### System-Level

| Document | What it covers |
|----------|----------------|
| [ARCHITECTURE.md](ARCHITECTURE.md) | Mermaid diagrams: system topology, data flow pipeline, Docker container architecture, MCP integration, agent workflow |
| [TECH_STACK.md](TECH_STACK.md) | Detailed technology role descriptions organized by layer |
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | OS-specific issues and fixes (Linux, Windows, macOS) |

### Agent

| Document | What it covers |
|----------|----------------|
| [README.PENTEST_AGENT.md](README.PENTEST_AGENT.md) | Full pentest agent architecture: ReAct loop, LangGraph state machine, WebSocket protocol, tool specs, multi-objective support, RoE guardrails, EvoGraph attack chains, prompt token optimization |
| [README.CYPHERFIX_AGENTS.md](README.CYPHERFIX_AGENTS.md) | Triage + CodeFix agents: hybrid architecture, prioritization algorithm, 11 code tools, diff approval flow, GitHub PR integration, WebSocket protocols |


### Reconnaissance

| Document | What it covers |
|----------|----------------|
| [README.RECON.md](README.RECON.md) | Reconnaissance pipeline overview — all 6 phases |
| [README.RECON_ORCHESTRATOR.md](README.RECON_ORCHESTRATOR.md) | Container lifecycle management (spawn, health-check, SSE streaming, cleanup) |
| [README.PORT_SCAN.md](README.PORT_SCAN.md) | Phase 2: Naabu port scanning + Shodan passive |
| [README.HTTP_PROBE.md](README.HTTP_PROBE.md) | Phase 3: Httpx probing, Wappalyzer, TLS inspection |
| [README.RESOURCE_ENUM.md](README.RESOURCE_ENUM.md) | Phase 4: Katana crawling, Kiterunner API discovery, GAU |
| [README.VULN_SCAN.md](README.VULN_SCAN.md) | Phase 5: Nuclei template scanning |
| [README.MITRE.md](README.MITRE.md) | MITRE CWE/CAPEC enrichment for discovered CVEs |

### Infrastructure & Data

| Document | What it covers |
|----------|----------------|
| [README.MCP.md](README.MCP.md) | MCP tool servers in the Kali sandbox (Nmap, Nuclei, Metasploit, Network Recon) |
| [README.WEBAPP.md](README.WEBAPP.md) | Webapp architecture, component tree, page structure |
| [README.GVM.md](README.GVM.md) | OpenVAS/GVM scanner integration (170k+ NVTs) |
| [README.GRAPH_DB.md](README.GRAPH_DB.md) | Neo4j graph utilities |
| [GRAPH.SCHEMA.md](GRAPH.SCHEMA.md) | Full Neo4j node types, relationship types, and property definitions |
| [README.POSTGRES.md](README.POSTGRES.md) | PostgreSQL schema details (Prisma models, field reference) |
| [README.GPIGS.md](README.GPIGS.md) | Guinea pigs — intentionally vulnerable test applications for local testing |

### Project-Level

| Document | Location | What it covers |
|----------|----------|----------------|
| [CONTRIBUTING.md](../CONTRIBUTING.md) | repo root | Contribution guidelines, PR process, contributor ranks |
| [CHANGELOG.md](../CHANGELOG.md) | repo root | Release history and version notes |
| [DISCLAIMER.md](../DISCLAIMER.md) | repo root | Legal disclaimer — authorized testing only |
| [SECURITY.md](../SECURITY.md) | repo root | Security vulnerability reporting |
