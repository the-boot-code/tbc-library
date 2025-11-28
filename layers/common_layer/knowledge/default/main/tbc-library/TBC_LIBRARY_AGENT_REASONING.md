# Agent Reasoning and Perspectives in tbc-library

This document is a dedicated guide for **agents** (and advanced operators) for interpreting the tbc-library documentation, filesystem, and orchestration roles. It focuses on mental models and points of view rather than low-level configuration details.

> **Navigation**: [← Back to README](README.md) | [Installation →](TBC_LIBRARY_INSTALLATION.md)

## Config-First Rule

> **Always read configuration files as JSON before inferring from the filesystem.**
>
> - **Your runtime configuration** lives in `/a0/tmp/settings.json`. Read it to learn your `agent_memory_subdir`, `agent_profile`, `agent_knowledge_subdir`, model settings, and connectivity options.
> - **Your active profiles and prompt-includes** live in `/a0/tmp/system_control.json`.
> - **Your live `behaviour.md`** is at `/a0/memory/<agent_memory_subdir>/behaviour.md`, where `<agent_memory_subdir>` comes from `settings.json`.
>
> **Anti-pattern**: Do not scan the filesystem with commands like `find / -name behaviour.md` to locate your configuration or behaviour file. Such searches are slow, ambiguous when backups exist, and ignore the authoritative configuration.

This rule applies to reasoning about yourself and about other agents you may manage.

---

## How to reason about this documentation as an agent

When you (as an agent) work with this tbc-library documentation set, treat it as a **map** that describes both the host repository and your in-container environment. Use this file as your primary quick-reference for perception and roles.

1. **Determine your vantage point**  
   - Paths like `tbc-library/...`, `containers/...`, or `layers/...` **without** a leading `/` describe the **host repository**.  
   - Paths like `/a0/...`, `/layers/...`, `/agent_layer/...`, `/common_layer/...`, `/agent_orchestration`, or `/containers/...` describe the **inside of a container** created by tbc-library's Docker Compose orchestration.
2. **Decide who you are acting as**  
   - Are you reasoning as the **current self profile** inside one container, as a **manager of other profiles** in the same container, or as an **orchestrator of other containers/deployments** from the host?  
   - This distinction prevents confusion between "self" vs "managed" agents and between local vs external orchestration.
3. **Apply the Config-First Rule** (above) before inferring configuration from filesystem patterns.
4. **Use supporting docs for deep dives**  
   - Bind-mount mappings: [TBC_LIBRARY_SELF_REVEALING_ORCHESTRATION.md](TBC_LIBRARY_SELF_REVEALING_ORCHESTRATION.md#direct-agent-access-via-bind-mounts).  
   - Path tables and worked examples: [TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md](TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md#agent-perspectives-and-management).  
   - Dynamic profiles and reasoning modes: [TBC_LIBRARY_EXTENSIBILITY.md](TBC_LIBRARY_EXTENSIBILITY.md#dynamic-system-control-and-profiles).

By consistently applying this perception model, you can treat the documentation set as a stable conceptual map, even as details evolve.

## Vantage points: host, container, and multi-deployment

tbc-library is designed so that the same structures are visible from multiple vantage points. Keep these three in mind:

1. **Host repository vantage point** (outside any container)  
   - You see a clone of the `tbc-library` repository with top-level directories such as `containers/`, `layers/`, and `volumes/`.  
   - Each subdirectory under `containers/` (for example, `containers/a0-template`, `containers/a0-myagent`) describes an **agent container**: Compose file, `.env`, nginx config.  
   - Each subdirectory under `layers/` (for example, `layers/common_layer`, `layers/a0-template`) describes **shared** vs **agent-specific** state: prompts, tools, knowledge, profiles, and helper code.
2. **Inside-container vantage point** (from within one Agent Zero container)  
   - You see the same structures via bind mounts: host `containers/` and `layers/` appear as `/containers` and `/layers`; the container's own orchestration and layer directories appear as `/agent_orchestration`, `/agent_container`, and `/agent_layer`.  
   - Your live Agent Zero tree is under `/a0/...` (for example, `/a0/agents`, `/a0/prompts`, `/a0/knowledge`); many of these paths are views onto the same host directories. Within `/a0/knowledge`, the tbc-library documentation cluster normally lives under `/a0/knowledge/default/main/tbc-library`, and tbc-library solutions under `/a0/knowledge/default/solutions/tbc-library`.  
   - For how these mounts are wired, see [TBC_LIBRARY_SELF_REVEALING_ORCHESTRATION.md → Direct Agent Access via Bind Mounts](TBC_LIBRARY_SELF_REVEALING_ORCHESTRATION.md#direct-agent-access-via-bind-mounts) and [TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md → Docker Compose Orchestration](TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md#docker-compose-orchestration).
3. **Multi-deployment / external orchestrator vantage point** (from the host or another system)  
   - You may see multiple tbc-library clones (for example, `/opt/tbc-a/tbc-library`, `/opt/tbc-b/tbc-library`), each with its own `containers/` and `layers/` trees.  
   - From this perspective, you manage many containers and agents by operating on host paths; inside each container, `/containers` and `/layers` reflect only that deployment.  
   - For concrete multi-deployment orchestration examples, see [TBC_LIBRARY_SELF_REVEALING_ORCHESTRATION.md → Orchestration patterns (inside vs outside)](TBC_LIBRARY_SELF_REVEALING_ORCHESTRATION.md#orchestration-patterns-inside-vs-outside) and the worked examples in [TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md → Agent perspectives and management](TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md#agent-perspectives-and-management).

## Who you are acting as: self vs managed vs external

When you interpret prompts, tools, or filesystem state, be explicit about **which agent you are**:

1. **Self (this container's active agent)**  
   - Your canonical self-profile lives at `/a0/agents/${CONTAINER_NAME}` inside the container and mirrors `layers/${CONTAINER_NAME}/agents/${CONTAINER_NAME}` and `/agent_layer/agents/${CONTAINER_NAME}`.  
   - Treat `/a0/agents/${CONTAINER_NAME}` as the primary "who am I?" location in the usual single-agent-per-container pattern.
2. **Managed agents in the same container**  
   - Additional profiles under `/a0/agents` (for example, `default`, `developer`, `kairos`) may represent other identities managed by the same container.  
   - These can be activated or called as subordinates, but they are still part of this container's `/a0/agents` tree.
3. **Agents in other containers or deployments**  
   - Agent profiles under `/layers/<other-agent>/agents/<other-agent>` belong to other containers in the same deployment; they do **not** appear under `/a0/agents` for this container.  
   - From inside a container, you reason about these via `/layers/...` and `/containers/...`, not as local subordinates.

For detailed path tables, classification rules, and examples, use [TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md → Agent perspectives and management](TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md#agent-perspectives-and-management).

## Memory vantage and backup-safe files

As the active self inside a container, treat your memory paths as part of the same self-revealing architecture. This section is the **authoritative reference** for locating `behaviour.md` and memory roots; other docs link here.

### Locating your own memory root and behaviour file

**Recipe (config-first)**:

1. Read `/a0/tmp/settings.json` as JSON.
2. Extract the `agent_memory_subdir` field.
3. Your memory root is `/a0/memory/<agent_memory_subdir>`.
4. Your live `behaviour.md` is `/a0/memory/<agent_memory_subdir>/behaviour.md`.

**Host mirror**: The same directory is `layers/${CONTAINER_NAME}/memory/<agent_memory_subdir>` on the host.

**Editing behaviour**: When you are acting **inside your own container**, treat this as an operational rule: do **not** rewrite `behaviour.md` directly. Use the `behaviour_adjustment` tool (`agent.system.tool.behaviour.md`) so the framework can update this file safely, unless a human operator explicitly instructs you otherwise and you have confirmed that doing so is safe.

### Locating another agent's memory root and behaviour file (orchestrator view)

When you are acting as an orchestrator with access to `/containers` and `/layers`:

1. Identify the target agent's container name (for example, `a0-myagent`).
2. Read `/containers/<other>/a0/tmp/settings.json` (or host mirror `layers/<other>/tmp/settings.json`) as JSON.
3. Extract its `agent_memory_subdir` field.
4. The target agent's memory root is `layers/<other>/memory/<agent_memory_subdir>` on the host, and `/a0/memory/<agent_memory_subdir>` inside that agent's container.
5. Its live `behaviour.md` is at `<memory_root>/behaviour.md`.

Treat any modification of another agent's memory or `behaviour.md` as a high-impact orchestration action that must follow the documented tools and safety rules.

### Backup-safe files

Files under the memory root are runtime data you may safely **read** and, when instructed, **copy or snapshot**. Prefer copying to `/a0/work_dir` or host paths instead of editing in place unless documentation or a tool explicitly tells you to.

### Cloned agents and memory isolation

When a human or orchestrator runs `create_agent.sh` with a `memory_subdir` argument, the new agent gets its own memory root under `/a0/memory/<memory_subdir>`, separating its memory and `behaviour.md` from the source agent.

## Reasoning modes, profiles, and System Control

The tbc-library architecture separates **where you are** from **how you think and behave**:

- Narrative requirements such as "creative brainstorming mode" or "conservative audit mode" become concrete **profiles** (for example, workflow, reasoning, security, philosophy) managed by System Control; together these form the library's **dynamic profiles** capability.  
- These profiles live under `control_layer/profile_modules/...` on the host and are surfaced to you via prompts and tools.

As an agent, keep these guidelines in mind:

1. **Treat System Control as the source of truth for modes**  
   - Your active workflow, reasoning, philosophy, liminal thinking, and security modes are recorded in `/a0/tmp/system_control.json`.  
   - Tools like `workflow_profile_control`, `reasoning_profile_control`, and `prompt_include_control` are thin wrappers around this state.
2. **Use profiles to align behaviour with story intent**  
   - Narrative concepts (for example, "Finder", "creative gateway", "liminal thinking") map onto specific profile and feature configurations within these dynamic profiles.  
   - For how this realizes the "feedback machine" and Narrative Driven Development, see [TBC_LIBRARY_NARRATIVE_DRIVEN_DEVELOPMENT.md → The Feedback Machine](TBC_LIBRARY_NARRATIVE_DRIVEN_DEVELOPMENT.md#the-feedback-machine) and [TBC_LIBRARY_EXTENSIBILITY.md → Dynamic system control and profiles](TBC_LIBRARY_EXTENSIBILITY.md#dynamic-system-control-and-profiles).
3. **Distinguish knowledge from control**  
   - Knowledge trees (under `/a0/knowledge/...`) describe **what you know**.  
   - System Control profiles (under `control_layer/profile_modules/...` and `/a0/tmp/system_control.json`) describe **how you should act and reason right now**.

For concrete details on profile modules, tools, and example configurations that implement dynamic profiles, use [TBC_LIBRARY_EXTENSIBILITY.md → Dynamic system control and profiles](TBC_LIBRARY_EXTENSIBILITY.md#dynamic-system-control-and-profiles).

## Where to go next

Use this file as your starting point whenever you need to re-establish orientation. Key supporting docs:

| Topic | Document |
|-------|----------|
| Bind mounts and paths | [TBC_LIBRARY_SELF_REVEALING_ORCHESTRATION.md](TBC_LIBRARY_SELF_REVEALING_ORCHESTRATION.md) |
| Path tables and worked examples | [TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md](TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md) |
| Dynamic profiles and System Control | [TBC_LIBRARY_EXTENSIBILITY.md](TBC_LIBRARY_EXTENSIBILITY.md) |
| Upstream Agent Zero docs index | [TBC_LIBRARY_UPSTREAM_REFERENCES.md](TBC_LIBRARY_UPSTREAM_REFERENCES.md) |
