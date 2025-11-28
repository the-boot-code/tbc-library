# Upstream Agent Zero Documentation References

> **Navigation**: [← Back to README](README.md) | [Project Meta and Glossary →](TBC_LIBRARY_META_AND_GLOSSARY.md)

This document indexes **upstream Agent Zero documentation** that ships with the Agent Zero image under `/a0/docs/...`.

These upstream files are **not** part of the tbc-library knowledge tree on disk, but they are usually accessible inside an Agent Zero container and can be treated as authoritative references when you need details that go beyond what the tbc-library documentation covers.

Use this index when you want to:

- Confirm core Agent Zero behaviour or concepts that tbc-library layers on top of.
- Find the upstream explanation for a feature that the tbc-library docs only summarize or override.
- Anchor your reasoning in the engine's own documentation while still respecting tbc-library's layered abstractions.

## How to use this index

- **Humans (host perspective)**: Use the "Host example" paths to locate the corresponding `/a0/docs/...` file under a running container's directory in `containers/<agent>/a0/docs/...`.
- **Agents (inside-container perspective)**: Use the **Upstream in-container path** exactly as shown (for example, `/a0/docs/extensibility.md`). When you need more detail than the tbc-library docs provide, you may cite or summarize the upstream doc.
- **Precedence and safety**: When you are operating inside this `tbc-library` deployment (either from the host repository or from within one of its containers), treat the tbc-library docs as authoritative for what you may change (Compose files, volumes, knowledge, profiles, tools). Use upstream `/a0/docs/...` to understand the engine and generic usage, not to rewire this deployment unless the tbc-library docs explicitly instruct you to.
- Treat upstream docs as **engine-level references** and tbc-library docs as the **layered, deployment-specific view**. When they differ, prefer tbc-library for deployment behaviour, and use upstream docs to understand the engine's intent.

---

## Extensibility framework (core Agent Zero)

- **Topic**: Extensibility framework in Agent Zero (extensions, tools, prompts, projects)
- **Upstream in-container path**: `/a0/docs/extensibility.md`
- **Host example**: `containers/a0-clarity/a0/docs/extensibility.md` (for the `a0-clarity` container in this repository)

**What it covers**

- Overview of the **extensible components** in Agent Zero:
  - Extensions
  - Tools
  - API endpoints
  - Helpers
  - Prompts
  - Subagent customization
  - Projects
- How extension points such as `agent_init`, `message_loop_start`, `system_prompt`, and others are discovered and invoked via `call_extensions`.
- Override rules for **default** versus **agent-specific** implementations for:
  - Extensions (`/python/extensions/{extension_point}/` vs `/agents/{agent_profile}/extensions/{extension_point}/`)
  - Tools (`/python/tools/` vs `/agents/{agent_profile}/tools/`)
  - Prompts (`/prompts/` vs `/agents/{agent_profile}/prompts/`)
- Prompt features in the upstream engine:
  - Variable placeholders (`{{var}}`)
  - Dynamic variable loaders (paired `.py` files that implement `VariablesPlugin` to compute variables at runtime)
  - File includes (`{{ include "path/to/file.md" }}`)
- Project support under `/a0/usr/projects/...`, including `.a0proj` metadata, project-specific prompts, knowledge, memory, secrets, and variables.

**How it relates to tbc-library docs**

- Use this upstream doc when you need the **engine-level view** of how extensions, tools, prompts, and projects work in Agent Zero.
- Use [TBC_LIBRARY_EXTENSIBILITY.md → Extensibility Features of Agent Zero](TBC_LIBRARY_EXTENSIBILITY.md#extensibility-features-of-agent-zero) when you want the **tbc-library-specific layering**, including:
  - How System Control and dynamic profiles are wired.
  - How shared `_symlink` extensions and prompts are organized under `layers/control_layer/...`.
  - How knowledge trees and solutions under `/a0/knowledge/default/...` are used to document tbc-library tools and behaviour.

When reasoning as an agent, treat `/a0/docs/extensibility.md` as the upstream specification for the extensibility framework, and the tbc-library knowledge cluster as the deployment- and narrative-specific adaptation of that framework.

---

## Architecture overview (core Agent Zero)

- **Topic**: Overall Agent Zero architecture (system layout, runtime container, directories, core components)
- **Upstream in-container path**: `/a0/docs/architecture.md`
- **Host example**: `containers/a0-clarity/a0/docs/architecture.md` (for the `a0-clarity` container in this repository)

**What it covers**

- **System architecture** at a high level:
  - Hierarchical relationship between agents and subagents.
  - How agents call tools and use shared assets such as prompts, memory, knowledge, extensions, and instruments.
  - Diagrams such as `arch-01.svg` and interaction-flow visuals.
- **Runtime architecture** around Docker:
  - Host system responsibilities (Docker, browser, orchestration).
  - Runtime container responsibilities (Web UI, API endpoints, core framework, standardized environment).
  - Notes on the legacy non-Docker setup and how to use full-binaries installation.
- **Implementation details** inside the upstream `/a0` tree:
  - Directory layout (`/docs`, `/instruments`, `/knowledge`, `/logs`, `/memory`, `/prompts`, `/python`, `/api`, `/extensions`, `/helpers`, `/tools`, `/tmp`, `/webui`, `/work_dir`).
  - Key files such as `.env`, `agent.py`, `initialize.py`, `models.py`, `run_ui.py`, and others.
- **Core components** in the upstream engine:
  - Agents and their hierarchy, message structure, and interaction flow.
  - Tools (built-in tools like `call_subordinate`, `code_execution_tool`, `memory_tool`, and how they are organized).
  - Memory system architecture, including message history summarization and context-window optimisation.
  - Prompt organization under `/prompts`, including core prompt files such as `agent.system.main.*.md` and how they define role, communication, solving, tips, behaviour, environment, and tools.
  - Knowledge, instruments, and extensions directories and how they fit into the upstream design.

**How it relates to tbc-library docs**

- Use `/a0/docs/architecture.md` when you need the **engine-level architecture map** for a vanilla Agent Zero deployment: how `/a0` is laid out, which directories exist, and how components like tools, memory, prompts, instruments, and extensions fit together before any tbc-library layering is applied.
- Use [TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md → Docker Compose Orchestration](TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md#docker-compose-orchestration) and [TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md → Structure](TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md#structure) when you want the **tbc-library-specific view** of how `/containers`, `/layers`, and `/volumes` on the host project into `/a0`, `/layers`, `/agent_layer`, `/common_layer`, and `/agent_orchestration` inside the container.
- Use [TBC_LIBRARY_SELF_REVEALING_ORCHESTRATION.md → Direct Agent Access via Bind Mounts](TBC_LIBRARY_SELF_REVEALING_ORCHESTRATION.md#direct-agent-access-via-bind-mounts) when you need concrete bind-mount mappings and path reasoning that sit on top of the upstream architecture.
- Use [TBC_LIBRARY_EXTENSIBILITY.md → Extensibility Features of Agent Zero](TBC_LIBRARY_EXTENSIBILITY.md#extensibility-features-of-agent-zero) when you need to understand how tbc-library adds System Control, dynamic profiles, shared `_symlink` layers, and knowledge trees to that upstream architecture.

When reasoning as an agent, treat `/a0/docs/architecture.md` as the upstream description of the core Agent Zero layout and components, and the tbc-library knowledge cluster as the explanation of how that architecture is projected, extended, and narrated in this deployment.

---

## Connectivity and external integrations (core Agent Zero)

- **Topic**: External API, logs, files, MCP server, and A2A connectivity for Agent Zero
- **Upstream in-container path**: `/a0/docs/connectivity.md`
- **Host example**: `containers/a0-clarity/a0/docs/connectivity.md` (for the `a0-clarity` container in this repository)

**What it covers**

- **External API endpoints** for integrating other applications with Agent Zero:
  - `POST /api_message` for sending messages, attachments, and continuing conversations.
  - `GET/POST /api_log_get` for retrieving logs for a given `context_id`.
  - `POST /api_terminate_chat` for terminating a chat context and freeing resources.
  - `POST /api_reset_chat` for resetting a chat context while keeping the `context_id`.
  - `POST /api_files_get` for retrieving file contents by path as base64 encoded data.
  - Detailed JavaScript examples for each endpoint, including request payloads and typical workflows.
- **API token usage** across subsystems:
  - Explains that a single API token (derived from username and password) is used for External API, MCP, and A2A.
- **MCP server connectivity**:
  - Describes the Agent Zero MCP server endpoints:
    - SSE: `/mcp/sse`.
    - Streamable HTTP: `/mcp/http/`.
  - Provides an example `mcp.json` configuration for MCP clients.
- **A2A (Agent to Agent) connectivity**:
  - Introduces the A2A server and connection URL format using the FastA2A protocol.
  - Shows the `/a2a/t-YOUR_API_TOKEN` URL pattern and where to find it in the UI.

**How it relates to tbc-library docs**

- Use `/a0/docs/connectivity.md` when you need the **engine-level reference** for how Agent Zero exposes external APIs, log access, file retrieval, MCP server endpoints, and A2A connectivity.
- Use [TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md → Docker Compose Orchestration](TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md#docker-compose-orchestration) to understand how these endpoints are surfaced through the container's ports and nginx configuration under tbc-library's Compose setup.
- Use [TBC_LIBRARY_SELF_REVEALING_ORCHESTRATION.md → Direct Agent Access via Bind Mounts](TBC_LIBRARY_SELF_REVEALING_ORCHESTRATION.md#direct-agent-access-via-bind-mounts) when you want to see how self-revealing path mappings (such as `/agent_orchestration` and `/a0/...`) give agents insight into their own connectivity configuration.
- Use [TBC_LIBRARY_EXTENSIBILITY.md → Extensibility Features of Agent Zero](TBC_LIBRARY_EXTENSIBILITY.md#extensibility-features-of-agent-zero) when you need to see how tbc-library-managed tools and System Control profiles interact with connectivity features (for example, how tools may call external APIs or how prompts describe external access patterns).

When reasoning as an agent, treat `/a0/docs/connectivity.md` as the upstream specification for how to reach Agent Zero from the outside world and coordinate with other systems, and use the tbc-library documentation to understand how that connectivity sits inside this layered, self-revealing deployment.

---

## MCP setup and configuration (core Agent Zero)

- **Topic**: Configuring MCP servers for Agent Zero (UI options and `tmp/settings.json` details)
- **Upstream in-container path**: `/a0/docs/mcp_setup.md`
- **Host example**: `containers/a0-clarity/a0/docs/mcp_setup.md` (for the `a0-clarity` container in this repository)

**What it covers**

- How to configure MCP servers for Agent Zero using the Web UI and the `Settings > External Services > MCP Servers` section.
- The meaning and behaviour of the `mcp_servers` field in `tmp/settings.json`:
  - Default behaviour when `mcp_servers` is missing or empty.
  - How the value is stored as a JSON string and how to edit it safely.
  - Example `mcp_servers` JSON string that configures multiple MCP servers (such as `sequential-thinking`, `brave-search`, and `fetch`), including:
    - `name`, `command`, and `args` for each server.
    - Optional `env` values such as `BRAVE_API_KEY`.
- Guidance on when manual editing of `tmp/settings.json` is appropriate and when to prefer the UI.

**How it relates to tbc-library docs**

- Use `/a0/docs/mcp_setup.md` when you need the **engine-level instructions** for how MCP servers are registered and how the `mcp_servers` configuration is represented inside `tmp/settings.json`.
- Use [TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md → Agent perspectives and management](TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md#agent-perspectives-and-management) together with [TBC_LIBRARY_SELF_REVEALING_ORCHESTRATION.md → Direct Agent Access via Bind Mounts](TBC_LIBRARY_SELF_REVEALING_ORCHESTRATION.md#direct-agent-access-via-bind-mounts) when you want to see how `tmp/settings.json` is surfaced and manipulated inside a container (for example, via `/a0/tmp/settings.json` or self-revealing paths under `/agent_layer` and `/containers`).
- Use [TBC_LIBRARY_EXTENSIBILITY.md → Extensibility Features of Agent Zero](TBC_LIBRARY_EXTENSIBILITY.md#extensibility-features-of-agent-zero) when you need to understand how configured MCP servers and other external integrations fit into the larger extensibility story and System Control managed behaviour.

When reasoning as an agent, treat `/a0/docs/mcp_setup.md` as the upstream guide for how MCP servers are configured and how `mcp_servers` is stored, and use the tbc-library knowledge cluster to reason about where `tmp/settings.json` lives in this deployment and how those settings affect layered behaviour.

---

## Notifications (core Agent Zero)

- **Topic**: Agent Zero notification system for backend and frontend
- **Upstream in-container path**: `/a0/docs/notifications.md`
- **Host example**: `containers/a0-clarity/a0/docs/notifications.md` (for the `a0-clarity` container in this repository)

**What it covers**

- **Backend notification helper** in Python:
  - `AgentNotification.info`, `success`, `warning`, `error`, and `progress` convenience methods.
  - Optional `detail`, `display_time`, and `group` parameters.
  - How grouped notifications use the same `group` value so new messages replace older ones.
- **Frontend notification store** in Alpine.js:
  - `$store.notificationStore.info`, `success`, `warning`, `error`, and `progress` methods.
  - Frontend-only notification methods with backend persistence: `frontendError`, `frontendWarning`, `frontendInfo`.
- **Frontend notifications with backend sync**:
  - Behaviour when the backend is connected versus disconnected.
  - Global helper functions such as `toastFrontendError`, `toastFrontendWarning`, and `toastFrontendInfo` that send notifications and automatically fall back to frontend-only when the backend is unavailable.
- **HTML usage examples** for wiring notifications into UI elements.
- **Notification groups and behaviour**:
  - Group semantics for keeping only the most recent notification per group.
  - Parameters (`message`, `title`, `detail`, `display_time`, `group`).
  - Types (`info`, `success`, `warning`, `error`, `progress`) and how they appear in the UI.
  - How notifications are displayed as toasts, stored in history, and accessed via the bell icon.

**How it relates to tbc-library docs**

- Use `/a0/docs/notifications.md` when you need the **engine-level description** of how to emit notifications from backend code and frontend components, and how groups, persistence, and types behave inside the default Agent Zero UI.
- Use [TBC_LIBRARY_EXTENSIBILITY.md → Extensibility Features of Agent Zero](TBC_LIBRARY_EXTENSIBILITY.md#extensibility-features-of-agent-zero) when you want to understand how notifications can be used together with tbc-library extensions, tools, and System Control (for example, to surface profile or connectivity state changes).
- Use [TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md → Agent perspectives and management](TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md#agent-perspectives-and-management) when you need to know where notification helpers live in the filesystem under `/a0/python/helpers` and how they are visible across agents.

When reasoning as an agent, treat `/a0/docs/notifications.md` as the upstream guide to the notification system and use the tbc-library documentation to decide when to generate notifications in the context of layered profiles, connectivity, and orchestration.

---

## Installation and quick start (core Agent Zero)

- **Topic**: Installing Agent Zero and launching the upstream runtime outside tbc-library
- **Upstream in-container paths**: `/a0/docs/installation.md`, `/a0/docs/quickstart.md`
- **Host examples**: `containers/a0-clarity/a0/docs/installation.md`, `containers/a0-clarity/a0/docs/quickstart.md`

**What they cover**

- How to install and update Agent Zero on various platforms using the upstream workflow (Docker, full-binaries, mobile access).
- How to configure settings, choose LLMs, and integrate local models such as Ollama and LM Studio.
- How to launch the upstream web UI (for example, `python run_ui.py`), open the browser, and start a new chat.
- Basic usage patterns such as creating chats, saving/loading chat histories, and running simple tasks (for example, downloading a YouTube video).

**How they relate to tbc-library docs**

- Use these upstream docs when a human asks for **generic Agent Zero installation or first-run help** that is not specific to the tbc-library deployment.
- Use [TBC_LIBRARY_INSTALLATION.md → Installation (Automated, Recommended)](TBC_LIBRARY_INSTALLATION.md#installation-automated-recommended) and related sections when you want the **tbc-library-specific installation and cloning workflow** that creates layered containers such as `a0-template` and `a0-myagent`.
- Use the tbc-library knowledge README and Installation doc to explain how the upstream engine is packaged and orchestrated via Docker Compose under `tbc-library`, then, when needed, point humans to `/a0/docs/installation.md` and `/a0/docs/quickstart.md` for engine-level behaviour.

When reasoning as a helpdesk-style agent, treat `/a0/docs/installation.md` and `/a0/docs/quickstart.md` as the upstream answers for "how do I install and start Agent Zero?", and layer on the tbc-library documentation when the question involves containers, layers, or this deployment's knowledgebase.

---

## Usage guide and Web UI operations (core Agent Zero)

- **Topic**: Day-to-day use of the Agent Zero web UI and its features
- **Upstream in-container path**: `/a0/docs/usage.md`
- **Host example**: `containers/a0-clarity/a0/docs/usage.md`

**What it covers**

- Basic operations in the upstream web UI:
  - Restart framework.
  - Action buttons (New Chat, Reset Chat, Save Chat, Load Chat).
  - File attachments, tool usage, and example tool workflows (for example, web search and code execution).
  - Multi-agent cooperation, prompt engineering, voice interface, KaTeX-based mathematical expressions, file browser, backup and restore.
- Screenshots and explanations of how users interact with the UI.

**How it relates to tbc-library docs**

- Use `/a0/docs/usage.md` when a human asks **"how do I use the Agent Zero UI to do X?"** (for example, using the file browser, prompt engineering tools, or multi-agent features) and the answer is independent of tbc-library's layering.
- Use [TBC_LIBRARY_EXTENSIBILITY.md](TBC_LIBRARY_EXTENSIBILITY.md) when the question is about how tbc-library changes behaviour via profiles, prompts, and knowledge trees, or when you need to explain library-specific tools or prompts that appear in the same UI.

As a helpdesk agent, read `/a0/docs/usage.md` as your upstream handbook for user-facing UI operations, and use tbc-library docs to explain any additional, deployment-specific features layered on top.

---

## Troubleshooting and FAQ (core Agent Zero)

- **Topic**: Common issues, FAQs, and basic troubleshooting steps in upstream Agent Zero
- **Upstream in-container path**: `/a0/docs/troubleshooting.md`
- **Host example**: `containers/a0-clarity/a0/docs/troubleshooting.md`

**What it covers**

- Frequently asked questions such as:
  - Where to put files so the agent can work on them (for example, `/a0/work_dir`).
  - What to check when chat input appears unresponsive (for example, missing API keys).
  - How to integrate open-source models and where to find LLM configuration instructions.
  - Where to find more documentation, tutorials, and community links.
  - How to adjust rate limits and why code execution might be failing.
- Troubleshooting guidance for installation and usage issues (Docker problems, terminal commands, error messages, performance concerns).

**How it relates to tbc-library docs**

- Use `/a0/docs/troubleshooting.md` when a human asks high-level **"why is my Agent Zero not behaving correctly?"** questions that match the upstream patterns.
- Combine it with [TBC_LIBRARY_INSTALLATION.md](TBC_LIBRARY_INSTALLATION.md) and [TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md](TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md) when the problem clearly involves the layered Docker Compose deployment (for example, container startup, ports, or bind mounts) rather than the upstream engine alone.

Treat `/a0/docs/troubleshooting.md` as your first-stop FAQ for core Agent Zero issues, and use tbc-library docs to add deployment-specific context when needed.

---

## Development and contribution (core Agent Zero)

- **Topic**: Setting up a local development environment and contributing to the upstream Agent Zero project
- **Upstream in-container paths**: `/a0/docs/development.md`, `/a0/docs/contribution.md`
- **Host examples**: `containers/a0-clarity/a0/docs/development.md`, `containers/a0-clarity/a0/docs/contribution.md`

**What they cover**

- How to prepare a local development environment for Agent Zero using a VS Code-compatible IDE, Python env, and Docker.
- How to run, debug, and develop the upstream Agent Zero framework outside Docker, then connect it to a dockerized instance via SSH and RFC.
- How to build local Docker images, configure ports, and link local `/a0` to the Docker container.
- How to fork the repository, follow code style, update documentation, and submit pull requests to the upstream project.

**How they relate to tbc-library docs**

- Use these upstream docs when a human asks **"how do I hack on Agent Zero itself?"** or **"how do I contribute upstream?"**, which usually means working directly with the Agent Zero repository rather than this tbc-library deployment.
- Use [TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md → The Engine: Agent Zero](TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md#the-engine-agent-zero) when you want the tbc-library perspective on respecting the engine and layering rather than modifying it in place.

As a helpdesk agent, you can point advanced users to `/a0/docs/development.md` and `/a0/docs/contribution.md` when the conversation shifts from "how do I use this deployment?" to "how do I extend or contribute to the core engine?".

---

## Tunnel feature (core Agent Zero)

- **Topic**: Exposing a local Agent Zero instance via Flaredantic tunnels
- **Upstream in-container path**: `/a0/docs/tunnel.md`
- **Host example**: `containers/a0-clarity/a0/docs/tunnel.md`

**What it covers**

- How the tunnel feature uses the Flaredantic library to create secure HTTPS tunnels to a local Agent Zero instance.
- How to enable the tunnel via the UI (External Services → Flare Tunnel) and obtain a shareable URL.
- Security considerations when exposing Agent Zero to the internet, including authentication and the scope of exposure.
- Troubleshooting steps for connectivity issues with tunnels.
- How to configure basic authentication for tunneled access, either via environment variables (`AUTH_LOGIN`, `AUTH_PASSWORD`) or UI settings.

**How it relates to tbc-library docs**

- Use `/a0/docs/tunnel.md` when a human asks **"how can I share my Agent Zero instance over the internet?"**.
- Combine it with [TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md → Docker Compose Orchestration](TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md#docker-compose-orchestration) and [TBC_LIBRARY_SELF_REVEALING_ORCHESTRATION.md](TBC_LIBRARY_SELF_REVEALING_ORCHESTRATION.md) when reasoning about which container is being exposed and how its ports and security are configured under tbc-library.

When reasoning as an agent, use `/a0/docs/tunnel.md` as the upstream guide to the tunneling feature and rely on tbc-library docs to reason about which specific container or deployment is safe and appropriate to expose.

---

## Example helpdesk workflows

Use the following patterns when acting as a helpdesk or operator agent who needs to know **where to look** in upstream `/a0/docs/...` and in the tbc-library knowledgebase.

### 1. "How do I install or update Agent Zero?"

- **Step 1: Upstream engine view**  
  - Read `/a0/docs/installation.md` and `/a0/docs/quickstart.md` via the **Installation and quick start** entry in this index.
- **Step 2: Layered deployment view**  
  - If the question involves this repository or containers such as `a0-myagent`, switch to [TBC_LIBRARY_INSTALLATION.md](TBC_LIBRARY_INSTALLATION.md) and the root `README.md` to explain how tbc-library clones, composes, and layers the upstream engine.

### 2. "How do I use the UI to do X?"

- **Step 1: Upstream UI behaviour**  
  - Use the **Usage guide and Web UI operations** entry (upstream `/a0/docs/usage.md`) to answer generic questions about action buttons, file attachments, multi-agent cooperation, prompt engineering, voice, KaTeX, file browser, and backup or restore.
- **Step 2: Layered features and prompts**  
  - If the question touches profiles, special tools, or narrative behaviour, add the tbc-library layer by consulting [TBC_LIBRARY_EXTENSIBILITY.md](TBC_LIBRARY_EXTENSIBILITY.md) and [TBC_LIBRARY_AGENT_REASONING.md](TBC_LIBRARY_AGENT_REASONING.md).

### 3. "Something is broken or slow, what should I check?"

- **Step 1: Upstream troubleshooting**  
  - Start with **Troubleshooting and FAQ** (upstream `/a0/docs/troubleshooting.md`) to see if the symptom matches a known upstream issue such as missing API keys, Docker not running, incorrect rate limits, or misconfigured models.
- **Step 2: Layered deployment troubleshooting**  
  - If the issue clearly involves containers, ports, or paths, move to [TBC_LIBRARY_INSTALLATION.md](TBC_LIBRARY_INSTALLATION.md) and [TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md](TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md) to reason about Docker Compose orchestration, bind mounts, and container naming.

### 4. "How do I connect another app or tool to this agent?"

- **Step 1: Engine-level connectivity**  
  - Use **Connectivity and external integrations** (upstream `/a0/docs/connectivity.md`) for External API endpoints, logs, file retrieval, MCP server endpoints, and A2A URLs.
  - Use **MCP setup and configuration** (upstream `/a0/docs/mcp_setup.md`) for `mcp_servers` and `tmp/settings.json` details.
- **Step 2: Deployment-level context**  
  - If the question involves which container is exposed or how paths map, add [TBC_LIBRARY_SELF_REVEALING_ORCHESTRATION.md](TBC_LIBRARY_SELF_REVEALING_ORCHESTRATION.md) and [TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md](TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md) to explain how this deployment projects `/containers/...` into `/a0/...` and how connectivity fits into the layered world.

### 5. "How do I extend or contribute to Agent Zero itself?"

- **Step 1: Upstream development and contribution**  
  - Use **Development and contribution** (upstream `/a0/docs/development.md` and `/a0/docs/contribution.md`) when a human wants to run the engine directly in an IDE, debug it, or open pull requests against the upstream repository.
- **Step 2: Layered philosophy**  
  - Use [TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md → The Engine: Agent Zero](TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md#the-engine-agent-zero) to reinforce that tbc-library treats Agent Zero as an engine and layers on top of it rather than modifying it directly.

When in doubt, first classify whether a question is **engine-level** (about how Agent Zero works in general) or **deployment-level** (about how this repository composes and extends it). Then start from the corresponding section in this index and bring in the matching tbc-library document for the layered view.
