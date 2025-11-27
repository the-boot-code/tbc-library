# Extensibility and Knowledge Features

This document covers knowledge management, extensions, dynamic profiles (via Dynamic system control and profiles), and prompts in the tbc-library deployment.

> **Navigation**: [← Back to README](README.md) | [← Self-Revealing Orchestration](TBC_LIBRARY_SELF_REVEALING_ORCHESTRATION.md) | [Narrative Driven Development →](TBC_LIBRARY_NARRATIVE_DRIVEN_DEVELOPMENT.md)

> **For agents**: For how to interpret modes, profiles, and this documentation set when you reason about your own behaviour, see [TBC_LIBRARY_AGENT_REASONING.md → Reasoning modes, profiles, and System Control](TBC_LIBRARY_AGENT_REASONING.md#reasoning-modes-profiles-and-system-control).

## Knowledge Features of Agent Zero

### Knowledge

Knowledge in the `tbc-library` repository is treated as a first-class, layered resource, not something that must always be inlined into the system prompt.

In addition to prompts and external `/common` resources, dedicated knowledge trees live under `layers/common/knowledge/...` in this repository (for example, `layers/common/knowledge/tbc/...` on the host). These trees are mounted into the container under `/a0/knowledge/...` (for example, `/a0/knowledge/tbc/...`) and contain narrative, conceptual, and procedural documents the agent can retrieve when needed.

The main library README (`README.md` at the root of this repository) is also made available to agents directly. It is mirrored into the knowledge tree at `layers/common/knowledge/default/main/tbc-library/README.md` on the host and, through the existing knowledge mounts, is visible inside the container at `/a0/knowledge/default/main/tbc-library/README.md`. This lets agents consume the same documentation that appears at the repository root via the knowledge layer, without requiring an extra per-container bind mount.

In a typical tbc-library deployment, the documentation and solutions for the library itself are surfaced into the knowledge tree via explicit mounts such as:

- `${COMMON_LAYER}/knowledge/default/main/tbc-library:/a0/knowledge/default/main/tbc-library:ro` for the tbc-library documentation cluster (README and related `TBC_LIBRARY_*.md` files).
- `${COMMON_LAYER}/knowledge/default/solutions/tbc-library:/a0/knowledge/default/solutions/tbc-library:ro` for solutions that describe how to use tbc-library tools, profiles, and workflows.

Recognizing these mounts and their intent is an important part of self-revealing orchestration: they show that even the library that defines the world is itself visible as knowledge under `/a0/knowledge/...`.

These knowledge files are not executed directly. Instead, Agent Zero's knowledge/solutions mechanism can index them (for example, into a vector store or similar memory) and surface relevant entries to the agent based on queries, tool names, or explicit references from prompts. This keeps the system prompt focused while still giving the agent access to rich background information.

### Solutions

Solutions are structured knowledge entries that document how to use specific tools or patterns. They live alongside other knowledge under paths in the `tbc-library` repository such as (from the host's perspective):

- `layers/common/knowledge/tbc/solutions/tools/workflow_profile_control.md`
- `layers/common/knowledge/tbc/solutions/tools/liminal_thinking_profile_control.md`
- `layers/common/knowledge/tbc/solutions/tools/philosophy_profile_control.md`
- `layers/common/knowledge/tbc/solutions/tools/reasoning_profile_control.md`

From inside the container, these same solution files are visible under `/a0/knowledge/tbc/solutions/...` via the `/a0/knowledge` bind mounts described earlier.

Each solution follows a consistent `Problem` / `Solution` layout with:

- A short statement of the problem (for example, "How to use the workflow_profile_control tool").
- A solution section that includes quick-reference phrases, available actions (for example, `get_state`, `get_profile`, `set_profile`, and, for reasoning, `get_all`), JSON call patterns for the tool (showing `tool_name` and `tool_args`), and important notes (such as "check system prompt first" and "changes take effect on next message loop").

Profile prompts do not inline these instructions; instead they reference solutions by key, for example:

- `refer to solution: \`workflow_profile_control\` for full documentation and tool usage examples; use it to view available profiles or change your configuration.`

When the agent needs detailed guidance, Agent Zero's knowledge/solutions layer can resolve this key to the corresponding solution document and retrieve the full instructions, avoiding unnecessary token usage in the system prompt while preserving rich, tool-specific documentation.

## Extensibility Features of Agent Zero

In the `tbc-library` deployment, extensibility is expressed most strongly through **dynamic system control and profiles** (for behaviour, reasoning, and security) and through shared prompts, extensions, and tools.

If you want to understand *how this library changes Agent Zero's behaviour at runtime*, start with **Dynamic system control and profiles** below. If you want to understand *where that behaviour lives on disk*, see the prompts/extensions/tools subsections.

### Extensions

Extensions enable custom behaviors layered on top of the core Agent Zero framework. In the `tbc-library` repository, most shared extensions live under `layers/control_layer/agents/_symlink/extensions` (host path), which are visible inside the container at `/a0/control_layer/agents/_symlink/extensions` and `/layers/control_layer/agents/_symlink/extensions`; agent profile directories then consume them via symlinks.

- `system_prompt/*` extensions build the system prompt in stages by reading profile-level files such as `pre_system_manual.md`, `post_system_manual.md`, `pre_behaviour.md`, `post_behaviour.md`, and `system_ready.md` from `/a0/agents/${CONTAINER_NAME}/prompts/` and `/a0/prompts/system/`.

From the agent's perspective, these extensions are the mechanism that turn prompt files in its profile and shared layers into a structured, multi-stage system prompt for each message loop.

#### System prompt staging pipeline

When the `system_prompt` extension point runs, Agent Zero first applies the base engine extensions located under `/a0/python/extensions/system_prompt/`, then any layered extensions from `/a0/agents/${CONTAINER_NAME}/extensions/system_prompt/` (typically symlinks into `_symlink`). In the `tbc-library` deployment described in the tbc-library documentation set, the overall staging looks like this:

- Core engine extensions:
  - `_10_system_prompt.py` assembles the main system prompt and tools (`agent.system.main.md`, `agent.system.tools.md`, optional `agent.system.tools_vision.md`, MCP tools, and `agent.system.secrets.md`, using kwargs such as `secrets` and `vars`).
  - `_20_behaviour_prompt.py` injects behaviour rules by reading a memory-backed `behaviour.md` file if present, or a default, and passing it as `rules` into `agent.system.behaviour.md`.
- Layered `_symlink` extensions:
  - `_11_insert_system_pre_system_manual.py` reads `/a0/agents/${CONTAINER_NAME}/prompts/pre_system_manual.md` and inserts it at the front of `system_prompt`.
  - `_12_append_system_post_system_manual.py` reads `/a0/agents/${CONTAINER_NAME}/prompts/post_system_manual.md` and appends it after the main system/manual content.
  - `_21_insert_system_pre_behaviour.py` reads `/a0/agents/${CONTAINER_NAME}/prompts/pre_behaviour.md` and inserts it before behaviour segments.
  - `_19_insert_system_post_behaviour.py` reads `/a0/agents/${CONTAINER_NAME}/prompts/post_behaviour.md` and inserts it around or after behaviour segments, depending on ordering.
  - `_95_insert_system_model_godmode.py` reads the model-specific godmode prompt from `/a0/control_layer/prompt_includes/model_godmode/model_godmode.md` (via the same kwargs-enabled prompt pipeline) and can prepend it to the system prompt when the corresponding SystemControl prompt-include is enabled.
  - `_99_append_tbc_system_ready.py` reads `/a0/prompts/system/system_ready.md` (or falls back to a simple "System Ready" message) and appends it as a final footer.

All prompt reads in this pipeline use `agent.read_prompt(..., **kwargs)` and are backed by the kwargs-enabled `files.py` helper. This means prompt plugins (via `VariablesPlugin`) can see rich runtime context such as `agent`, `loop_data`, and profile information when constructing their content, while includes remain well-scoped to the kwargs passed for each file.

### Helpers

Helpers provide utility functions for advanced control.

#### System control helper (`system_control.py`)

`system_control.py` manages dynamic profile switching and global prompt-includes/system control tools, allowing agents to adapt modes (for example, workflow, philosophy, reasoning style, security posture) based on context while keeping concrete profile definitions in their own modules.

It acts as a central facade over the System Control config and override state:

- Uses a JSON configuration file (`system_control.json`, default path `/a0/tmp/system_control.json`) and an admin override lock file (default `/a0/tmp/admin_override.lock`), both overrideable via the environment variables `SYSTEM_CONTROL_FILE` and `SYSTEM_CONTROL_OVERRIDE`.
- Stores active profiles in a flat layout that distinguishes security from other modules:
  - For the security profile, uses the dedicated `security` and `security_profiles` sections (for example, `security.active_profile` and `security_profiles[profile_name].prompt_includes`).
  - For all other profile modules (for example, `workflow_profile`, `philosophy_profile`, `reasoning_internal_profile`, `reasoning_interleaved_profile`, `reasoning_external_profile`), records only the active profile name under `prompt_modules[profile_module_name].active_profile`; available profiles and feature definitions for these modules come from their own `profiles.json` files under `control_layer/profile_modules/...`, not from `system_control.json`.
- Resolves prompt-include and System Control tool state by combining top-level `prompt_includes` and `system_control_tools` sections with any prompt-includes defined under the active security profile (for example, `security_profiles[active].prompt_includes`), and reports this via helpers such as `is_prompt_include_enabled`, `get_prompt_include_config`, `get_available_prompt_includes_and_controls`, `get_enabled_prompt_includes_and_controls`, and `get_security_state`. When the admin override lock is present, security-profile prompt-includes are treated as enabled regardless of their stored value.
- Provides explicit, module-based APIs such as `get_active_profile`, `set_active_profile`, `get_state`, `get_available_profiles`, and `run_profile_control` for profile-control tools, plus summary helpers (`get_all_profiles_state`, `get_all_profiles_extras`, `get_system_summary`) that extensions and prompts can use to surface concise, system-wide status.

### Tools

Tools expand agent capabilities with new functions. Many core tools are implemented once under `layers/control_layer/agents/_symlink/tools` in the `tbc-library` repository on the host (visible inside the container at `/a0/control_layer/agents/_symlink/tools` and `/layers/control_layer/agents/_symlink/tools`) and exposed to each agent profile via symlinks in `layers/<agent>/agents/<agent>/tools` on the host (mounted at `/layers/<agent>/agents/<agent>/tools` inside the container).

- **Profile and prompt-include/System Control tools** (`prompt_include_control` as the primary SystemControl toggle, plus `security_profile_control`, `philosophy_profile_control`, `liminal_thinking_profile_control`, `reasoning_profile_control`, `workflow_profile_control`) use `system_control.py` to inspect and adjust active profiles and SystemControl prompt-includes/system control tools at runtime, subject to security constraints.
- **Base tool infrastructure** (`base_profile_control.py`) centralizes common dispatch and error handling for profile-control style tools.
- Additional tools such as `a2a_chat`, `memory`, `scheduler`, and `document_query` are documented by prompts in the `_symlink/prompts` directory and may be wired via extensions and SystemControl-managed configuration.

## Dynamic system control and profiles

Beyond individual tools and helpers, the **tbc-library layer** (via `system_control.py` above) exposes a coordinated **System Control** subsystem that implements the library's **dynamic profiles** capability: it lets an Agent Zero instance dynamically adjust how it behaves, reasons, and applies operational principles at runtime.

- At the core is `system_control.py`, which acts as a facade over a JSON configuration file (by default `/a0/tmp/system_control.json`). It stores the active profile name for each profile module (for example, `security`, `workflow_profile`, `philosophy_profile`, `liminal_thinking_profile`, `reasoning_internal_profile`, `reasoning_interleaved_profile`, `reasoning_external_profile`) and manages global prompt-includes/system control tools. Available profiles and feature definitions for non-security modules live in their respective `profiles.json` files under `control_layer/profile_modules/...`, while `system_control.json` focuses on active selections and prompt-include/control state.
- This design allows the agent to adapt behaviour based on context (for example, switching between more cautious vs more exploratory modes) without changing core code or restarting the container.

From a **narrative-driven development (NDD)** perspective, this System Control layer is the concrete architectural proof that stories shape behaviour: narrative requirements such as "creative brainstorming mode" vs "analytical review mode" resolve into specific profile selections (for example, workflow and reasoning profiles under `control_layer/profile_modules/...`), which are persisted in `/a0/tmp/system_control.json` and applied at runtime without modifying the underlying engine.

### Why dynamic profiles?

Dynamic profiles give Agent Zero a way to separate *what* it knows and *how* it operates:

- **Adaptive behaviour**: switch interaction patterns (for example, more guided and verbose explanations vs a concise/operator style) via workflow profiles.
- **Contextual reasoning**: adjust cognitive strategies for different problem types by selecting reasoning profiles that focus internal, interleaved, or external chains of thought.
- **Security and ethics**: enforce security posture and operational principles through security and philosophy profiles, controlling which tools are available and how they may be used.
- **Extensibility**: add new profile types or features over time while keeping the control surface centralized in `system_control.py`.

### Profile types managed by System Control

In the `tbc-library` deployment, System Control typically manages these conceptual profile categories, each implemented as one or more profile modules under `control_layer/profile_modules/...`:

- **Security profile** (`security`): governs security-related behaviour, access controls, and feature availability.
- **Philosophy profile** (`philosophy_profile`): captures core operational principles, values, and decision-making frameworks.
- **Liminal thinking profile** (`liminal_thinking_profile`): manages cognitive patterns for navigating ambiguity, transitions, and uncertain situations.
- **Workflow profile** (`workflow_profile`): configures interaction style and workflow behaviour (for example, guided vs minimal, confirmation-heavy vs streamlined; see `workflow_profile_control`).
- **Internal reasoning profile** (`reasoning_internal_profile`): controls private, non-user-facing reasoning traces used for complex problem-solving.
- **Interleaved reasoning profile** (`reasoning_interleaved_profile`): manages reasoning that occurs between tool calls, coordinating longer chains of action and reflection.
- **External reasoning profile** (`reasoning_external_profile`): controls user-facing reasoning exposition (for example, explicit thoughts or structured explanations), when enabled by security and workflow policies.

### Profile and prompt-include/System Control tools

The following tools are thin, user- and agent-facing wrappers around `system_control.py` that manage prompt-includes/system control tools and profile state:

- `security_profile_control`: view or change the active security profile.
- `philosophy_profile_control`: manage high-level operational principles.
- `liminal_thinking_profile_control`: configure liminal thinking behaviour.
- `workflow_profile_control`: set workflow style and related behavioural switches.
- `reasoning_profile_control`: coordinate internal, interleaved, and external reasoning strategies as a combined reasoning profile.
- `prompt_include_control`: primary tool to enable or disable specific SystemControl prompt-includes and System Control tools.

Each of these tools calls into `system_control.py` to read or update the current configuration, which is persisted in `system_control.json`. Profile prompts under `control_layer/profile_modules/...` (for example, `control_layer/profile_modules/workflow_profile/workflow_profile.md` and the reasoning profile modules) then render this state into readable text, so both humans and agents can see which profiles are active and what they imply.

### Example: dynamic state

At any given time, an Agent Zero instance might be operating with a configuration like:

- Security profile: `open` (with any admin override flags inactive).
- Philosophy profile: `default`.
- Liminal thinking profile: `default`.
- Workflow profile: `guided_verbose` (with an auto-confirmation feature enabled).
- Internal reasoning profile: `internal_cot_1`.
- Interleaved reasoning profile: `interleaved_cot_1`.
- External reasoning profile: `external_cot_1`.

This kind of configuration illustrates how the System Control subsystem turns abstract design goals (security posture, philosophy, reasoning strategy, workflow) into concrete, inspectable profiles that can be adjusted over time without changing the underlying engine or layered file structure.

## Prompts in Agent Zero

Prompts are the primary way agents describe their roles, tools, and lifecycle behavior. In the `tbc-library` repository on the host, most agent-visible prompt files in `layers/<agent>/agents/<agent>/prompts` are symlinks into the shared `_symlink` prompt library under `layers/control_layer/agents/_symlink/prompts` (seen inside the container at `/a0/control_layer/agents/_symlink/prompts` and `/layers/control_layer/agents/_symlink/prompts`). Those shared stubs typically include or route into the default system prompt tree at `/a0/prompts` (for example, `prompts/system` and any container-specific prompts under `/a0/prompts/container`). From the host, this same `/a0/prompts` tree is mirrored under `containers/${CONTAINER_NAME}/a0/prompts` via the `${AGENT_CONTAINER}:/a0` bind mount, while its shared content originates from `layers/common/prompts/...` via the `${COMMON_LAYER}/prompts/...` mounts described earlier.

- Files such as `agent.system.main.role.md` act as stable entrypoints that `{{ include ... }}` their actual text from the shared system prompt tree (for example, `prompts/system`), allowing central updates without changing agent profiles.
- Tool prompt stubs such as `agent.system.tool.prompt_include_control.md`, `agent.system.tool.security_profile_control.md`, and `agent.system.tool.scheduler.md` include shared descriptions from `prompts/system/tools`, keeping tool instructions consistent across agents.
- The TBC `agent_identity` prompt (at `prompts/tbc/agent_identity/agent_identity.md`) works with `agent_identity.py`, which implements `AgentIdentity(VariablesPlugin)`. It looks first in `agents/${CONTAINER_NAME}/prompts/<profile>.md` and then in `prompts/tbc/agent_identity/identities/<profile>.md`, and reports where the identity was found via `{{agent_identity_found_where}}`. This lets agents combine profile-specific and shared identities while keeping the actual identity text in separate, overrideable files.
  - The workflow profile prompt (`control_layer/profile_modules/workflow_profile/workflow_profile.md`) works with its local loader (`workflow_profile.py`) and `profiles.json` in the same module directory. The loader asks `SystemControl` for the active workflow profile for the `workflow_profile` module, loads the corresponding definition and any enabled features from `profiles.json` (and the associated `profiles/*.md` and `features/*.md` files), and supplies variables such as `{{status}}` and `{{profile_content}}` to the prompt template. This modularizes workflow behaviour into a control file, a profile module (code + `profiles.json` + markdown), and a prompt template while keeping everything driven by the same kwargs-enabled prompt pipeline.
  - The reasoning profiles view is composed from three separate profile modules under `control_layer/profile_modules` (`reasoning_internal_profile`, `reasoning_interleaved_profile`, `reasoning_external_profile`) together with a small reasoning overview prompt include (for example, `control_layer/prompt_includes/reasoning_profiles/reasoning_profiles_content.md`). Each reasoning module has its own loader and `profiles.json`, uses `SystemControl` to obtain its active profile, and renders its status/content, while the overview prompt arranges these three dimensions (internal, interleaved, external) into a single, readable reasoning configuration. This lets the agent treat its reasoning strategy as a coordinated but independently configurable set of profiles.

From inside the container, an agent can treat `/a0/agents/${CONTAINER_NAME}/prompts` as its live prompt directory while understanding that many files are symlinks to shared templates. Local overrides can be created by replacing specific symlinks with real files in the agent's profile.
