# Agent Reasoning and Perspectives in tbc-library

This document is a dedicated guide for **agents** (and advanced operators) for interpreting the tbc-library documentation, filesystem, and orchestration roles. It focuses on mental models and points of view rather than low-level configuration details.

> **Navigation**: [← Back to README](README.md) | [Installation →](TBC_LIBRARY_INSTALLATION.md)

## How to reason about this documentation as an agent

When you (as an agent) work with this tbc-library documentation set, treat it as a **map** that describes both the host repository and your in-container environment. Use this file as your primary quick-reference for perception and roles:

1. **Determine your vantage point**  
   - If you see paths like `tbc-library/...`, `containers/...`, or `layers/...` **without** a leading `/`, you are reasoning about the **host repository**.  
   - If you see paths like `/a0/...`, `/layers/...`, `/agent_layer/...`, `/common_layer/...`, `/agent_orchestration`, or `/containers/...`, you are reasoning about the **inside of a container** created by tbc-library's Docker Compose orchestration.
2. **Decide who you are acting as**  
   - Are you reasoning as the **current self profile** inside one container, as a **manager of other profiles** in the same container, or as an **orchestrator of other containers/deployments** from the host?  
   - This distinction is central to avoiding confusion between "self" vs "managed" agents and between local vs external orchestration.
3. **Use this guide as your mental model, and other docs as rulebooks**  
   - For concrete bind-mount mappings and path-level rules, use [TBC_LIBRARY_SELF_REVEALING_ORCHESTRATION.md → Direct Agent Access via Bind Mounts](TBC_LIBRARY_SELF_REVEALING_ORCHESTRATION.md#direct-agent-access-via-bind-mounts).  
   - For detailed host/container path relationships, self vs managed agents, and worked examples, use [TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md → Agent perspectives and management](TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md#agent-perspectives-and-management).  
   - For how narrative intent becomes reasoning modes and profiles, use [TBC_LIBRARY_EXTENSIBILITY.md → Dynamic system control and profiles](TBC_LIBRARY_EXTENSIBILITY.md#dynamic-system-control-and-profiles) together with [TBC_LIBRARY_NARRATIVE_DRIVEN_DEVELOPMENT.md → Narrative Driven Development: The Boot Code Storybook](TBC_LIBRARY_NARRATIVE_DRIVEN_DEVELOPMENT.md).

By consistently applying this perception model, you can treat the documentation set as a stable conceptual map, even as details evolve.

## Vantage points: host, container, and multi-deployment

tbc-library is designed so that the same structures are visible from multiple vantage points. Keep these three in mind:

1. **Host repository vantage point** (outside any container)  
   - You see a clone of the `tbc-library` repository with top-level directories such as `containers/`, `layers/`, and `volumes/`.  
   - Each subdirectory under `containers/` (for example, `containers/a0-template`, `containers/a0-myagent`) describes an **agent container**: Compose file, `.env`, nginx config.  
   - Each subdirectory under `layers/` (for example, `layers/common`, `layers/a0-template`) describes **shared** vs **agent-specific** state: prompts, tools, knowledge, profiles, and helper code.
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

As the active self inside a container, treat your memory paths as part of the same self-revealing architecture:

- **Memory root**: Your primary memory root is `/a0/memory/<agent_memory_subdir>`. The value of `agent_memory_subdir` comes from `/a0/tmp/settings.json` (cloned from `layers/${CONTAINER_NAME}/tmp/settings.json` on the host and optionally updated by `create_agent.sh` via its `memory_subdir` argument). The same directory is visible on the host as `layers/${CONTAINER_NAME}/memory/<agent_memory_subdir>`.
- **Safe to read and back up**: Treat files under this memory root as runtime data you may safely **read** and, when instructed, **copy or snapshot** (for example, backing up `layers/${CONTAINER_NAME}/memory/<agent_memory_subdir>` or `/a0/memory/<agent_memory_subdir>`). Prefer copying to `/a0/work_dir` or host paths instead of editing memory files in place unless the documentation or a tool explicitly tells you to.
 - **Behaviour rules**: Behaviour rules are loaded from a memory-backed `behaviour.md` file located at `/a0/memory/<agent_memory_subdir>/behaviour.md`; see [TBC_LIBRARY_EXTENSIBILITY.md → System prompt staging pipeline](TBC_LIBRARY_EXTENSIBILITY.md#system-prompt-staging-pipeline). Do **not** rewrite `behaviour.md` directly. Use the `behaviour_adjustment` tool (`agent.system.tool.behaviour.md`) so the framework can update this file safely.
 - **How to locate your own `behaviour.md` (preferred)**: To identify your live behaviour file, (1) read `/a0/tmp/settings.json`, (2) find the `agent_memory_subdir` value, and (3) combine it with `/a0/memory/<agent_memory_subdir>/behaviour.md`. Treat other `behaviour.md` files you may find on the filesystem as backups or historical copies unless the documentation for this deployment explicitly says otherwise.
 - **Cloned agents and memory isolation**: When a human or orchestrator runs `create_agent.sh` with a `memory_subdir` argument, the new agent gets its own memory root under `/a0/memory/<memory_subdir>`, separating its memory from the source agent. For concrete patterns, see [TBC_LIBRARY_INSTALLATION.md](TBC_LIBRARY_INSTALLATION.md) and `create_agent.md` in this repository.
 - **Other agents' memory and behaviour (orchestrator view)**: When you are acting as an orchestrator with access to `/containers` and `/layers`, you can locate another agent's memory root and behaviour file by (1) identifying that agent's container name, (2) reading its `/containers/<other>/a0/tmp/settings.json` (or the host mirror) to learn its `agent_memory_subdir` value, and then (3) combining that value with the known mappings to find `/containers/<other>/layers/<other>/memory/<agent_memory_subdir>` on the host and `/a0/memory/<agent_memory_subdir>/behaviour.md` inside that agent's own container. Treat any modification of another agent's memory or `behaviour.md` as a high-impact orchestration action that must follow the documented tools and safety rules for that deployment.

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

Use this file as your starting point whenever you need to re-establish orientation. Then follow these references for deeper knowledge:

- [README.md → Reading as a human or an agent](README.md#reading-as-a-human-or-an-agent) for how humans and agents should approach the documentation set.  
- [TBC_LIBRARY_SELF_REVEALING_ORCHESTRATION.md → Direct Agent Access via Bind Mounts](TBC_LIBRARY_SELF_REVEALING_ORCHESTRATION.md#direct-agent-access-via-bind-mounts) for a detailed view of bind mounts and self-revealing orchestration.  
- [TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md → Agent perspectives and management](TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md#agent-perspectives-and-management) for worked examples of self vs managed agents, symlinks, and host/container path mappings.  
- [TBC_LIBRARY_EXTENSIBILITY.md → Dynamic system control and profiles](TBC_LIBRARY_EXTENSIBILITY.md#dynamic-system-control-and-profiles) for how modes, profiles, and tools translate narrative requirements into runtime behaviour.  
- [TBC_LIBRARY_NARRATIVE_DRIVEN_DEVELOPMENT.md → Narrative Driven Development: The Boot Code Storybook](TBC_LIBRARY_NARRATIVE_DRIVEN_DEVELOPMENT.md) for the story context that motivates these structures and modes.  
- [TBC_LIBRARY_UPSTREAM_REFERENCES.md → Upstream Agent Zero documentation references](TBC_LIBRARY_UPSTREAM_REFERENCES.md) for an index of `/a0/docs` topics provided by the Agent Zero engine and how they relate to this layered deployment.
