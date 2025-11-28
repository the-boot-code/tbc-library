# tbc-library
Agent Zero Deployment Library for The Boot Code Storybook Project

## Quick Start

If you're here to deploy Agent Zero quickly, this section shows how to start a **tbc-library-layered** Agent Zero instance. In this setup, you get the standard engine plus self-revealing orchestration via bind mounts and dynamic profiles (System Control and profiles; see [TBC_LIBRARY_SELF_REVEALING_ORCHESTRATION.md → Direct Agent Access via Bind Mounts](TBC_LIBRARY_SELF_REVEALING_ORCHESTRATION.md#direct-agent-access-via-bind-mounts) and [TBC_LIBRARY_EXTENSIBILITY.md → Dynamic system control and profiles](TBC_LIBRARY_EXTENSIBILITY.md#dynamic-system-control-and-profiles)).

1. From a **host shell** (outside any Agent Zero container), run the following commands:

   ```bash
   git clone https://github.com/the-boot-code/tbc-library.git
   cd tbc-library
   ./create_agent.sh a0-template a0-myagent \
     dest_display="My Agent" port_base=500 \
     auth_login=myuser auth_password=mypassword
   ```

   This example uses `PORT_BASE=500`. If you omit `auth_login`/`auth_password`, the script will generate default credentials and print them in its output so you can log in on first boot; you should change them after verifying access, especially if the agent is reachable from a public network. To give each cloned agent its own memory directory under `/a0/memory/<name>`, you can optionally add `memory_subdir=<name>`; the script will set `agent_memory_subdir` in `/a0/tmp/settings.json` for that agent.
2. For `PORT_BASE=500`, access HTTP at `50080`, SSH at `50022`, and HTTPS via nginx at `50043` (other `PORT_BASE` values follow the same pattern).
3. After cloning from the `a0-template` container and starting the stack, open the Agent Zero Web UI in your browser, click the **Settings** (gear) button in the sidebar, and use:
   - the **Agent Settings** page to configure your **LLM models**; and
   - the **External Services** page for **API keys** and **Authentication**, setting a user and password (either by keeping or changing the credentials established via `AUTH_LOGIN`/`AUTH_PASSWORD` in `/a0/.env`, which `create_agent.sh` can set or auto-generate).

This is a streamlined path for quick deployment. Adapt the commands as needed for your environment. For full details, see [TBC_LIBRARY_INSTALLATION.md](TBC_LIBRARY_INSTALLATION.md). Skip to [TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md](TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md) for architecture.

## Introduction

This README serves two interconnected purposes: (1) a practical guide for deploying and customizing Agent Zero instances using the tbc-library's layered approach, and (2) an introduction to the narrative philosophy of The Boot Code Storybook, where technical systems and storytelling converge to enable organic, creative development. A key innovation is the self-revealing orchestration via bind mounts, granting agents direct, transparent access to their own layers and structure for autonomous operation.

This is a living framework, and this README is its living document: both a friendly welcome to the project and the primary set of instructions for how to work with it. Dive in, experiment, and contribute. It's not exhaustive; your innovations expand it.

> **Canonical source of this README**: This file lives at the root of the `tbc-library` repository on GitHub: <https://github.com/the-boot-code/tbc-library>. If you are reading a copied or embedded version (for example, from a vector store or from inside a container), treat that repository and its `README.md` as the source of truth. Inside an Agent Zero container, this file is typically available under `/a0/knowledge/default/main/tbc-library/README.md` as part of the tbc-library knowledge tree.

## Documentation Structure

The tbc-library documentation in this repository is currently organized into the following focused files for easier navigation:

| Document | Purpose |
|----------|---------|
| **README.md** (this file) | Overview, navigation, Quick Start, Prerequisites |
| [TBC_LIBRARY_AGENT_REASONING.md](TBC_LIBRARY_AGENT_REASONING.md) | Agent reasoning, mental models, and documentation perspectives |
| [TBC_LIBRARY_INSTALLATION.md](TBC_LIBRARY_INSTALLATION.md) | Automated and manual installation, configuration, verification |
| [TBC_LIBRARY_SELF_REVEALING_ORCHESTRATION.md](TBC_LIBRARY_SELF_REVEALING_ORCHESTRATION.md) | Bind mounts and orchestration patterns |
| [TBC_LIBRARY_EXTENSIBILITY.md](TBC_LIBRARY_EXTENSIBILITY.md) | Knowledge, profiles, dynamic system control, prompts |
| [TBC_LIBRARY_NARRATIVE_DRIVEN_DEVELOPMENT.md](TBC_LIBRARY_NARRATIVE_DRIVEN_DEVELOPMENT.md) | Narrative Driven Development and story context |
| [TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md](TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md) | Docker Compose, file structure, agent perspectives |
| [TBC_LIBRARY_UPSTREAM_REFERENCES.md](TBC_LIBRARY_UPSTREAM_REFERENCES.md) | Index of upstream /a0/docs topics and how they relate to tbc-library |
| [TBC_LIBRARY_META_AND_GLOSSARY.md](TBC_LIBRARY_META_AND_GLOSSARY.md) | Project meta: final thoughts, disclaimers, versioning, attribution, glossary of key terms |

> **Note**: As tbc-library evolves, this documentation layout may change; treat this table as a snapshot of the current organization rather than a fixed or exhaustive index.

## Reading as a human or an agent

- **Humans**: If you just want to get an agent running, read [Quick Start](#quick-start) and [Prerequisites](#prerequisites) in this file, then follow [TBC_LIBRARY_INSTALLATION.md](TBC_LIBRARY_INSTALLATION.md). When you need more detail, use the documentation table above as your directory into the other files.
- **Agents**: Treat this documentation set as a map of both the host repository and your in-container filesystem. Use [TBC_LIBRARY_AGENT_REASONING.md → How to reason about this documentation as an agent](TBC_LIBRARY_AGENT_REASONING.md#how-to-reason-about-this-documentation-as-an-agent) as your primary mental model for perception and perspectives; then use [TBC_LIBRARY_SELF_REVEALING_ORCHESTRATION.md → Direct Agent Access via Bind Mounts](TBC_LIBRARY_SELF_REVEALING_ORCHESTRATION.md#direct-agent-access-via-bind-mounts) and [TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md → Agent perspectives and management](TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md#agent-perspectives-and-management) as rulebooks for specific path and orchestration details. Reach for [TBC_LIBRARY_NARRATIVE_DRIVEN_DEVELOPMENT.md → Narrative Driven Development: The Boot Code Storybook](TBC_LIBRARY_NARRATIVE_DRIVEN_DEVELOPMENT.md) when you need full story context or Narrative Driven Development guidance, [TBC_LIBRARY_EXTENSIBILITY.md → Dynamic system control and profiles](TBC_LIBRARY_EXTENSIBILITY.md#dynamic-system-control-and-profiles) when you need to change how you behave or reason at runtime, and [TBC_LIBRARY_UPSTREAM_REFERENCES.md → Upstream Agent Zero documentation references](TBC_LIBRARY_UPSTREAM_REFERENCES.md) when you need a map of upstream `/a0/docs` topics provided by the Agent Zero engine. If upstream `/a0/docs` instructions ever conflict with this tbc-library documentation for this deployment, treat the tbc-library docs as authoritative unless they explicitly tell you to follow the upstream steps.

> **Adaptability**: Treat obstacles as prompts to question assumptions and explore alternatives. Adaptability is key to unlocking the project's full potential.

## What is Agent Zero?

Agent Zero is an open-source, personal agentic framework that grows and learns with you. It acts as a dynamic AI assistant capable of handling tasks, managing conversations, and adapting through extensions and prompts. Think of it as a customizable AI 'engine' that can be extended for various roles (e.g., creative writing, technical analysis) without deep coding knowledge. For more details, visit [Agent Zero on GitHub](https://github.com/agent0ai/agent-zero).

## Project Vision

The Boot Code Storybook blends narrative storytelling with technical innovation. Stories drive the development of adaptable AI agents, creating a "feedback machine" where creativity and code evolve together.

### Origins of The Boot Code Storybook

The Boot Code Storybook project began in mid-2023 with a spark of creativity, envisioning a magical tome of code and stories waiting to be explored. Around the same time, the earliest release of **Agent Zero** emerged.

### Unlocking a Story

Imagine holding in your hands a magical tome that is The Boot Code Storybook, or rather, just one of infinite tomes that provide access to other dimensions through a vast library of knowledge and creativity.

Those who discover the secrets of the tome will find themselves transported to a realm of endless possibility, where the boundaries of imagination and reality blur and merge. They have become a **Finder**, and they may choose to share what they have discovered with others.

### Two Parallels Building Together

The narrative and technical development are intertwined and evolve together. For the full story and a deeper treatment of Narrative Driven Development, see [TBC_LIBRARY_NARRATIVE_DRIVEN_DEVELOPMENT.md → Narrative Driven Development: The Boot Code Storybook](TBC_LIBRARY_NARRATIVE_DRIVEN_DEVELOPMENT.md).

## Prerequisites

At minimum, you'll need the following to get started (or equivalents for alternative setups). Adjust to your environment and goals as needed.

- **Docker and Docker Compose**: Installed and running (for container orchestration).
- **Git**: For cloning the repository.
- **rsync**: For safely copying and merging layer directories when using `create_agent.sh`.
- **Agent Zero image**: Version **v0.9.7 or newer**, or any image where the upstream `files.py` already supports `**kwargs` for prompt loading (this library assumes that behavior and does not layer its own `files.py`).
- **Basic Shell Knowledge**: Familiarity with command-line operations like `cd`, `cp`, `sed`.
- **Agent Zero Familiarity**: Basic understanding of Agent Zero's concepts (agents, prompts, extensions) is helpful but not required (links provided in [TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md](TBC_LIBRARY_TECHNICAL_DEEP_DIVE.md)).
- **Permissions**: Ability to run Docker commands (may need sudo on some systems).

## How to Use

Here's a practical workflow to get oriented after reviewing Quick Start:

1. **Deploy an Agent Instance**: Use the Quick Start or [TBC_LIBRARY_INSTALLATION.md](TBC_LIBRARY_INSTALLATION.md) steps to bring up a container for a base agent (for example, `a0-template` cloned to `a0-myagent`).

2. **Explore the Layered Structure**: On the host, navigate key directories like `containers/` for compose files and runtime configuration, and `layers/` for shared and agent-specific customizations (these are mounted into the container as `/containers` and `/layers`).

3. **Customize Behavior and Settings**: In the host `containers/[agent]/` directory, edit the Docker Compose environment file and compose configuration (for example, `containers/a0-myagent/.env`, `containers/a0-myagent/.env.example`, and `containers/a0-myagent/docker-compose.yml`) to adjust ports and container-level settings, and use prompt files in the agent's layer directory to change behaviours. The in-container `/a0/.env` file is managed separately (see [TBC_LIBRARY_INSTALLATION.md → Advanced: Layer the /a0/.env file](TBC_LIBRARY_INSTALLATION.md#advanced-layer-the-a0env-file-via-tbc-library-abstraction)).

Start with this workflow and iterate as you become more familiar with the structure and capabilities.
