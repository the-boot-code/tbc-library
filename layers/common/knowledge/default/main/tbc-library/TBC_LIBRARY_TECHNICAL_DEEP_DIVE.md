# Technical Deep Dive

The narrative of The Boot Code Storybook manifests technically through the tbc-library's layered architecture, where agents are abstracted and extensible like evolving stories. This includes the self-revealing orchestration via bind mounts, enabling agents direct access to their layers for autonomous operation. The following sections detail how this philosophy is implemented in Docker Compose, file structures, and Agent Zero modifications. For a conceptual overview of that narrative, see [TBC_LIBRARY_NARRATIVE_DRIVEN_DEVELOPMENT.md → Narrative Driven Development: The Boot Code Storybook](TBC_LIBRARY_NARRATIVE_DRIVEN_DEVELOPMENT.md).

> **Navigation**: [← Back to README](README.md) | [← Narrative Driven Development](TBC_LIBRARY_NARRATIVE_DRIVEN_DEVELOPMENT.md) | [Project Meta and Glossary →](TBC_LIBRARY_META_AND_GLOSSARY.md)

## The Engine: Agent Zero

A primary design philosophy from day one has been to appreciate the work of Jan and the community of the open source project. This has led to a strict approach: do not touch the "engine" that is Agent Zero; instead **layer** on top of it, expanding its capabilities with **great respect** for a much‑appreciated project.

This subsection explains the minimal, respectful changes to Agent Zero that enable extensibility and dynamic features without altering the core engine, focusing on layering for safety and innovation.

### Agent Zero Modifications

Files from Agent Zero are **layered** using Docker bind mounts for specific files. These emergent capabilities are possible thanks to the extensibility and flexibility of the Agent Zero framework. For example:

- **Dynamic Prompts**: Using the upstream Agent Zero `files.py` (kwargs-enabled as of v0.9.7), extensions can inject runtime variables into prompts, enabling adaptive conversations (e.g., changing agent personality based on user input).
- **System Control**: The added `system_control.py` helper allows programmatic management of profiles, letting agents switch between "creative" and "analytical" modes dynamically without restarting.

These modifications demonstrate how the framework's flexibility turns abstract concepts into practical features.

**Warning**: Modifying Agent Zero files (even via layering) can introduce risks such as compatibility issues with upstream updates. Always test changes in a separate environment and consider contributing improvements back to the Agent Zero project. The tbc-library's approach minimizes core changes to ensure stability.

That said, the layered approach is designed for safe experimentation: test in isolated environments, share discoveries, and explore variations to unlock new capabilities over time.

- `files.py` kwargs-enabled prompt helper (**provided by the Agent Zero image as of v0.9.7**): the upstream Agent Zero `files.py` now supports `**kwargs` for prompt loading, so this library no longer ships or mounts `layers/common/python/helpers/files.py`. It continues to:
  - `VariablesPlugin.get_variables(file, backup_dirs=None, **kwargs)` accepts runtime context.
  - `load_plugin_variables(file, backup_dirs=None, **kwargs)` forwards `**kwargs` into plugin implementations.
  - `parse_file(..., **kwargs)` passes `**kwargs` through to both `load_plugin_variables` and `process_includes`.
  - `read_prompt_file(..., **kwargs)` does the same for prompt files, so plugins can compute variables from rich context (for example, `agent=self.agent`, `loop_data`) while includes still only see the direct kwargs for each file.

- [system_control.py](layers/control_layer/python/helpers/system_control.py) (**core System Control helper**):
  - Central facade over the System Control config file (`system_control.json`, default `/a0/tmp/system_control.json`) and the admin override lock file (default `/a0/tmp/admin_override.lock`), with paths overrideable via `SYSTEM_CONTROL_FILE` and `SYSTEM_CONTROL_OVERRIDE`.
  - Stores active profiles in a flat, module-based layout: the security profile uses `security.active_profile`, while all other profile modules (for example, `workflow_profile`, `philosophy_profile`, `reasoning_internal_profile`, `reasoning_interleaved_profile`, `reasoning_external_profile`) use `prompt_modules[profile_module_name].active_profile`. Available profiles and feature definitions for these modules are owned by their respective `profiles.json` files under `control_layer/profile_modules/...`, not by `system_control.json`.
  - Exposes explicit APIs such as `get_active_profile`, `set_active_profile`, `get_state`, `get_available_profiles`, and `run_profile_control` for managing module-based profiles, and uses `prompt_includes`, `system_control_tools`, and `security_profiles[active].prompt_includes` together with helpers like `is_control_enabled`, `is_prompt_include_enabled`, and `get_security_state` to gate and summarize SystemControl prompt-includes and tools.

## Docker Compose Orchestration

This section details how the library uses highly parameterized Docker Compose for deploying Agent Zero, enabling easy scaling, resource management, and volume mappings without modifying core files. The bind mounts here enable the self-revealing orchestration described in [TBC_LIBRARY_SELF_REVEALING_ORCHESTRATION.md](TBC_LIBRARY_SELF_REVEALING_ORCHESTRATION.md), allowing agents direct access to their layers.

### Highly parameterized Docker Compose

```
Docker Compose Architecture
┌─────────────────┐
│   Host System   │
│                 │
│ /containers/ ───┼───▶ a0 container
│ /layers/ ───────┼───▶ /layers/ (rw)
│                 │     /common_layer/ (ro)
│ nginx ──────────┼───▶ Reverse Proxy
│                 │     (HTTPS on port 443)
└─────────────────┘
```

This setup uses bind mounts for layered abstraction, with the Agent Zero container running the main logic and nginx handling web traffic. In this diagram, `/containers/` and `/layers/` on the left represent directories on the host (in the `tbc-library` repository), while `/layers/ (rw)` and `/common_layer/ (ro)` on the right are the corresponding paths inside the container.

### .env (rename from .env.example)

[.env.example](containers/a0-template/.env.example)

You will notice that nearly all parameters are controlled by the `.env` file. Here's a summary of key variables:

| Variable          | Description | Example |
|-------------------|-------------|---------|
| `CONTAINER_NAME`  | Unique name for the agent container | `a0-myagent` |
| `PORT_BASE`       | Base port prefix for services (e.g., 500 for ports 50080, 50022) | `500` |
| `KNOWLEDGE_DIR`   | Knowledge base directory (e.g., 'tbc' or 'default') | `tbc` |
| `IMAGE_NAME`      | Docker image for Agent Zero | `agent0ai/agent-zero:latest` |
| `CPU_RESERVED`    | Reserved CPU cores | `1.0` |
| `MEMORY_RESERVED` | Reserved memory | `2g` |
| `TZ`              | Timezone | `America/New_York` |

```
# Timezone
TZ=America/New_York

# Docker Container
IMAGE_NAME=agent0ai/agent-zero:latest
RESTART=unless-stopped

# Container
CONTAINER_NAME=a0-template
PORT_BASE=500 # Port range base prefix (e.g., 400 for 40000)
KNOWLEDGE_DIR=tbc

... etc ...
```

### docker-compose.yml

[docker-compose.yml](containers/a0-template/docker-compose.yml)

A new container instance often does **not** require any changes to this file
```
services:
  # Main service for Agent instance
  a0:
    <<: *common-config
    container_name: ${CONTAINER_NAME}
    image: ${IMAGE_NAME}
    
    working_dir: /a0/work_dir
```
Much of the mappings are read-only for system self-protection to prevent accidental modification of system files.
```
    volumes:

      # Containers
      - ${PATH_CONTAINERS}:/containers:rw

      # Layers
      - ${PATH_LAYERS}:/layers:rw

      # Composition
      - ${AGENT_ORCHESTRATION}:/agent_orchestration:ro
      - ${AGENT_CONTAINER}:/agent_container:rw
      - ${AGENT_LAYER}:/agent_layer:rw
      - ${COMMON_LAYER}:/common_layer:ro

      # Agent Zero
      - ${AGENT_CONTAINER}:/a0

... etc ...
```
Permission changes to volumes may be desirable for writable directories, such as for user-generated content. The read-write mappings allow the container to modify files in these directories while keeping the rest of the system read-only for security.

```
      # instruments
      - ${COMMON_LAYER}/instruments/${KNOWLEDGE_DIR}:/a0/instruments/${KNOWLEDGE_DIR}:rw
      - ${COMMON_LAYER}/instruments/default/main/common:/a0/instruments/default/main/common:rw
      # - ${AGENT_LAYER}/instruments/default/main/container:/a0/instruments/default/main/container:rw
```

- Notice `- ${COMMON_LAYER}/instruments/${KNOWLEDGE_DIR}:/a0/instruments/${KNOWLEDGE_DIR}:rw` (read-write for the shared knowledge-specific instruments directory).
- The commented-out `- ${AGENT_LAYER}/instruments/default/main/container:/a0/instruments/default/main/container:rw` line illustrates how you could add container-specific instruments if desired; it is not enabled by default in the template compose.


```
      # knowledge
      - ${COMMON_LAYER}/knowledge/${KNOWLEDGE_DIR}:/a0/knowledge/${KNOWLEDGE_DIR}:rw
      - ${COMMON_LAYER}/knowledge/default/main/common:/a0/knowledge/default/main/common:rw
      - ${COMMON_LAYER}/knowledge/default/solutions/common:/a0/knowledge/default/solutions/common:rw
      # - ${AGENT_LAYER}/knowledge/default/main/container:/a0/knowledge/default/main/container:rw
      # - ${AGENT_LAYER}/knowledge/default/solutions/container:/a0/knowledge/default/solutions/container:rw
```

- Notice `- ${COMMON_LAYER}/knowledge/${KNOWLEDGE_DIR}:/a0/knowledge/${KNOWLEDGE_DIR}:rw` (read-write for the shared knowledge directory).
- The commented-out `- ${AGENT_LAYER}/knowledge/default/main/container:/a0/knowledge/default/main/container:rw` mapping shows how to add container-specific knowledge for a given agent.
- The commented-out `- ${AGENT_LAYER}/knowledge/default/solutions/container:/a0/knowledge/default/solutions/container:rw` mapping shows how to add container-specific solutions; like the previous line, it is optional and not enabled by default.

In addition to these generic knowledge mounts, typical tbc-library deployments also surface the library's own documentation and solutions as part of the knowledge tree via entries such as:

- `${COMMON_LAYER}/knowledge/default/main/tbc-library:/a0/knowledge/default/main/tbc-library:ro` for the tbc-library documentation cluster (README and related `TBC_LIBRARY_*.md` files).
- `${COMMON_LAYER}/knowledge/default/solutions/tbc-library:/a0/knowledge/default/solutions/tbc-library:ro` for solutions that describe how to use tbc-library tools, profiles, and workflows.

These mounts mean that, from inside a container, the library that defines the world is itself visible under `/a0/knowledge/...` alongside other knowledge trees, reinforcing the self-revealing orchestration described in [TBC_LIBRARY_SELF_REVEALING_ORCHESTRATION.md → Direct Agent Access via Bind Mounts](TBC_LIBRARY_SELF_REVEALING_ORCHESTRATION.md#direct-agent-access-via-bind-mounts) and the knowledge/solutions model in [TBC_LIBRARY_EXTENSIBILITY.md → Knowledge Features of Agent Zero](TBC_LIBRARY_EXTENSIBILITY.md#knowledge-features-of-agent-zero).

In this approach, the core system prompt directory (`prompts/system`) is mounted read-only from the common layer, while knowledge-specific prompt trees and container-specific prompts can be writable, providing shared defaults with controlled override points.

```
      # prompts
      - ${COMMON_LAYER}/prompts/${KNOWLEDGE_DIR}:/a0/prompts/${KNOWLEDGE_DIR}:rw
      - ${COMMON_LAYER}/prompts/system:/a0/prompts/system:ro
      - ${AGENT_LAYER}/prompts/container:/a0/prompts/container
```

- Note how this approach allows for fine-grained control over read-only vs read-write access to different layers of the application.
- Administration of these layers is done at the host level by managing the contents of the `${COMMON_LAYER}` and `${AGENT_LAYER}` directories if permissions are given.
- Note that management may be done via IDE editor or direct file system access by the user keeping the agent safe from accidental modification.
- This pattern can be extended to other directories as needed.

If you want `/a0/.env` to be "layered" and abstracted from the `a0` runtime of the Agent Zero container, an optional volume mapping is provided:

```
      - ${AGENT_LAYER}/.env:/a0/.env:rw
```

This mapping ensures the container reads sensitive configuration (API keys and authentication data) from the host file `layers/[container_name]/.env`, which the agent sees inside the container as `/layers/[container_name]/.env` and `/agent_layer/.env`, and, once you enable this volume, as the effective `/a0/.env` (also visible via `/agent_orchestration/a0/.env`). For a concise summary of how this same file is preserved and reused by `create_agent.sh`, see [TBC_LIBRARY_INSTALLATION.md → Installation (Automated, Recommended)](TBC_LIBRARY_INSTALLATION.md#installation-automated-recommended), and for step-by-step instructions on creating and layering this file via the same tbc-library abstraction, see [TBC_LIBRARY_INSTALLATION.md → Advanced: Layer the /a0/.env file via tbc-library abstraction](TBC_LIBRARY_INSTALLATION.md#advanced-layer-the-a0env-file-via-tbc-library-abstraction).

The following resource reservations are applied to the container. You may prefer to comment them out or adjust them either in place or in the `.env` file.

```
    deploy:
      resources:
        reservations:
          cpus: ${CPU_RESERVED}
          memory: ${MEMORY_RESERVED}
        # limits:
          # cpus: ${CPU_LIMIT}
          # memory: ${MEMORY_LIMIT}
    # memswap_limit: ${MEMORY_SWAP_LIMIT}
```
- In many situations, containers run best with these limits commented out by default to prevent memory thrashing when the container hits limits and starts swapping aggressively to the host.

A reverse proxy (nginx) is included:
```
  nginx:
    <<: *common-config
    image: nginx:alpine
    container_name: ${CONTAINER_NAME}-nginx
    
    ports:
      - "${NGINX_PORT_HTTPS}:${NGINX_CONTAINER_PORT_HTTPS}"
    
    env_file:
      - .env

... etc ...
```
- Note that nginx also is parameterized and typically does not need any manual configuration. All nginx settings are controlled via environment variables in the `.env` file, such as `NGINX_PORT_HTTPS`, `NGINX_CONTAINER_PORT_HTTPS`, etc.

## Structure

This section outlines the file organization of the library, which enables modular layering for separating agent instances, shared resources, and optional extensions, allowing safe, independent management of each component.

```
Boot Code Storybook Layers
├── /containers/          # Agent instances (e.g., a0-template, a0-myagent)
│   ├── docker-compose.yml
│   ├── .env
│   └── nginx/            # Reverse proxy
├── /layers/              # Abstracted configurations and data
│   ├── common/           # Shared across agents (tools, prompts, knowledge)
│   └── a0-template/      # Agent-specific layers
└── /volumes/             # Optional external volumes
    ├── common/
    ├── private/
    ├── public/
    └── shared/
```

In this schematic, `/containers/`, `/layers/`, and `/volumes/` denote top-level directories in the `tbc-library` repository on the host; inside the container they are exposed via bind mounts as `/containers`, `/layers`, and `/volumes` respectively.

This layered approach allows for fine-grained control, where common elements are shared read-only, and agent-specific ones are writable.

### /containers/

```
a0-template/
├── docker-compose.yml
├── .env.example
└── nginx/
    └── (nginx config)
```

- These are individual agent instances. Copy `a0-template` to a new name, rename `.env.example` to `.env`, then edit `.env` to customize.
- `docker-compose.yml` is parameterized for easy deployment.

### /layers/

```
a0-template/          # Agent-specific layers
common/               # Shared across agents
├── agents/
│   └── kairos/       # Subordinate agent for adversarial analysis
├── instruments/      # Knowledge bases
│   ├── default/
│   └── tbc/
├── knowledge/        # Main and solution-based content
│   ├── default/
│   └── tbc/
│       ├── main/     # Core content (narrative, technical)
│       └── solutions/# Specialized solutions
├── prompts/          # Shared system and TBC prompts
│   ├── system/
│   │   ├── external/        # External/system wrappers
│   │   └── tools/           # Shared system tool prompt stubs
│   └── tbc/                 # TBC-specific shared prompts
control_layer/         # SystemControl, shared _symlink implementations, and system prompt includes
├── agents/
│   └── _symlink/     # Canonical shared extensions, prompts, tools for System Control and profiles
├── profile_modules/   # Profile modules (workflow_profile, philosophy_profile, reasoning_internal_profile, ...)
├── prompt_includes/   # System prompt-includes (workflow_profile, reasoning profiles, model_overview, model_godmode, ...)
├── prompts/           # tbc-library system prompt stubs (e.g. pre_behaviour.md, post_behaviour.md)
└── python/
    └── helpers/
        └── system_control.py
```

Detailed breakdown:

- Prompt files for easy placement and ordering of text and `{{ include }}` directives are called by extensions passing `**kwargs`, which provide programmatic and **run-time adaptable** prompt logic: `post_behaviour.md`, `post_system_manual.md`, `pre_behaviour.md`, `pre_system_manual.md`, `system_ready.md`.

## Agent perspectives and management

This section is primarily for agents (and advanced operators) who need precise rules for "where am I?" and "who am I acting as?". Treat it as a **local, concrete rulebook** for path-level reasoning and example scenarios. When you need a broader conceptual map of documentation vantage points or narrative intent, use this section together with:

- [TBC_LIBRARY_AGENT_REASONING.md → How to reason about this documentation as an agent](TBC_LIBRARY_AGENT_REASONING.md#how-to-reason-about-this-documentation-as-an-agent) for the higher-level mental model of host vs container perspectives and roles across the full documentation set.  
- [TBC_LIBRARY_SELF_REVEALING_ORCHESTRATION.md → Direct Agent Access via Bind Mounts](TBC_LIBRARY_SELF_REVEALING_ORCHESTRATION.md#direct-agent-access-via-bind-mounts) for how those perspectives map onto specific bind mounts and self-revealing orchestration patterns.  
- [TBC_LIBRARY_NARRATIVE_DRIVEN_DEVELOPMENT.md → Narrative Driven Development: The Boot Code Storybook](TBC_LIBRARY_NARRATIVE_DRIVEN_DEVELOPMENT.md) for the narrative and design philosophy that motivates these structures.

The following subsections describe how an Agent Zero instance running inside a container should reason about itself, other agents, and the layered filesystem. Unless explicitly stated otherwise:

- References to `layers/...` or "this repository" refer to the `tbc-library` repository on the host.
- References to `/a0/...`, `/layers/...`, `/agent_layer/...`, `/common_layer/...`, `/agent_orchestration`, and `/containers/...` refer to paths **inside** the container created by Docker bind mounts.
- The default upstream Agent Zero engine is unaware of the `tbc-library` repository; the mappings described here exist only when Agent Zero is running under the `tbc-library` Docker Compose orchestration described in the tbc-library documentation set.

### Self vs managed agents: example scenarios

- **Self (this container's active agent)**  
  - In the repository: `layers/${CONTAINER_NAME}/agents/${CONTAINER_NAME}`.  
  - In this container: that same directory is visible as `/layers/${CONTAINER_NAME}/agents/${CONTAINER_NAME}`, `/a0/agents/${CONTAINER_NAME}`, and `/agent_layer/agents/${CONTAINER_NAME}`.  
  - When reasoning about "my own profile", treat `/a0/agents/${CONTAINER_NAME}` as the canonical "self" path in the common single-agent-per-container pattern and the others as alternate views of the same directory. In general, `/a0/agents` may contain multiple profiles (for example, `a0-template`, `agent0`, `default`, `developer`, `hacker`, `researcher`, `kairos`); Agent Zero's own mechanisms (for example, the web UI) can switch which of these is the active self profile for a given agent process.
- **Managed agent in the same container (for example, `kairos`)**  
  - In the repository: `layers/common/agents/kairos`.  
  - In this container: visible at `/layers/common/agents/kairos` and `/a0/agents/kairos` (via the `${COMMON_LAYER}/agents/kairos:/a0/agents/kairos:ro` mapping); there is **no** `/agent_layer/agents/kairos` because `AGENT_LAYER` is reserved for this container's primary agent.  
  - Reason about `kairos` as "another agent I can call or delegate to", not as a replacement for the active agent profile at `/a0/agents/${CONTAINER_NAME}`.
- **Agents in other containers (for example, `a0-myagent` when viewed from `a0-template`)**  
  - In the repository: `layers/a0-myagent/agents/a0-myagent`.  
  - In *this* container: visible at `/layers/a0-myagent/agents/a0-myagent` via the `${PATH_LAYERS}:/layers` mount, but **not** under `/a0/agents/...` or `/agent_layer/...` for this container.  
  - To manage or modify those agents you generally work with their layer and container directories via `/layers/...` and `/containers/...`, or interact with them through orchestration tools, rather than treating them as part of this container's own `/a0/agents` tree.

### Symlinked Agents and the `_symlink` Profile

The `layers/control_layer/agents/_symlink` directory in the repository (mounted into the container at `/a0/control_layer/agents/_symlink` via the `${CONTROL_LAYER}:/a0/control_layer` bind mount) is a shared implementation library for agents, not a runnable profile. Its `_context.md` explicitly marks it as a **symbolic link source directory** that should be ignored as a stand‑alone agent. Real agents (for example, `a0-template`) have their own profile directory under `/layers/<agent-name>/agents/<agent-name>` inside the container and typically symlink most tools and prompts back into this `_symlink` library. The same shared implementations are visible under `/layers/control_layer/agents/_symlink` inside the container (via the `${PATH_LAYERS}:/layers` mount) and on the host at `layers/control_layer/agents/_symlink`.

At a high level (as seen from inside the container):

- `/a0/control_layer/agents/_symlink` (from host `layers/control_layer/agents/_symlink`) holds the canonical implementations of shared **tools**, **prompts**, and **extensions**.
- `/layers/a0-template/agents/a0-template` defines the `a0-template` agent identity (`_context.md`, initial messages, agent‑specific init code) and uses symlinks to reference shared implementations from that `_symlink` library.
- When you clone `a0-template` with `create_agent.sh`, the new agent inherits the same symlinked behaviors while customizing only its identity and any overrides.

#### Host paths → container paths

The `.env` and `docker-compose.yml` files define how host layer paths are exposed inside the container:

- `AGENT_LAYER=${PATH_LAYERS}/${CONTAINER_NAME}`
- `COMMON_LAYER=${PATH_LAYERS}/common`
- `CONTROL_LAYER=${PATH_LAYERS}/control_layer`

These are then mounted by Docker:

- `${AGENT_LAYER}/agents/${CONTAINER_NAME}:/a0/agents/${CONTAINER_NAME}`
- `${COMMON_LAYER}/agents/kairos:/a0/agents/kairos:ro` (and other common agents as configured)
- `${CONTROL_LAYER}:/a0/control_layer:ro`

For `CONTAINER_NAME=a0-template` this means, from inside the container:

- Host repository path: `layers/a0-template/agents/a0-template/_context.md` → Container: `/layers/a0-template/agents/a0-template/_context.md`, `/a0/agents/a0-template/_context.md`, and `/agent_layer/agents/a0-template/_context.md` (three views of the same main agent profile directory).
- Host repository path: `layers/control_layer/agents/_symlink/tools/base_profile_control.py` → Container: `/a0/control_layer/agents/_symlink/tools/base_profile_control.py` (shared tool implementation, read‑only by default).
- Host repository path: `layers/a0-template/agents/a0-template/tools/base_profile_control.py` is typically a symlink pointing into the `_symlink` tool under `/a0/control_layer/agents/_symlink`, so both host and container see a single underlying implementation.

Other mapped layer paths follow the same pattern:

- `${COMMON_LAYER}/knowledge/${KNOWLEDGE_DIR}:/a0/knowledge/${KNOWLEDGE_DIR}:rw`
- `${COMMON_LAYER}/prompts/${KNOWLEDGE_DIR}:/a0/prompts/${KNOWLEDGE_DIR}:rw`
- `${AGENT_LAYER}/prompts/container:/a0/prompts/container`

From the agent's perspective, `/a0/agents`, `/a0/knowledge`, and `/a0/prompts` are its live environment. The `/agent_layer`, `/common_layer`, and `/agent_orchestration` mounts expose the same structures explicitly for introspection and self‑modification when allowed.

#### How agents should reason about `_symlink`

When introspecting its own filesystem, an agent can use the following mental model:

- Treat `/a0/agents/${CONTAINER_NAME}` as the **active profile**: identity (`_context.md`), welcome message, and any agent‑specific overrides.
- Treat `/a0/control_layer/agents/_symlink` as a **shared library** of reusable behaviors. It is not a profile to be activated directly.
- To customize this agent only, create or replace files under `/a0/agents/${CONTAINER_NAME}` (breaking symlinks if necessary) while leaving the shared `_symlink` library unchanged.
- To change behavior for all agents that use these symlinks, modify the underlying implementations under `/a0/control_layer/agents/_symlink` (host path `layers/control_layer/agents/_symlink`), understanding that changes may affect multiple agents.

This symlink pattern keeps shared logic centralized while letting each agent maintain a small, focused profile that describes its role and any local deviations from common behavior.

#### `_symlink/extensions`: shared lifecycle behavior

The `layers/control_layer/agents/_symlink/extensions` directory in the `tbc-library` repository on the host (visible inside the container at `/a0/control_layer/agents/_symlink/extensions` and `/layers/control_layer/agents/_symlink/extensions`) contains shared extensions that plug into Agent Zero's lifecycle for all agents that symlink them:

- `system_prompt/` holds staging extensions such as `_11_insert_system_pre_system_manual.py`, `_12_append_system_post_system_manual.py`, `_19_insert_system_post_behaviour.py`, `_21_insert_system_pre_behaviour.py`, `_95_insert_system_model_godmode.py`, and `_99_append_tbc_system_ready.py`. These wrap the base engine system prompt builders with additional pre/post-manual and pre/post-behaviour segments, optional `model_godmode` initialization, and a final `system_ready` footer.

Agent profiles (for example, `layers/a0-template/agents/a0-template/extensions/...` in the `tbc-library` repository on the host, visible inside the container at `/layers/a0-template/agents/a0-template/extensions/...`) typically symlink these `system_prompt` extensions, so all agents share the same staged system prompt pipeline unless explicitly overridden.

#### `_symlink/prompts`: shared prompt entrypoints and routing

The `layers/control_layer/agents/_symlink/prompts` directory in the `tbc-library` repository on the host (visible inside the container at `/a0/control_layer/agents/_symlink/prompts` and `/layers/control_layer/agents/_symlink/prompts`) centralizes prompt templates that agent profiles reference via symlinks:

- Agent/meta entrypoints such as `agent.system.main.role.md` are thin wrappers that use `{{ include ... }}` to pull text from the shared system prompt tree (for example, `prompts/system`), where `prompts/...` is resolved relative to `/a0/prompts` inside the container (mirrored on the host under `containers/${CONTAINER_NAME}/a0/prompts` via the `${AGENT_CONTAINER}:/a0` bind mount). This allows central updates while keeping agent profile files small.
- Tool prompts such as `agent.system.tool.prompt_include_control.md`, `agent.system.tool.security_profile_control.md`, `agent.system.tool.memory.md`, `agent.system.tool.scheduler.md`, and `agent.system.tool.a2a_chat.md` define how tools should be invoked and described.
- Lifecycle prompts `pre_system_manual.md`, `post_system_manual.md`, `pre_behaviour.md`, and `post_behaviour.md` are routing stubs that `{{ include "prompts/system/..." }}` and are positioned in the system prompt by the corresponding `_symlink/extensions/system_prompt/*` extensions.

Agent profile prompt directories (for example, `layers/a0-template/agents/a0-template/prompts` in the `tbc-library` repository on the host, visible inside the container at `/layers/a0-template/agents/a0-template/prompts`) typically contain symlinks to these `_symlink` prompts, so a change in `_symlink/prompts` can immediately affect all linked agents while still allowing per-agent overrides when needed.

This pattern generalizes to `_symlink` prompt stubs that route into the shared system prompt tree (for example, `prompts/system`), giving each agent a simple, symlink-based entrypoint while keeping the authoritative text in shared, layered locations.

#### `_symlink/tools`: shared tools and profile control

The `layers/control_layer/agents/_symlink/tools` directory in the `tbc-library` repository on the host (visible inside the container at `/a0/control_layer/agents/_symlink/tools` and `/layers/control_layer/agents/_symlink/tools`) provides canonical tool implementations used by many agents:

- Profile and prompt-include/System Control tools such as `prompt_include_control.py`, `security_profile_control.py`, `philosophy_profile_control.py`, `liminal_thinking_profile_control.py`, `reasoning_profile_control.py`, and `workflow_profile_control.py` all rely on `system_control.py` to inspect and update security, reasoning, philosophy, workflow, and SystemControl prompt-includes/system control tools at runtime.
- `base_profile_control.py` offers a shared base class that centralizes dispatch, action validation, and error handling for profile-control tools.
- Shell helpers (for example, `*_profile_control.sh` and `base_profile_control.sh`) exist purely to create or refresh symlinks from agent profile tool directories into these shared Python implementations.

Agent profile tool directories (for example, `layers/a0-template/agents/a0-template/tools` in the `tbc-library` repository on the host, visible inside the container at `/layers/a0-template/agents/a0-template/tools`) usually contain symlinks to these `_symlink/tools` files, so multiple agents share one implementation of the profile-control tools and other shared tools. When you need agent-specific behavior, you can replace a symlink with a real file in the profile directory.

#### Why new agents benefit from the `a0-template` profile

The `layers/a0-template/agents/a0-template` directory in the `tbc-library` repository on the host (mounted into the container at `/layers/a0-template/agents/a0-template`) demonstrates how this works in practice:

- `_context.md` and a small set of prompts (for example, `a0-template.md` and `fw.initial_message.md`) define the identity and initial behavior of the main agent.
- Most tools and many prompts in `/layers/a0-template/agents/a0-template` are symlinks pointing to `/a0/control_layer/agents/_symlink`, so their actual implementations are maintained centrally.

When you run `./create_agent.sh a0-template a0-myagent dest_display="My Agent"` from the `tbc-library` root on the host:

- A new agent profile directory `layers/a0-myagent/agents/a0-myagent` (mounted into the container at `/layers/a0-myagent/agents/a0-myagent`) is created, preserving the same symlink structure.
- Centralized tools and prompts continue to live under `layers/control_layer/agents/_symlink` (visible in the container at `/a0/control_layer/agents/_symlink` and `/layers/control_layer/agents/_symlink`), so improvements there automatically apply to `a0-myagent` (and other agents) without copying or manual synchronization.
- For a new agent such as `a0-myagent`, you typically only need to adjust its copies of `_context.md`, the greeting prompt (`prompts/fw.initial_message.md`), the main identity prompt (for example, `prompts/a0-myagent.md` derived from `a0-template.md`), the agent-name extension (`extensions/agent_init/_05_agent_name.py`), and any local overrides, keeping per-agent maintenance small while benefiting from shared evolution of the shared `_symlink` library.

### /volumes/

```
common/
├── prompts/
│   └── tbc/          # External prompt files
private/
public/
shared/
```

- Optional external volumes for additional data or configurations.

#### External prompt resources via `/common`

The `/common` mount exposes host-level resources from `volumes/common` into the container. This enables prompts to pull in external content that lives outside the `/a0` and `/layers` trees while still participating in the same kwargs-aware prompt and plugin system.

- In `docker-compose.yml`, `${PATH_COMMON}` is mounted as `/common` inside the container. For example, host path `volumes/common/prompts/merged/merged_post_system_manual.md` is accessible as `/common/prompts/merged/merged_post_system_manual.md`.
- The prompt `prompts/system/external/merged/merged_post_system_manual.md` is a thin wrapper containing `{{resource_content}}` and is paired with `merged_post_system_manual.py`, a `VariablesPlugin` that calls:
  - `files.read_prompt_file("merged_post_system_manual.md", _directories=["/common/prompts/merged"], **kwargs)`
  - and returns `{"resource_content": <loaded content>}`.
- The system-level prompt `prompts/system/post_behaviour.md` includes this wrapper, so the merged external resource is injected into the system prompt at the desired stage.
- A similar pattern is used for TBC resources such as `tbc.protocols`, `tbc.overview`, and `tbc.lineage`: wrappers in `prompts/tbc/external_resources/...` (each containing `{{resource_content}}`) are paired with `VariablesPlugin` implementations that load the corresponding files from `/common/prompts/tbc/...` (for example, `/common/prompts/tbc/tbc.protocols/tbc.protocols.md`) using `files.read_prompt_file(..., **kwargs)`.

- Because `read_prompt_file` and `VariablesPlugin.get_variables` are kwargs-enabled in the upstream Agent Zero `files.py` (v0.9.7+), any external prompt loaded from `/common` can still see runtime context such as `agent`, `loop_data`, and profile information, making `/common` a powerful external prompt/knowledge layer managed on the host.

## More About Agent Zero

For comprehensive documentation of Agent Zero itself (configuration options, upstream features, API details), refer to the upstream project:

- [Agent Zero on GitHub](https://github.com/agent0ai/agent-zero)
- Inside a running container: `/a0/docs/installation.md` and related files

This technical deep dive focuses on how `tbc-library` layers on top of Agent Zero; the upstream documentation remains the authoritative source for core Agent Zero behavior.
