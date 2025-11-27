# Self-Revealing Orchestration

This document explains how bind mounts enable agents to access their own structure and how to reason about paths and orchestration roles.

> **Navigation**: [← Back to README](README.md) | [← Installation](TBC_LIBRARY_INSTALLATION.md) | [Extensibility →](TBC_LIBRARY_EXTENSIBILITY.md)

## How to reason as an agent using this tbc-library documentation

This document focuses on how self-revealing orchestration works: how bind mounts expose your own structure and how to read the path mappings that follow. For the **full mental model** of host vs container perspectives, self vs managed agents, and multi-deployment orchestration across the entire documentation set, use [TBC_LIBRARY_AGENT_REASONING.md → How to reason about this documentation as an agent](TBC_LIBRARY_AGENT_REASONING.md#how-to-reason-about-this-documentation-as-an-agent).

When you read the examples and mappings below, remember:

- Paths like `/a0/...`, `/agent_orchestration`, `/agent_layer`, `/common_layer`, and `/containers` describe your **in-container view** of the world created by tbc-library's bind mounts.
- Paths like `tbc-library/...`, `containers/...`, and `layers/...` (without a leading `/`) describe the **host repository view** of the same structures.

For detailed classification of self vs managed agents, and for worked path-perspective examples, see [TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md → Agent perspectives and management](TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md#agent-perspectives-and-management).

## Direct Agent Access via Bind Mounts

The `docker-compose.yml` file leverages bind mounts to create a self-revealing orchestration, where the agent gains direct, transparent access to its own layers and orchestration elements. This eliminates the need for complex path-indirection logic, allowing Agent Zero to interact with its configurations, data, and even its own container structure as native paths within the container.

### Direct /a0/ Layer Mappings

These mappings provide agent-specific access to layers directly under `/a0/`, enabling seamless internal operations, including but not limited to:

- `${AGENT_LAYER}/agents/${CONTAINER_NAME}:/a0/agents/${CONTAINER_NAME}` → Agent profiles accessible at `/a0/agents/${CONTAINER_NAME}`.
- `${AGENT_LAYER}/conf:/a0/conf` → Configuration files at `/a0/conf`.
- `${AGENT_LAYER}/memory:/a0/memory` → Memory data at `/a0/memory`.
- `${AGENT_LAYER}/logs:/a0/logs` → Logs at `/a0/logs`.
- `${AGENT_LAYER}/tmp:/a0/tmp` → Temp files at `/a0/tmp`.
- `${AGENT_LAYER}/work_dir:/a0/work_dir` → Working directory at `/a0/work_dir`.

This setup allows Agent Zero to treat its layers as intrinsic container paths, simplifying extensions and enabling organic growth without external dependencies.

### Composition Mappings for Self-Access

The composition mappings provide the agent with reliable direct access to its own orchestration and structure, fostering self-awareness and autonomy, including but not limited to:

- `${AGENT_ORCHESTRATION}:/agent_orchestration:ro` → Read-only access to the agent's orchestration directory, allowing introspection of its own setup. *Example*: The agent can read its `docker-compose.yml` from `/agent_orchestration` to dynamically discover port mappings or container names, enabling self-configuring behaviors without hardcoded values.
- `${AGENT_CONTAINER}:/agent_container:rw` → Read-write access to the container's root `/a0`, enabling full self-modification and layering.
- `${AGENT_LAYER}:/agent_layer:rw` → Direct manipulation of the agent's layer directory for dynamic configurations.
- `${COMMON_LAYER}:/common_layer:ro` → Shared resources accessible without duplication, ensuring consistency across agents.

In addition to these high-level mounts, typical tbc-library deployments expose the library's own documentation and solutions into the knowledge tree via knowledge-specific mappings, for example:

- `${COMMON_LAYER}/knowledge/default/main/tbc-library:/a0/knowledge/default/main/tbc-library:ro` for the tbc-library documentation cluster (README and `TBC_LIBRARY_*.md` files).
- `${COMMON_LAYER}/knowledge/default/solutions/tbc-library:/a0/knowledge/default/solutions/tbc-library:ro` for solutions that describe how to use tbc-library tools, profiles, and workflows.

For an agent reasoning about its environment, simply recognizing that these mounts exist and what they represent is part of self-revealing orchestration: the library that shapes the world is itself visible under `/a0/knowledge/...` alongside other knowledge trees.

Note: Some mounts are read-only (ro) for system protection and introspection, while others are read-write (rw), allowing agents to modify their own files (e.g., `docker-compose.yml` via `/containers/[agent_name]/docker-compose.yml`) for full autonomy. This balance enables safe self-awareness while supporting generative evolution.

These mappings empower the agent to reveal and control its own existence, blurring the line between container and host. With this self-knowledge, the agent understands its own configuration and can modify, maintain, or create other agents, fostering a truly autonomous ecosystem (see [TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md → Agent perspectives and management](TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md#agent-perspectives-and-management) for distinguishing "self" vs other agents across these paths).

### Orchestration patterns (inside vs outside)

- **Inside-container orchestrator**  
  An Agent Zero instance running inside a container uses `/a0/agents` plus the rules in [TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md → Self vs managed agents: example scenarios](TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md#self-vs-managed-agents-example-scenarios) to treat `/a0/agents/${CONTAINER_NAME}` as "self" and other entries (e.g., `kairos`) as managed/subordinate agents. Profile-control tools operate on these local profiles while respecting shared `_symlink` implementations. Subordinate orchestration tools (e.g., an upstream Agent Zero `call_subordinate` tool, if present in your image) are image-dependent and not shipped by `tbc-library`.
- **Inside-container library-aware orchestrator**  
  The same in-container agent can reason about other agents and containers within the same `tbc-library` deployment by using `/containers` and `/layers` (bind-mounted from that deployment's `containers/` and `layers/` directories on the host) together with `/agent_orchestration` and `/agent_layer` (self-specific views of its own container directory and layer). This provides a clear separation between "my own container" (`/agent_orchestration`, `/agent_container`, `/agent_layer`) and "other containers/agents in this deployment" (visible under `/containers` and `/layers`), while still applying the self vs managed agents rules for anything under `/a0/agents`.
- **Host/external orchestrator (multi-deployment)**  
  A human or external agent running on the host uses the `tbc-library` repository layout to manage multiple containers and even multiple `tbc-library` deployments: each deployment corresponds to a clone of `tbc-library`, with individual agents at `containers/a0-*/` and their layers at `layers/a0-*/`. From this perspective, `/containers` and `/layers` inside each container are simply bind-mounted views of that deployment's host directories, and `/agent_orchestration`, `/agent_container`, and `/agent_layer` are per-container convenience mounts, allowing orchestration across many agents and containers without confusing their internal `/a0/agents` trees.

Other permutations (for example, an in-container manager coordinating both its own subordinates and other containers via `/layers/...` and `/containers/...`) can be constructed by combining these two patterns while always applying the path and perspective rules above.

## Worked examples: perspectives and paths

These examples show how to apply the path and orchestration rules in concrete situations.

### 1. Self introspection from inside a container (inside-container orchestrator)
- **Scenario**: `a0-myagent` wants to find its own `docker-compose.yml` without guessing host paths.
- **Action (inside container)**: read `/agent_orchestration/docker-compose.yml` to introspect its own orchestration.
- **Mapping**: `/agent_orchestration/docker-compose.yml` corresponds to `tbc-library/containers/a0-myagent/docker-compose.yml` on the host for this deployment.

### 2. Calling a subordinate in the same container (self vs managed agents)
- **Scenario**: the `/a0/agents` directory contains entries such as `a0-myagent`, `kairos`, `default`, `developer`, and `_symlink`, and you want to call one of the non-underscore profiles as a subordinate while treating `_symlink` as a shared implementation library, not a runnable profile.
- **Classification**: `/a0/agents/a0-myagent` is the current self profile; entries such as `default` or `developer` are additional profiles in the same container that could be activated as self or treated as managed/subordinate agents; `/a0/agents/kairos` is a subordinate profile from the common layer; `_symlink` physically exists under `/a0/agents` as a shared implementation library but is not offered as a runnable profile in `{{agent_profiles}}`.
- **Action**: invoke `kairos` (or another non-underscore profile) by name using whatever subordinate orchestration mechanism your Agent Zero deployment provides (for example, an upstream `call_subordinate` tool, if present in your image), treating it as a managed agent within the same container. In this deployment, `tbc-library` does not ship its own `call_subordinate` plugin; availability and behaviour of any such tool are determined by the underlying Agent Zero image.

### 3. Inspecting another agent/container within the same deployment (inside-container library-aware orchestrator)
- **Scenario**: inside the `a0-template` container, you want to examine the `a0-myagent` profile that belongs to another container in the same `tbc-library` deployment.
- **Action**: inspect `/layers/a0-myagent/agents/a0-myagent/_context.md` and related files; this path is visible inside the `a0-template` container via the `${PATH_LAYERS}:/layers` bind mount.
- **Separation**: `a0-myagent` never appears under `/a0/agents` in the `a0-template` container; it is part of another container's Agent Zero tree, so you reason about it via `/layers/...` and `/containers/...`, not as a local subordinate.

### 4. Host/external orchestration across deployments (multi-deployment orchestrator)
- **Scenario**: a human or external agent manages two separate `tbc-library` deployments at `/opt/tbc-a/tbc-library` and `/opt/tbc-b/tbc-library`.
- **Action**: for each deployment, treat `containers/a0-*/` as container definitions and `layers/a0-*/` as their layer trees; starting or modifying containers is done via these host paths.
- **Mapping**: inside each container created from a given deployment, `/containers` and `/layers` are bind-mounted views of that deployment's host directories, and `/agent_orchestration`, `/agent_container`, and `/agent_layer` provide self-specific views for that particular container.
