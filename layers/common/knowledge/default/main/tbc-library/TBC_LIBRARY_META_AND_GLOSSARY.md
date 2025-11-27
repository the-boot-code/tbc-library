# Project Meta and Glossary

This document captures project meta information: final thoughts, disclaimers, versioning details, attribution, and a glossary of key terms.

> **Navigation**: [← Back to README](README.md) | [← Technical Deep Dive](TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md)

## Final Thoughts

The Boot Code Storybook is a living, breathing, evolving project. It is not limited to Agent Zero; what you find here is a framework for taking part in building an idea.

Use your imagination. You can also use Agent Zero to:

- create, maintain, and evolve other agents autonomously by leveraging self-revealing orchestration (see [TBC_LIBRARY_SELF_REVEALING_ORCHESTRATION.md](TBC_LIBRARY_SELF_REVEALING_ORCHESTRATION.md)), and
- layer custom extensions and prompts to add new behaviors without touching the core engine.

This enables organic growth through experimentation and collaboration.

## Disclaimers

This is an ongoing live development project, and the tbc-library documentation set is a living resource. Treat these docs as both a friendly welcome to the project and a primary, evolving source of instructions for how to work with tbc-library; their structure and contents may change over time.

## Versioning

- tbc-library does not yet have a formal version assigned
- The `a0-template/.env.example` file currently sets `IMAGE_NAME=agent0ai/agent-zero:latest`
- Development is in progress to integrate the anticipated Agent Zero v0.9.7 "Projects" functionality with tbc-library

## Attribution

Many thanks to Agent Zero, especially its creator Jan, and to the community of the open-source project.

https://github.com/agent0ai/agent-zero

## Concepts Index

Use this section as a map from high-level ideas to the documents that explain them in depth.

### Narrative concepts

- **Narrative Driven Development (NDD)**  
  - Canonical narrative: [TBC_LIBRARY_NARRATIVE_DRIVEN_DEVELOPMENT.md → Narrative Driven Development: The Boot Code Storybook](TBC_LIBRARY_NARRATIVE_DRIVEN_DEVELOPMENT.md).  
  - High-level positioning alongside technical development: [README.md → Two Parallels Building Together](README.md#two-parallels-building-together).

- **Boot Code and Feedback Machine**  
  - Narrative and technical combination: [TBC_LIBRARY_NARRATIVE_DRIVEN_DEVELOPMENT.md → The "Boot Code" is Narrative and Technical Combined](TBC_LIBRARY_NARRATIVE_DRIVEN_DEVELOPMENT.md#the-boot-code-is-narrative-and-technical-combined).  
  - Feedback loop between stories and systems: [TBC_LIBRARY_NARRATIVE_DRIVEN_DEVELOPMENT.md → The Feedback Machine](TBC_LIBRARY_NARRATIVE_DRIVEN_DEVELOPMENT.md#the-feedback-machine).  
  - Operational view of how modes and profiles realize this: [TBC_LIBRARY_AGENT_REASONING.md → Reasoning modes, profiles, and System Control](TBC_LIBRARY_AGENT_REASONING.md#reasoning-modes-profiles-and-system-control).

- **Finder and creative gateways**  
  - Narrative role of the **Finder** and gateways into the library: [TBC_LIBRARY_NARRATIVE_DRIVEN_DEVELOPMENT.md → Unlocking a Story](TBC_LIBRARY_NARRATIVE_DRIVEN_DEVELOPMENT.md#unlocking-a-story).

### Technical concepts

- **Self-Revealing Orchestration**  
  - Canonical explanation and path mappings: [TBC_LIBRARY_SELF_REVEALING_ORCHESTRATION.md → Direct Agent Access via Bind Mounts](TBC_LIBRARY_SELF_REVEALING_ORCHESTRATION.md#direct-agent-access-via-bind-mounts).  
  - How this underpins Docker Compose: [TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md → Docker Compose Orchestration](TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md#docker-compose-orchestration).

- **Dynamic profiles and System Control**  
  - Core implementation and runtime behaviour: [TBC_LIBRARY_EXTENSIBILITY.md → Dynamic system control and profiles](TBC_LIBRARY_EXTENSIBILITY.md#dynamic-system-control-and-profiles).  
  - System Control helper details: [TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md → Technical Deep Dive](TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md).  
  - How narrative "modes" become profile selections: [TBC_LIBRARY_AGENT_REASONING.md → Reasoning modes, profiles, and System Control](TBC_LIBRARY_AGENT_REASONING.md#reasoning-modes-profiles-and-system-control).

- **Knowledge trees and Solutions**  
  - Knowledge trees and how agents read documentation via `/a0/knowledge`: [TBC_LIBRARY_EXTENSIBILITY.md → Knowledge Features of Agent Zero](TBC_LIBRARY_EXTENSIBILITY.md#knowledge-features-of-agent-zero).  
  - Structured solutions for tools: [TBC_LIBRARY_EXTENSIBILITY.md → Solutions](TBC_LIBRARY_EXTENSIBILITY.md#solutions).

- **Layered architecture and library structure**  
  - Compose, volumes, and bind-mounts: [TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md → Docker Compose Orchestration](TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md#docker-compose-orchestration).  
  - Repository layout and major directories: [TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md → Structure](TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md#structure).

### Agent perspectives and orchestration roles

- **Vantage points (host, container, multi-deployment)**  
  - Mental model of where you are: [TBC_LIBRARY_AGENT_REASONING.md → Vantage points: host, container, and multi-deployment](TBC_LIBRARY_AGENT_REASONING.md#vantage-points-host-container-and-multi-deployment).

- **Self vs managed vs external agents**  
  - Who you are acting as in a given context: [TBC_LIBRARY_AGENT_REASONING.md → Who you are acting as: self vs managed vs external](TBC_LIBRARY_AGENT_REASONING.md#who-you-are-acting-as-self-vs-managed-vs-external).  
  - Concrete path-level rules and scenarios: [TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md → Agent perspectives and management](TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md#agent-perspectives-and-management) and [TBC_LIBRARY_SELF_REVEALING_ORCHESTRATION.md → Orchestration patterns (inside vs outside)](TBC_LIBRARY_SELF_REVEALING_ORCHESTRATION.md#orchestration-patterns-inside-vs-outside).

### Paths, layers, and shared libraries

- **Key paths (`/a0`, `/layers`, `/containers`, `/agent_layer`, `/common_layer`, `/agent_orchestration`)**  
  - How host directories are projected into the container: [TBC_LIBRARY_SELF_REVEALING_ORCHESTRATION.md → Direct Agent Access via Bind Mounts](TBC_LIBRARY_SELF_REVEALING_ORCHESTRATION.md#direct-agent-access-via-bind-mounts).  
  - Host vs container mapping tables: [TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md → Agent perspectives and management](TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md#agent-perspectives-and-management).

- **`_symlink` shared library**  
  - Shared tools, prompts, and extensions for many agents: [TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md → Symlinked Agents and the `_symlink` Profile](TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md#symlinked-agents-and-the-_symlink-profile).

## Glossary

The glossary below is organized alphabetically and focuses on individual terms. Use the **Concepts Index** above when you want grouped, big-picture ideas and where to read about them.

- **Adaptability**: Willingness to revisit assumptions and adjust behaviour when obstacles or new information appear. Emphasized in [README.md → Reading as a human or an agent](README.md#reading-as-a-human-or-an-agent).
- **Agent**: In this project, an "agent" is an Agent Zero process together with its active profile (for example, `/a0/agents/${CONTAINER_NAME}` inside a container). See [TBC_LIBRARY_AGENT_REASONING.md → Who you are acting as: self vs managed vs external](TBC_LIBRARY_AGENT_REASONING.md#who-you-are-acting-as-self-vs-managed-vs-external) and [TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md → Agent perspectives and management](TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md#agent-perspectives-and-management).
- **Agent container**: A Docker container running an Agent Zero instance plus its bind mounts. Containers are parameterized primarily by `.env` and `docker-compose.yml` under `containers/<name>/`; see [TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md → Docker Compose Orchestration](TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md#docker-compose-orchestration).
- **Agent profile**: A specific identity under `/a0/agents/<name>` (mirrored from `layers/<name>/agents/<name>` on the host). Contains prompts, tools, and extensions that describe how that agent behaves; see examples in [TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md → Agent perspectives and management](TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md#agent-perspectives-and-management).
- **Agent Zero**: An open-source AI framework for building customizable agents that learn and adapt. Upstream documentation lives at <https://github.com/agent0ai/agent-zero>; this library layers on top of that engine without modifying its core.
- **Boot Code**: Persistent narrative and technical data that "activates" the system's creative feedback loop. Introduced in [TBC_LIBRARY_NARRATIVE_DRIVEN_DEVELOPMENT.md → The "Boot Code" is Narrative and Technical Combined](TBC_LIBRARY_NARRATIVE_DRIVEN_DEVELOPMENT.md#the-boot-code-is-narrative-and-technical-combined).
- **Common layer**: The shared host directory `layers/common` (seen inside the container as `/common_layer` and via specific `/a0/...` mounts) that holds shared agents, knowledge, prompts, and instruments used by many agents.
- **Control layer**: The host directory `layers/control_layer` (visible inside the container at `/a0/control_layer` and `/layers/control_layer`) containing System Control helpers, profile modules, prompt-includes, and shared `_symlink` implementations; see [TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md → Structure](TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md#structure).
- **Dynamic profiles**: Coordinated System Control and profile modules that let an Agent Zero instance adjust behaviour, reasoning, and security at runtime without changing core code. Canonically described in [TBC_LIBRARY_EXTENSIBILITY.md → Dynamic system control and profiles](TBC_LIBRARY_EXTENSIBILITY.md#dynamic-system-control-and-profiles).
- **Feedback Machine**: The dynamic interplay between storytelling and code execution, enabling organic agent growth. Described narratively in [TBC_LIBRARY_NARRATIVE_DRIVEN_DEVELOPMENT.md → The Feedback Machine](TBC_LIBRARY_NARRATIVE_DRIVEN_DEVELOPMENT.md#the-feedback-machine) and operationally in [TBC_LIBRARY_AGENT_REASONING.md → Reasoning modes, profiles, and System Control](TBC_LIBRARY_AGENT_REASONING.md#reasoning-modes-profiles-and-system-control).
- **Finder**: A user who discovers and shares the secrets of The Boot Code Storybook, often acting as a bridge between narrative worlds and technical systems. Introduced in the "Unlocking a Story" sections of [TBC_LIBRARY_NARRATIVE_DRIVEN_DEVELOPMENT.md](TBC_LIBRARY_NARRATIVE_DRIVEN_DEVELOPMENT.md).
- **Knowledge tree**: A structured directory of narrative, conceptual, or procedural documents under `layers/common/knowledge/...` on the host, exposed inside the container under `/a0/knowledge/...`. See [TBC_LIBRARY_EXTENSIBILITY.md → Knowledge Features of Agent Zero](TBC_LIBRARY_EXTENSIBILITY.md#knowledge-features-of-agent-zero).
- **Layers**: On the host, the `layers/` directory in the `tbc-library` repository; inside the container, the same content is exposed at `/layers` (with `/agent_layer` and `/common_layer` providing focused views). These abstracted directories hold shared and agent-specific configs and data, avoiding direct modifications to the Agent Zero engine; see [TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md → Structure](TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md#structure).
- **Narrative Driven Development**: Building software where stories guide technical features and user experiences. Canonical narrative and philosophy live in [TBC_LIBRARY_NARRATIVE_DRIVEN_DEVELOPMENT.md → Narrative Driven Development: The Boot Code Storybook](TBC_LIBRARY_NARRATIVE_DRIVEN_DEVELOPMENT.md).
- **Self-Revealing Orchestration**: Bind-mount-based orchestration that provides agents with direct, transparent access to their own layers and structure so they can introspect and carefully modify their environment. See [TBC_LIBRARY_SELF_REVEALING_ORCHESTRATION.md → Direct Agent Access via Bind Mounts](TBC_LIBRARY_SELF_REVEALING_ORCHESTRATION.md#direct-agent-access-via-bind-mounts).
- **System Control**: A coordinated subsystem (centered on `system_control.py`) that records active profiles and prompt-includes, and exposes tools (such as `workflow_profile_control` and `reasoning_profile_control`) for adjusting them at runtime. See [TBC_LIBRARY_EXTENSIBILITY.md → Dynamic system control and profiles](TBC_LIBRARY_EXTENSIBILITY.md#dynamic-system-control-and-profiles) and [TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md → Technical Deep Dive](TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md).
- **tbc-library**: The host Git repository and layered deployment framework that orchestrates Agent Zero containers, layers, and volumes for The Boot Code Storybook project. Introduced in [README.md](README.md) and elaborated across the split documentation set.
- **Vantage point**: The perspective from which you are reasoning about the system (for example, host repository, inside a single container, or multi-deployment orchestrator). See [TBC_LIBRARY_AGENT_REASONING.md → Vantage points: host, container, and multi-deployment](TBC_LIBRARY_AGENT_REASONING.md#vantage-points-host-container-and-multi-deployment).
