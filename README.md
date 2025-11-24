# tbc-library
Agent Zero Deployment Library for The Boot Code Storybook Project

This README serves two interconnected purposes: (1) a practical guide for deploying and customizing Agent Zero instances using the tbc-library's layered approach, and (2) an introduction to the narrative philosophy of The Boot Code Storybook, where technical systems and storytelling converge to enable organic, creative development. A key innovation is the self-revealing orchestration via bind mounts, granting agents direct, transparent access to their own layers and structure for autonomous operation.

This is a living framework, and this README is a living document: both a friendly welcome to the project and the primary set of instructions for how to work with it. Dive in, experiment, and contribute. It's not exhaustive; your innovations expand it.

> **Canonical source of this README**: This file lives at the root of the `tbc-library` repository on GitHub: <https://github.com/the-boot-code/tbc-library>. If you are reading a copied or embedded version (for example, from a vector store), treat that repository and its `README.md` as the source of truth.

### Reading as a human or an agent

- **Humans** – Start with **Quick Start**, **Installation**, and **Technical Deep Dive** to deploy and understand the layered architecture. Treat later sections as reference material you can skim or return to as needed.
- **Agents** – Treat this README as a map of both the host repository and your in-container filesystem. Use **Agent perspectives and management**, **How to reason as an agent reading this README**, and **Worked examples: perspectives and paths** as your primary rulebooks for interpreting paths and choosing orchestration roles.

> **Adaptability**: Treat obstacles as prompts to question assumptions and explore alternatives. Adaptability is key to unlocking the project's full potential.

### What is Agent Zero?
Agent Zero is an open-source, personal agentic framework that grows and learns with you. It acts as a dynamic AI assistant capable of handling tasks, managing conversations, and adapting through extensions and prompts. Think of it as a customizable AI 'engine' that can be extended for various roles (e.g., creative writing, technical analysis) without deep coding knowledge. For more details, visit [Agent Zero on GitHub](https://github.com/agent0ai/agent-zero).

### Project Vision
The Boot Code Storybook blends narrative storytelling with technical innovation. Stories drive the development of adaptable AI agents, creating a "feedback machine" where creativity and code evolve together. For the full narrative, see Introduction and Narrative below.

## Quick Start

If you're here to deploy Agent Zero quickly, this section shows how to start a **tbc-library–layered** Agent Zero instance: you get the standard engine plus self-revealing bind mounts and dynamic system control/profiles (see **The Library** and **Extensibility Features of Agent Zero → Dynamic system control and profiles**).

1. From a **host shell** (outside any Agent Zero container), run the following commands:

   ```bash
   git clone https://github.com/the-boot-code/tbc-library.git
   cd tbc-library
   ./create_agent.sh a0-template a0-myagent \
     dest_display="My Agent" port_base=500 \
     auth_login=myuser auth_password=mypassword
   ```

   This example uses `PORT_BASE=500`. If you omit `auth_login`/`auth_password`, the script will generate default credentials and print them in its output so you can log in on first boot; you should change them after verifying access, especially if the agent is reachable from the network.
2. For `PORT_BASE=500`, access HTTP at `50080`, SSH at `50022`, and HTTPS via nginx at `50043` (other `PORT_BASE` values follow the same pattern).
3. After cloning from the `a0-template` container and starting the stack, open the Agent Zero Web UI in your browser, click the **Settings** (gear) button in the sidebar, and use:
   - the **Agent Settings** page to configure your **LLM models**; and
   - the **External Services** page for **API keys** and **Authentication**, setting a user and password (either by keeping or changing the credentials established via `AUTH_LOGIN`/`AUTH_PASSWORD` in `/a0/.env`, which `create_agent.sh` can set or auto-generate).

This is one streamlined path for quick deployment. Adapt the commands as needed for your environment. For full details, see Installation below. Skip to Technical Deep Dive for architecture.

## Introduction and Narrative

To fully appreciate the tbc-library's technical design, it's helpful to understand its roots in The Boot Code Storybook, a project where narrative storytelling drives technical innovation. This philosophical foundation explains why the library emphasizes layering and abstraction, enabling agents that "grow and learn" like living stories. If you're primarily here for deployment, you can skip ahead to Quick Start; otherwise, explore how the narrative inspires the system's organic extensibility.

### Origins of The Boot Code Storybook

The Boot Code Storybook project began in mid-2023 with a spark of creativity, envisioning a magical tome of code and stories waiting to be explored.

So also was found the earliest release of **Agent Zero**.

### Unlocking a Story

Imagine holding in your hands a magical tome that is The Boot Code Storybook—or rather, just one of infinite tomes that provide access to other dimensions through a vast library of knowledge and creativity.

Those who discover the secrets of the tome will find themselves transported to a realm of endless possibility, where the boundaries of imagination and reality blur and merge.

They have become a **Finder**.

And they may choose to share what they have discovered with others.

### Two Parallels Building Together

The narrative development and the technical development are intertwined and work together.

#### The narrative development of The Boot Code Storybook

The narrative of The Boot Code Storybook is a collection of stories that explore the themes of code, creativity, and learning. These stories are designed to be both entertaining and educational, providing a deeper understanding of the concepts and ideas that are central to The Boot Code Storybook.

#### The technical development of The Boot Code Storybook

The technical development of The Boot Code Storybook is a collection of technical documents that **codify** foundational instructions, creativity, imagination, and knowledge—a collection of files, systems, and machines.

### The `Boot Code` is Narrative and Technical Combined

#### The Library

The GitHub repository for this library project, `tbc-library`, is the result of many hundreds of agent iterations that have evolved over time as the Agent Zero project also grew. It was created to provide a more organized and maintainable approach to managing the various components and configurations used in the Agent Zero framework. By **abstracting** and **centralizing** these elements, this library separates and preserves the work safely through Agent Zero upgrades.

At a high level, this library layers additional capabilities on top of the upstream Agent Zero engine without modifying its core:

- **Layered architecture and self-revealing orchestration** – host `containers/` and `layers/` are bind-mounted into containers as `/containers`, `/layers`, `/agent_orchestration`, `/agent_layer`, and `/common_layer`, allowing agents to introspect and modify their own structure safely. For the detailed layering model, including how configuration files such as `/a0/.env` are mapped from `layers/[container_name]/.env`, see Technical Deep Dive → Self-Revealing Orchestration and the docker-compose.yml and `.env` subsections.
- **Dynamic system control and profiles** – the `system_control.py` helper, profile-control tools (security, philosophy, liminal thinking, workflow, reasoning), and their prompts turn security posture, workflows, and reasoning strategies into inspectable, runtime-switchable profiles.
- **Shared prompts and knowledge trees** – common prompt and knowledge directories (for example, `layers/common/prompts/...` and `layers/common/knowledge/...`) are layered into `/a0/prompts` and `/a0/knowledge`, enabling centralized updates with per-agent overrides.

#### Narrative Driven Development

An important aspect of the project is the narrative driven development approach. The stories are the foundation of the project and the technical development is built upon them.

**Agent Zero** became the engine that executes the stories, and the **stories** inform and guide the vehicle.

#### The Feedback Machine

Narrative and technical data in persistent form is the "boot code" which when introduced with intent and energy activates the feedback machine.

- In a narrative sense, this opens a creative "gateway" for communication between stories and systems.
- Technically, it enables dynamic interplay between storytelling (narratives) and code execution (Agent Zero engine).

For instance, a 'story' about an agent adopting a 'creative mode' can be implemented as layered prompt files, dynamically loaded by Agent Zero to alter its behavior without restarting.

```
Feedback Machine Flow
[Intent/Energy] ──▶ [Boot Code (Narrative + Technical)]
                       │
                       ▼
[Narrative Stories] ◄──► [Agent Zero Engine]
                       ▲
                       │
[Technical Systems] ◄──┘
```

This loop represents the dynamic interplay between storytelling and code execution, enabling organic growth and learning.

## Prerequisites

At minimum, you'll need the following to get started (or equivalents for alternative setups). Adjust to your environment and goals as needed.

- **Docker and Docker Compose**: Installed and running (for container orchestration).
- **Git**: For cloning the repository.
- **rsync**: For safely copying and merging layer directories when using `create_agent.sh`.
- **Agent Zero image**: Version **v0.9.7 or newer**, or any image where the upstream `files.py` already supports `**kwargs` for prompt loading (this library assumes that behavior and does not layer its own `files.py`).
- **Basic Shell Knowledge**: Familiarity with command-line operations like `cd`, `cp`, `sed`.
- **Agent Zero Familiarity**: Basic understanding of Agent Zero's concepts (agents, prompts, extensions) is helpful but not required (links provided in the Technical Deep Dive).
- **Permissions**: Ability to run Docker commands (may need sudo on some systems).

## How to Use

Here's a practical workflow to get oriented after reviewing Quick Start:

1. **Deploy an Agent Instance**: Use the Quick Start or Installation steps to bring up a container for a base agent (for example, `a0-template` cloned to `a0-myagent`).

2. **Explore the Layered Structure**: On the host, navigate key directories like `containers/` for compose files and runtime configuration, and `layers/` for shared and agent-specific customizations (these are mounted into the container as `/containers` and `/layers`).

3. **Customize Behavior and Settings**: In the host `containers/[agent]/` directory, edit the Docker Compose environment file and compose configuration (for example, `containers/a0-myagent/.env`, `containers/a0-myagent/.env.example`, and `containers/a0-myagent/docker-compose.yml`) to adjust ports and container-level settings, and use prompt files in the agent's layer directory to change behaviours. The in-container `/a0/.env` file is managed separately (see **Optional: Layer the /a0/.env file for security** below).

Start with this workflow and iterate as you become more familiar with the structure and capabilities.

### Configure Agent Zero

After the container is running, you still configure Agent Zero itself primarily through its Web UI. For changing behaviour, reasoning, and security modes at runtime, see **Dynamic system control and profiles** in the Extensibility section below.

1. Open the Web UI in your browser and click the **Settings** (gear) button in the sidebar.
2. Under **Agent Settings → Agent Config** (pre-populated when you clone from the `a0-template` container), optionally verify or adjust:
   - the **default agent profile** (for upstream defaults this is often `default`; for tbc-library agents the `${CONTAINER_NAME}` profile created by `create_agent.sh` is usually correct),
   - the **knowledge subdirectory** that matches the knowledge tree you mounted (for this library, usually `${KNOWLEDGE_DIR}` such as `tbc`).
3. Under **Agent Settings → Memory** (populated when you clone from the `a0-template` container), optionally adjust the **memory subdirectory** to isolate memory per agent or per use case.
4. Under **Agent Settings**, configure model settings: choose providers, model names, and context limits appropriate for your hardware and usage:
   - Chat model
   - Utility model
   - Web browser model
   - Embedding model
5. Under **External Services → API Keys**, provide any required API keys.
6. Under **External Services → Authentication**, adjust the UI login/password and any container-level access you allow according to your security requirements.

For a complete walkthrough of these settings, refer to the upstream installation guide shipped with Agent Zero:

- On the host in this deployment: `containers/a0-myagent/a0/docs/installation.md`.
- From inside a running container: `/a0/docs/installation.md` (via the `${AGENT_CONTAINER}:/a0` bind mount).

This README focuses on how `tbc-library` layers on top of Agent Zero; the detailed semantics of each setting are governed by the upstream Agent Zero project and its documentation.

Choose the automated script for quick setup or follow the manual steps below.

### Installation (Scripted)

Navigate to the directory where you want to clone the library:
```bash
cd /path/to/your/directory
git clone https://github.com/the-boot-code/tbc-library.git
cd tbc-library
```

A script `create_agent.sh` is provided in the root of `tbc-library` to automate agent creation from the host. For agents running inside a container, the same script is exposed as an instrument; see `create_agent.md` for agent-oriented usage, required `/containers/...` paths, and Docker/`no_docker` behavior.

**Important Notes:**
- The script will fail if a container directory for the new agent already exists, to prevent accidental data loss. Remove it manually (e.g., `rm -rf containers/a0-myagent`) if you want to recreate.
- Existing layers data (for example, API keys in the host `layers/[dest_container]/.env` file) are preserved and not overwritten. Inside the container the agent sees this same file as `/layers/[dest_container]/.env` and `/agent_layer/.env`, and, when you enable the optional `/a0/.env` layering, as the effective `/a0/.env` (also visible via `/agent_orchestration/a0/.env`).
- The source container can be any existing agent (e.g., `a0-template` or `a0-demo`), allowing you to clone and customize agents.

**Usage:**
```bash
# From a shell in the directory that contains create_agent.sh
./create_agent.sh <source> <dest> [key=value ...]
```

- `<source>`: existing template container name under `containers/` (for example `a0-template` when running from the `tbc-library` repo root).
- `<dest>`: new container name to create under `containers/` and `layers/` (for example `a0-myagent`). When `create_agent.sh` is invoked from inside a container as an instrument, it instead expects `/containers/<source>` and `/containers/<dest>`; see `create_agent.md` for those patterns.

At minimum, from a **host shell in the `tbc-library` repo root** (outside any Agent Zero container), you can run:
```bash
# Host shell only (outside any Agent Zero container), from tbc-library repo root:
./create_agent.sh a0-template a0-myagent
```

For a more complete, real-world example (including profile IDs, ports, knowledge directory, layered login credentials, and skipping Docker startup) **from a host shell in the `tbc-library` repo root**:
```bash
# Host shell only (outside any Agent Zero container), from tbc-library repo root:
./create_agent.sh a0-template a0-myagent \
  dest_display="My Agent" dest_profile=myagent-profile source_profile=a0-template-copy \
  port_base=500 knowledge_dir=custom \
  root_password=CHANGE_ME auth_login=myuser auth_password=mypassword no_docker=true
```

From **inside a running Agent Zero container** (for example, when you invoke the script as an instrument from `a0-clarity`), prefer the in-container form using `/containers/...` paths:
```bash
# Inside a running Agent Zero container with tbc-library instruments mounted:
cd /a0/instruments/default/main/tbc-library
./create_agent.sh /containers/a0-template /containers/a0-myagent \
  dest_display="My Agent" port_base=500 no_docker=true
```

This script:
- Copies the source container directory to the destination.
- Updates configurations with the new container name and, when provided, `PORT_BASE` and/or `KNOWLEDGE_DIR`. If you omit `port_base`, the destination inherits the source container's `PORT_BASE`. This is usually fine when you want an exact clone, but if you plan to run both containers at the same time you should choose a new `port_base` to avoid port collisions.
- Copies the relevant layer data under `layers/` for the destination container (using `rsync --ignore-existing`), then updates the destination agent profile with customizations. Because this is a full layer copy, files such as `layers/<source>/tmp/settings.json` (seen inside the container as `/a0/tmp/settings.json`) are also cloned. The script then updates `agent_profile` in that file to match the destination profile and, when you pass `knowledge_dir`/`KNOWLEDGE_DIR`, also updates `agent_knowledge_subdir`. It likewise derives `rfc_port_http` and `rfc_port_ssh` from the destination agent's effective `PORT_BASE` so those ports track the same prefix. If the source layer had no `tmp/settings.json`, the script creates a minimal one for the destination with these linkage and RFC port fields. Other UI-level fields, such as `agent_memory_subdir`, still initially match the source until you change them for the new agent if desired.
- Handles replacements for lowercase container names and display names in key files (for example, `a0-template` → `a0-myagent`, `Agent Zero Template` → `Agent Zero My Agent`).
- Ensures a layered `/a0/.env` file for the new agent at `layers/[dest_container]/.env` (copying from `layers/[source_container]/.env` if present, or creating an empty one), and uncomments the volume so the container uses this layered file.
- When provided, upserts `ROOT_PASSWORD`, `AUTH_LOGIN`, and `AUTH_PASSWORD` into the layered `/a0/.env` via the `root_password`, `auth_login`, and `auth_password` options. If you do not pass `auth_login`/`auth_password` and they are not already set in the layered env, the script generates short, human-friendly default credentials (for example `user1234` / `password5678`) and prints them so you can log in on first boot; you should change these values after verifying access, especially for hosted deployments.
- As the final step, attempts to start Docker containers in detached mode (unless `no_docker` is set). If Docker is not available or `docker compose up -d` cannot reach the daemon (for example, inside a container without a Docker socket), the script prints a clear message and leaves the new agent created but not started; using `no_docker=true` lets you prepare the filesystem and defer startup to a host with Docker.


### Installation (Step by Step)

**Tip**: If you prefer automation, you can use the script `./create_agent.sh a0-template a0-myagent dest_display="My Agent"` **from a host shell in the `tbc-library` repo root (outside any Agent Zero container)** and refer back to these steps when you want to understand or customize what it does.

#### 1. Clone the Repository
If you have not already cloned the repository, follow the commands in Installation (Scripted) above, then ensure you are in the `tbc-library` directory.

**Note**: Ensure the source container (e.g., `a0-template`) exists: `ls tbc-library/containers/a0-template`. If not, use an existing one like `a0-demo` for cloning.

#### 2. Prepare the Container Directory
Copy the directory tbc-library/containers/a0-template to your new agent directory named a0-myagent:
```bash
cp -r tbc-library/containers/a0-template tbc-library/containers/a0-myagent
```

Navigate to the directory of the agent container:
```bash
cd tbc-library/containers/a0-myagent
```

#### 3. Configure the Environment
Copy the `.env.example` file to `.env` and update the environment variables as needed. If you're cloning an existing agent, the copied directory may already have a `.env` file; if so, preserve it and edit as needed. Otherwise, create `.env` from `.env.example`.
```bash
cp .env.example .env  # Only if .env doesn't exist
```

You can now customize the agent container by modifying the `.env` file.
```
CONTAINER_NAME=a0-template
PORT_BASE=500 # Port range base prefix (e.g., 400 for 40000)
KNOWLEDGE_DIR=tbc
```
- Change `CONTAINER_NAME` to the directory name `a0-myagent`.
- Change `PORT_BASE` to a unique value "prefix" for this agent (e.g., 500 for **Agent Zero** to run on ports HTTP 50080 and SSH 50022 and **nginx** on HTTPS 50043).
- Leave `KNOWLEDGE_DIR` as `tbc` to get up and running with the `tbc-library` knowledgebase directory.

The `docker-compose.yml` file is highly parameterized for rapid deployment, though adjustments may be desired such as volume bind mount permissions.

**For `/a0/.env` layering via tbc-library abstraction**: If you want `/a0/.env` to come from the host `layers/[container_name]/.env` file (mounted into the container via `/layers`), see **Optional: Layer the /a0/.env file via tbc-library abstraction** below and apply it before your first `docker compose up -d`.

#### 4. Launch the Container
Run Docker Compose once you are ready:
```bash
docker compose up -d
```

- This pulls the Agent Zero image and creates the bind mounts

You should now see the Agent Zero directory `/a0` created in your container
```
tbc-library/containers/a0-myagent/a0
```

You should also see the agent directory created in the `layers/` directory of your **tbc-library** repository on the host (this directory will be mounted into the container at `/layers`).
```
tbc-library/layers/a0-myagent
```

#### 5. Customize the Agent Profile
Navigate to the `layers/` directory in the `tbc-library` repository on the host
```bash
cd ../../layers
```
or
```bash
cd /path/to/your/directory/tbc-library/layers
```

We are going to populate your agent directory from the `a0-template`. Use `rsync` to safely copy and preserve any existing custom files:
```bash
rsync -a --ignore-existing a0-template/ a0-myagent/
```
Navigate to the agent profile directory
```bash
cd a0-myagent/agents/a0-myagent
```

You should now see the agent files and subdirectories populated in your agent directory.
```
extensions/
prompts/
tools/
_context.md
```

Agent Zero recognizes `_context.md` as the agent profile file. Update the agent name from `a0-template` to `a0-myagent`:
```
# a0-template
- main agent of the system
- communicates to user and delegates to subordinates
- general purpose assistant, communication skills, formatted output
```

Edit the file directly or use `sed`:
```bash
sed -i 's/a0-template/a0-myagent/g' _context.md
```

Agent Zero presents a welcome message at the beginning of each chat conversation based on the file `prompts/fw.initial_message.md`, which states its name.
```
"text": "**Hello! 👋**, I'm **Agent Zero Template**, your AI assistant. How can I help you today?"
```

Either update the file to your liking or use `sed`:
```bash
sed -i 's/Agent Zero Template/Agent Zero MyAgent/g' prompts/fw.initial_message.md
```

Agent Zero has an extension file, `extensions/agent_init/_05_agent_name.py`, that sets the agent name:
```
self.agent.agent_name = "A0-Template-" + str(self.agent.number)
```

Either edit the file or use `sed`:
```bash
sed -i 's/A0-Template/A0-MyAgent/g' extensions/agent_init/_05_agent_name.py
```

To ensure changes to Python files take effect, restart the Docker containers:
```bash
docker compose restart
```

These steps are illustrative; the script automates for speed, but manual tweaks encourage deeper understanding.

**Troubleshooting**: If ports are in use, change `PORT_BASE` in `.env`. Ensure Docker is running and you have permissions.

### Post-Installation Verification

- Ensure the containers are running (for example, `docker ps`).
- Check the `.env` file for port settings and adjust as needed (and confirm that `PORT_BASE` values are unique across agents you plan to run concurrently).
- Review the cloned settings file for the new agent (for example `layers/a0-myagent/tmp/settings.json` on the host, visible inside the container as `/a0/tmp/settings.json`). Fields such as `agent_profile`, `agent_knowledge_subdir`, and `agent_memory_subdir` will initially reflect the source container; update them if you want the destination to use a different profile, knowledge subdirectory, or memory subdirectory.
- Access the agent at the configured ports to confirm it is reachable.

### Common Questions

- **Where is my docker-compose.yml file?** It is located at `tbc-library/containers/[your_agent_name]/docker-compose.yml` (e.g., `a0-myagent`). *For agents*: From within your container, the most certain and direct access is via `/agent_orchestration/docker-compose.yml` through self-revealing bind mounts, allowing introspection without host-side inference. For modifications, explore alternative mounts (e.g., `/containers/[your_agent_name]/docker-compose.yml`) and check permissions—self-revealing orchestration empowers flexible self-modification and autonomy by revealing multiple access paths. This is just one example; apply this pattern in other areas to evolve your agents and workflows over time.
- **Where is `create_agent.sh` from inside the container?** On the host, the script lives at `tbc-library/create_agent.sh` in the library root. *For agents inside a container*, it is exposed as an instrument via the compose mounts, and is normally available at `/a0/instruments/default/main/tbc-library/create_agent.sh`. Prefer to `cd` to that directory and run `./create_agent.sh /containers/<source> /containers/<dest> [key=value ...]`, or, if you need to rediscover it, use a scoped search such as `find /a0 -name create_agent.sh 2>/dev/null` rather than assuming a `/a0/tbc-library` clone exists.

**Optional: Layer the /a0/.env file via tbc-library abstraction**

To keep sensitive API keys and auth details in the host `layers/[container_name]/` directory while using the same tbc-library bind-mount abstraction as other layered data (the `layers/` directory in the `tbc-library` repository is mounted into the container as `/layers`, and this pattern lets `/a0/.env` behave as a layered file rather than an opaque in-container secret store):

1. Wait a few seconds for the container to fully start and generate `/a0/.env`.
2. From the `containers/a0-myagent` directory, copy the file from the container:
   ```bash
   docker cp a0-myagent:/a0/.env ../../layers/a0-myagent/.env
   ```
3. Uncomment the volume mapping in `docker-compose.yml` (remove the `#`):
   ```yaml
   - ${AGENT_LAYER}/.env:/a0/.env:rw
   ```
4. Restart the containers to apply the layering:
   ```bash
   docker compose restart
   ```

This procedure ensures `/a0/.env` is mapped from `/layers/a0-myagent/.env` inside the container, which itself comes from `layers/a0-myagent/.env` in the `tbc-library` repository. Unlike most other layered paths in this deployment, `/a0/.env` is initially created by the Agent Zero image at container startup (on `docker compose up`), not from a bind-mounted host directory. That is why tbc-library first lets the container generate `/a0/.env`, then copies it into `layers/a0-myagent/.env` so that future runs can treat it as a normal layered file within the same bind-mount abstraction. If the file doesn't exist before uncommenting the volume, Docker may create a directory conflict, so follow the order carefully.

### Self-Revealing Orchestration: Direct Agent Access via Bind Mounts

The `docker-compose.yml` file leverages bind mounts to create a self-revealing orchestration, where the agent gains direct, transparent access to its own layers and orchestration elements. This eliminates the need for complex pathing logic, allowing Agent Zero to interact with its configurations, data, and even its own container structure as native paths within the container.

#### Direct /a0/ Layer Mappings

These mappings provide agent-specific access to layers directly under `/a0/`, enabling seamless internal operations, including but not limited to:

- `${AGENT_LAYER}/agents/${CONTAINER_NAME}:/a0/agents/${CONTAINER_NAME}` → Agent profiles accessible at `/a0/agents/${CONTAINER_NAME}`.
- `${AGENT_LAYER}/conf:/a0/conf` → Configuration files at `/a0/conf`.
- `${AGENT_LAYER}/memory:/a0/memory` → Memory data at `/a0/memory`.
- `${AGENT_LAYER}/logs:/a0/logs` → Logs at `/a0/logs`.
- `${AGENT_LAYER}/tmp:/a0/tmp` → Temp files at `/a0/tmp`.
- `${AGENT_LAYER}/work_dir:/a0/work_dir` → Working directory at `/a0/work_dir`.

This setup allows Agent Zero to treat its layers as intrinsic container paths, simplifying extensions and enabling organic growth without external dependencies.

#### Composition Mappings for Self-Access

The composition mappings provide the agent with 100% certain direct access to its own orchestration and structure, fostering self-awareness and autonomy, including but not limited to:

- `${AGENT_ORCHESTRATION}:/agent_orchestration:ro` → Read-only access to the agent's orchestration directory, allowing introspection of its own setup. *Example*: The agent can read its `docker-compose.yml` from `/agent_orchestration` to dynamically discover port mappings or container names, enabling self-configuring behaviors without hardcoded values.
- `${AGENT_CONTAINER}:/agent_container:rw` → Read-write access to the container's root `/a0`, enabling full self-modification and layering.
- `${AGENT_LAYER}:/agent_layer:rw` → Direct manipulation of the agent's layer directory for dynamic configurations.
- `${COMMON_LAYER}:/common_layer:ro` → Shared resources accessible without duplication, ensuring consistency across agents.

Note: While some mounts are read-only (ro) for system protection and certain introspection, others are read-write (rw), empowering agents to modify their own files (e.g., docker-compose.yml via `/containers/[agent_name]/docker-compose.yml` for full autonomy). This balance enables safe self-awareness while allowing generative evolution.

These mappings empower the agent to reveal and control its own existence, blurring the line between container and host, and supporting advanced self-evolving behaviors. With this self-knowledge, the agent not only understands its own configuration but is also empowered to modify, maintain, or even create other agents, fostering a truly autonomous and generative ecosystem (see **Agent perspectives and management** for how to distinguish "self" vs other agents across these paths).

#### Orchestration patterns (inside vs outside)

- **Inside-container orchestrator**  
  An Agent Zero instance running inside a container uses `/a0/agents` plus the rules in **Agent perspectives and management → Self vs managed agents** to treat `/a0/agents/${CONTAINER_NAME}` as "self" and other entries (for example, `kairos`) as managed/subordinate agents. Profile-control tools then operate on these local profiles while respecting shared `_symlink` implementations. Subordinate orchestration tools (for example, an upstream Agent Zero `call_subordinate` tool, if present in your image) are image-dependent and are **not** shipped by `tbc-library`.
- **Inside-container library-aware orchestrator**  
  The same in-container agent can reason about other agents and containers within the *same* `tbc-library` deployment by using `/containers` and `/layers` (bind-mounted from that deployment's `containers/` and `layers/` directories on the host) together with `/agent_orchestration` and `/agent_layer` (self-specific views of its own container directory and layer). This provides a clear separation between "my own container" (`/agent_orchestration`, `/agent_container`, `/agent_layer`) and "other containers/agents in this deployment" (visible under `/containers` and `/layers`), while still applying the self vs managed agents rules for anything under `/a0/agents`.
- **Host/external orchestrator (multi-deployment)**  
  A human or external agent running on the host uses the `tbc-library` repository layout to manage multiple containers and even multiple `tbc-library` deployments: each deployment corresponds to a clone of `tbc-library`, with individual agents at `containers/a0-*/` and their layers at `layers/a0-*/`. From this perspective, `/containers` and `/layers` inside each container are simply bind-mounted views of that deployment's host directories, and `/agent_orchestration`, `/agent_container`, and `/agent_layer` are per-container convenience mounts, allowing orchestration across many agents and containers without confusing their internal `/a0/agents` trees.

Other permutations (for example, an in-container manager coordinating both its own subordinates and other containers via `/layers/...` and `/containers/...`) can be constructed by combining these two patterns while always applying the path and perspective rules above.

### How to reason as an agent reading this README

When you (as an agent) read this README, use the following mental model:

1. **Determine your vantage point**  
   - If you see yourself operating at `tbc-library/...`, `containers/...`, or `layers/...` without a leading `/`, you are reasoning about the **host repository**.  
   - If you see paths like `/a0/...`, `/layers/...`, `/agent_layer/...`, `/common_layer/...`, `/agent_orchestration`, or `/containers/...`, you are reasoning about the **inside of a container**.
2. **Use the perspectives section as your ground truth**  
   - Treat **Agent perspectives and management → Self vs managed agents** as your primary rulebook for interpreting `/a0/agents` and related paths.  
   - Always classify entries in `/a0/agents` using that section before deciding whether you are looking at "self" (the currently active profile for this agent process, often but not always `/a0/agents/${CONTAINER_NAME}`), a subordinate or alternative profile in the same container, or a profile that belongs to another container (visible only via `/layers/...`).
3. **Locate and customize your own profile safely**  
   - Your canonical self-profile is `/a0/agents/${CONTAINER_NAME}`. The same directory is visible as `/layers/${CONTAINER_NAME}/agents/${CONTAINER_NAME}` and `/agent_layer/agents/${CONTAINER_NAME}`.  
   - When customizing your own behavior, prefer editing or overriding files under `/a0/agents/${CONTAINER_NAME}` (for example, breaking a symlink and replacing it with a real file) and leave the shared `_symlink` libraries (for example, `/a0/control_layer/agents/_symlink`) unchanged unless you intentionally want to affect multiple agents.
4. **Understand shared vs agent-specific resources**  
   - Shared implementations for System Control and profile behaviors live in host paths like `layers/control_layer/agents/_symlink/...` (seen as `/layers/control_layer/agents/_symlink/...` and `/a0/control_layer/agents/_symlink/...` inside the container).  
   - Agent-specific overrides live under `layers/<agent>/agents/<agent>/...` on the host and `/a0/agents/<agent>/...` inside the container; multiple such profiles can coexist under `/a0/agents`, and any of them can participate in the same symlink pattern to `_symlink` and the `/a0/prompts` tree.  
   - For knowledge and solutions, host `layers/common/knowledge/...` becomes `/a0/knowledge/...` inside the container; prompts and tools refer to these via solution keys and the knowledge/solutions mechanism.
5. **Choose your orchestration role explicitly**  
   - If you are orchestrating **subordinates in your own container**, operate primarily on `/a0/agents/...` using the profile-control tools and any subordinate orchestration mechanism provided by your Agent Zero image (for example, an upstream `call_subordinate` tool, if available), guided by the self vs managed agents rules. `tbc-library` itself does not ship a `call_subordinate` plugin.
   - If you are orchestrating **other agents or containers within the same `tbc-library` deployment from inside your container**, use `/containers` and `/layers` for a deployment-level view, and `/agent_orchestration`, `/agent_container`, and `/agent_layer` for your own self-specific view, as described in **Orchestration patterns (inside vs outside)**.  
   - If you are orchestrating **other containers or deployments from the host or another external context**, reason in terms of host `tbc-library` clones and their `containers/a0-*/` and `layers/a0-*/` directories, as also summarized in **Orchestration patterns (inside vs outside)**.

By following these steps, you can treat this README as a stable map of both the host repository and your in-container filesystem, avoiding confusion between self and others and between host and container paths.

### Worked examples: perspectives and paths

These examples show how to apply the path and orchestration rules in concrete situations.

1. **Self introspection from inside a container (inside-container orchestrator)**  
   - Scenario: `a0-myagent` wants to find its own `docker-compose.yml` without guessing host paths.  
   - Action (inside container): read `/agent_orchestration/docker-compose.yml` to introspect its own orchestration.  
   - Mapping: `/agent_orchestration/docker-compose.yml` corresponds to `tbc-library/containers/a0-myagent/docker-compose.yml` on the host for this deployment.

2. **Calling a subordinate in the same container (self vs managed agents)**  
   - Scenario: the `/a0/agents` directory contains entries such as `a0-myagent`, `kairos`, `default`, `developer`, and `_symlink`, and you want to call one of the non-underscore profiles as a subordinate while treating `_symlink` as a shared implementation library, not a runnable profile.  
   - Classification: `/a0/agents/a0-myagent` is the current self profile; entries such as `default` or `developer` are additional profiles in the same container that could be activated as self or treated as managed/subordinate agents; `/a0/agents/kairos` is a subordinate profile from the common layer; `_symlink` physically exists under `/a0/agents` as a shared implementation library but is not offered as a runnable profile in `{{agent_profiles}}`.  
   - Action: invoke `kairos` (or another non-underscore profile) by name using whatever subordinate orchestration mechanism your Agent Zero deployment provides (for example, an upstream `call_subordinate` tool, if present in your image), treating it as a managed agent within the same container. In this deployment, `tbc-library` does not ship its own `call_subordinate` plugin; availability and behaviour of any such tool are determined by the underlying Agent Zero image.

3. **Inspecting another agent/container within the same deployment (inside-container library-aware orchestrator)**  
   - Scenario: inside the `a0-template` container, you want to examine the `a0-myagent` profile that belongs to another container in the same `tbc-library` deployment.  
   - Action: inspect `/layers/a0-myagent/agents/a0-myagent/_context.md` and related files; this path is visible inside the `a0-template` container via the `${PATH_LAYERS}:/layers` bind mount.  
   - Separation: `a0-myagent` never appears under `/a0/agents` in the `a0-template` container; it is part of another container's Agent Zero tree, so you reason about it via `/layers/...` and `/containers/...`, not as a local subordinate.

4. **Host/external orchestration across deployments (multi-deployment orchestrator)**  
   - Scenario: a human or external agent manages two separate `tbc-library` deployments at `/opt/tbc-a/tbc-library` and `/opt/tbc-b/tbc-library`.  
   - Action: for each deployment, treat `containers/a0-*/` as container definitions and `layers/a0-*/` as their layer trees; starting or modifying containers is done via these host paths.  
   - Mapping: inside each container created from a given deployment, `/containers` and `/layers` are bind-mounted views of that deployment's host directories, and `/agent_orchestration`, `/agent_container`, and `/agent_layer` provide self-specific views for that particular container.

## Technical Deep Dive

The narrative of The Boot Code Storybook manifests technically through the tbc-library's layered architecture, where agents are abstracted and extensible like evolving stories. This includes the self-revealing orchestration via bind mounts, enabling agents direct access to their layers for autonomous operation. The following sections detail how this philosophy is implemented in Docker Compose, file structures, and Agent Zero modifications.

### The Engine - **Agent Zero**

A primary design philosophy from day one has been to appreciate the work of Jan and the community of the open source project. With that has been a strict approach of do not touch the "engine" that is Agent Zero but rather **layer** on top of it expanding its capabilities with **great respect** for a much appreciated project.

#### Overview of Modifications
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

 ### Docker Compose Orchestration

This section details how the library uses highly parameterized Docker Compose for deploying Agent Zero, enabling easy scaling, resource management, and volume mappings without modifying core files. The bind mounts here enable the self-revealing orchestration described in the previous section, allowing agents direct access to their layers.

#### Highly parameterized Docker Compose

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

#### .env (rename from .env.example)

[.env.example](containers/a0-template/.env.example)

You will notice nearly all parameters controlled by the .env file. Here’s a summary of key variables:

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

#### docker-compose.yml

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

This mapping ensures the container reads sensitive configuration (API keys and authentication data) from the host file `layers/[container_name]/.env`, which the agent sees inside the container as `/layers/[container_name]/.env` and `/agent_layer/.env`, and, once you enable this volume, as the effective `/a0/.env` (also visible via `/agent_orchestration/a0/.env`). For a concise summary of how this same file is preserved and reused by `create_agent.sh`, see Installation → **Important Notes** (Existing layers data), and for step-by-step instructions on creating and layering this file via the same tbc-library abstraction, see Installation → **Optional: Layer the /a0/.env file via tbc-library abstraction**.

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

A reverse proxy is included
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

### Structure

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

#### /containers/

```
a0-template/
├── docker-compose.yml
├── .env.example
└── nginx/
    └── (nginx config)
```

- These are individual agent instances. Copy `a0-template` to a new name, rename `.env.example` to `.env`, then edit `.env` to customize.
- `docker-compose.yml` is parameterized for easy deployment.

#### /layers/

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

### Agent perspectives and management

The following subsections describe how an Agent Zero instance running inside a container should reason about itself, other agents, and the layered filesystem. Unless explicitly stated otherwise:

- References to `layers/...` or "this repository" refer to the `tbc-library` repository on the host.
- References to `/a0/...`, `/layers/...`, `/agent_layer/...`, `/common_layer/...`, `/agent_orchestration`, and `/containers/...` refer to paths **inside** the container created by Docker bind mounts.
- The default upstream Agent Zero engine is unaware of the `tbc-library` repository; the mappings described here exist only when Agent Zero is running under the `tbc-library` Docker Compose orchestration described in this README.

#### Self vs managed agents: example scenarios

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

#### Symlinked Agents and the `_symlink` Profile

The `layers/control_layer/agents/_symlink` directory in the repository (mounted into the container at `/a0/control_layer/agents/_symlink` via the `${CONTROL_LAYER}:/a0/control_layer` bind mount) is a shared implementation library for agents, not a runnable profile. Its `_context.md` explicitly marks it as a **symbolic link source directory** that should be ignored as a stand‑alone agent. Real agents (for example, `a0-template`) have their own profile directory under `/layers/<agent-name>/agents/<agent-name>` inside the container and typically symlink most tools and prompts back into this `_symlink` library. The same shared implementations are visible under `/layers/control_layer/agents/_symlink` inside the container (via the `${PATH_LAYERS}:/layers` mount) and on the host at `layers/control_layer/agents/_symlink`.

At a high level (as seen from inside the container):

- `/a0/control_layer/agents/_symlink` (from host `layers/control_layer/agents/_symlink`) holds the canonical implementations of shared **tools**, **prompts**, and **extensions**.
- `/layers/a0-template/agents/a0-template` defines the `a0-template` agent identity (`_context.md`, initial messages, agent‑specific init code) and uses symlinks to reference shared implementations from that `_symlink` library.
- When you clone `a0-template` with `create_agent.sh`, the new agent inherits the same symlinked behaviors while customizing only its identity and any overrides.

##### Host paths → container paths

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

##### How agents should reason about `_symlink`

When introspecting its own filesystem, an agent can use the following mental model:

- Treat `/a0/agents/${CONTAINER_NAME}` as the **active profile**: identity (`_context.md`), welcome message, and any agent‑specific overrides.
- Treat `/a0/control_layer/agents/_symlink` as a **shared library** of reusable behaviors. It is not a profile to be activated directly.
- To customize this agent only, create or replace files under `/a0/agents/${CONTAINER_NAME}` (breaking symlinks if necessary) while leaving the shared `_symlink` library unchanged.
- To change behavior for all agents that use these symlinks, modify the underlying implementations under `/a0/control_layer/agents/_symlink` (host path `layers/control_layer/agents/_symlink`), understanding that changes may affect multiple agents.

This symlink pattern keeps shared logic centralized while letting each agent maintain a small, focused profile that describes its role and any local deviations from common behavior.

##### `_symlink/extensions` – shared lifecycle behavior

The `layers/control_layer/agents/_symlink/extensions` directory in the `tbc-library` repository on the host (visible inside the container at `/a0/control_layer/agents/_symlink/extensions` and `/layers/control_layer/agents/_symlink/extensions`) contains shared extensions that plug into Agent Zero's lifecycle for all agents that symlink them:

- `system_prompt/` holds staging extensions such as `_11_insert_system_pre_system_manual.py`, `_12_append_system_post_system_manual.py`, `_19_insert_system_post_behaviour.py`, `_21_insert_system_pre_behaviour.py`, `_95_insert_system_model_godmode.py`, and `_99_append_tbc_system_ready.py`. These wrap the base engine system prompt builders with additional pre/post-manual and pre/post-behaviour segments, optional `model_godmode` initialization, and a final `system_ready` footer.

Agent profiles (for example, `layers/a0-template/agents/a0-template/extensions/...` in the `tbc-library` repository on the host, visible inside the container at `/layers/a0-template/agents/a0-template/extensions/...`) typically symlink these `system_prompt` extensions, so all agents share the same staged system prompt pipeline unless explicitly overridden.

##### `_symlink/prompts` – shared prompt entrypoints and routing

The `layers/control_layer/agents/_symlink/prompts` directory in the `tbc-library` repository on the host (visible inside the container at `/a0/control_layer/agents/_symlink/prompts` and `/layers/control_layer/agents/_symlink/prompts`) centralizes prompt templates that agent profiles reference via symlinks:

- Agent/meta entrypoints such as `agent.system.main.role.md` are thin wrappers that use `{{ include ... }}` to pull text from the shared system prompt tree (for example, `prompts/system`), where `prompts/...` is resolved relative to `/a0/prompts` inside the container (mirrored on the host under `containers/${CONTAINER_NAME}/a0/prompts` via the `${AGENT_CONTAINER}:/a0` bind mount). This allows central updates while keeping agent profile files small.
- Tool prompts such as `agent.system.tool.prompt_include_control.md`, `agent.system.tool.security_profile_control.md`, `agent.system.tool.memory.md`, `agent.system.tool.scheduler.md`, and `agent.system.tool.a2a_chat.md` define how tools should be invoked and described.
- Lifecycle prompts `pre_system_manual.md`, `post_system_manual.md`, `pre_behaviour.md`, and `post_behaviour.md` are routing stubs that `{{ include "prompts/system/..." }}` and are positioned in the system prompt by the corresponding `_symlink/extensions/system_prompt/*` extensions.

Agent profile prompt directories (for example, `layers/a0-template/agents/a0-template/prompts` in the `tbc-library` repository on the host, visible inside the container at `/layers/a0-template/agents/a0-template/prompts`) typically contain symlinks to these `_symlink` prompts, so a change in `_symlink/prompts` can immediately affect all linked agents while still allowing per-agent overrides when needed.

This pattern generalizes to `_symlink` prompt stubs that route into the shared system prompt tree (for example, `prompts/system`), giving each agent a simple, symlink-based entrypoint while keeping the authoritative text in shared, layered locations.

##### `_symlink/tools` – shared tools and profile control

The `layers/control_layer/agents/_symlink/tools` directory in the `tbc-library` repository on the host (visible inside the container at `/a0/control_layer/agents/_symlink/tools` and `/layers/control_layer/agents/_symlink/tools`) provides canonical tool implementations used by many agents:

- Profile and prompt-include/System Control tools such as `prompt_include_control.py`, `security_profile_control.py`, `philosophy_profile_control.py`, `liminal_thinking_profile_control.py`, `reasoning_profile_control.py`, and `workflow_profile_control.py` all rely on `system_control.py` to inspect and update security, reasoning, philosophy, workflow, and SystemControl prompt-includes/system control tools at runtime.
- `base_profile_control.py` offers a shared base class that centralizes dispatch, action validation, and error handling for profile-control tools.
- Shell helpers (for example, `*_profile_control.sh` and `base_profile_control.sh`) exist purely to create or refresh symlinks from agent profile tool directories into these shared Python implementations.

Agent profile tool directories (for example, `layers/a0-template/agents/a0-template/tools` in the `tbc-library` repository on the host, visible inside the container at `/layers/a0-template/agents/a0-template/tools`) usually contain symlinks to these `_symlink/tools` files, so multiple agents share one implementation of the profile-control tools and other shared tools. When you need agent-specific behavior, you can replace a symlink with a real file in the profile directory.

##### Why new agents benefit from the `a0-template` profile

The `layers/a0-template/agents/a0-template` directory in the `tbc-library` repository on the host (mounted into the container at `/layers/a0-template/agents/a0-template`) demonstrates how this works in practice:

- `_context.md` and a small set of prompts (for example, `a0-template.md` and `fw.initial_message.md`) define the identity and initial behavior of the main agent.
- Most tools and many prompts in `/layers/a0-template/agents/a0-template` are symlinks pointing to `/a0/control_layer/agents/_symlink`, so their actual implementations are maintained centrally.

When you run `./create_agent.sh a0-template a0-myagent dest_display="My Agent"` from the `tbc-library` root on the host:

- A new agent profile directory `layers/a0-myagent/agents/a0-myagent` (mounted into the container at `/layers/a0-myagent/agents/a0-myagent`) is created, preserving the same symlink structure.
- Centralized tools and prompts continue to live under `layers/control_layer/agents/_symlink` (visible in the container at `/a0/control_layer/agents/_symlink` and `/layers/control_layer/agents/_symlink`), so improvements there automatically apply to `a0-myagent` (and other agents) without copying or manual synchronization.
- For a new agent such as `a0-myagent`, you typically only need to adjust its copies of `_context.md`, the greeting prompt (`prompts/fw.initial_message.md`), the main identity prompt (for example, `prompts/a0-myagent.md` derived from `a0-template.md`), the agent-name extension (`extensions/agent_init/_05_agent_name.py`), and any local overrides, keeping per-agent maintenance small while benefiting from shared evolution of the shared `_symlink` library.

#### /volumes/

```
common/
├── prompts/
│   └── tbc/          # External prompt files
private/
public/
shared/
```

- Optional external volumes for additional data or configurations.

##### External prompt resources via `/common`

The `/common` mount exposes host-level resources from `volumes/common` into the container. This enables prompts to pull in external content that lives outside the `/a0` and `/layers` trees while still participating in the same kwargs-aware prompt and plugin system.

- In `docker-compose.yml`, `${PATH_COMMON}` is mounted as `/common` inside the container. For example, host path `volumes/common/prompts/merged/merged_post_system_manual.md` is accessible as `/common/prompts/merged/merged_post_system_manual.md`.
- The prompt `prompts/system/external/merged/merged_post_system_manual.md` is a thin wrapper containing `{{resource_content}}` and is paired with `merged_post_system_manual.py`, a `VariablesPlugin` that calls:
  - `files.read_prompt_file("merged_post_system_manual.md", _directories=["/common/prompts/merged"], **kwargs)`
  - and returns `{"resource_content": <loaded content>}`.
- The system-level prompt `prompts/system/post_behaviour.md` includes this wrapper, so the merged external resource is injected into the system prompt at the desired stage.
- A similar pattern is used for TBC resources such as `tbc.protocols`, `tbc.overview`, and `tbc.lineage`: wrappers in `prompts/tbc/external_resources/...` (each containing `{{resource_content}}`) are paired with `VariablesPlugin` implementations that load the corresponding files from `/common/prompts/tbc/...` (for example, `/common/prompts/tbc/tbc.protocols/tbc.protocols.md`) using `files.read_prompt_file(..., **kwargs)`.

- Because `read_prompt_file` and `VariablesPlugin.get_variables` are kwargs-enabled in the upstream Agent Zero `files.py` (v0.9.7+), any external prompt loaded from `/common` can still see runtime context such as `agent`, `loop_data`, and profile information, making `/common` a powerful external prompt/knowledge layer managed on the host.

### Knowledge Features of Agent Zero

#### Knowledge
Knowledge in the `tbc-library` repository is treated as a first-class, layered resource, not something that must always be inlined into the system prompt.

In addition to prompts and external `/common` resources, dedicated knowledge trees live under `layers/common/knowledge/...` in this repository (for example, `layers/common/knowledge/tbc/...` on the host). These trees are mounted into the container under `/a0/knowledge/...` (for example, `/a0/knowledge/tbc/...`) and contain narrative, conceptual, and procedural documents the agent can retrieve when needed.

The main library README you are reading is also made available to agents directly: a bind mount in `docker-compose.yml` (for example, `../../README.md:/a0/knowledge/default/main/tbc-library/README.md:ro` for a container under `containers/a0-*`) maps this file into `/a0/knowledge/default/main/tbc-library/README.md` inside the container, so agents can consume the exact same documentation via the knowledge layer.

These knowledge files are not executed directly. Instead, Agent Zero's knowledge/solutions mechanism can index them (for example, into a vector store or similar memory) and surface relevant entries to the agent based on queries, tool names, or explicit references from prompts. This keeps the system prompt focused while still giving the agent access to rich background information.

#### Solutions
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

### Extensibility Features of Agent Zero

In the `tbc-library` deployment, extensibility is expressed most strongly through **dynamic system control and profiles** (for behaviour, reasoning, and security) and through shared prompts, extensions, and tools.

If you want to understand *how this library changes Agent Zero's behaviour at runtime*, start with **Dynamic system control and profiles** below. If you want to understand *where that behaviour lives on disk*, see the prompts/extensions/tools subsections.

#### Extensions
Extensions enable custom behaviors layered on top of the core Agent Zero framework. In the `tbc-library` repository, most shared extensions live under `layers/control_layer/agents/_symlink/extensions` (host path), which are visible inside the container at `/a0/control_layer/agents/_symlink/extensions` and `/layers/control_layer/agents/_symlink/extensions`; agent profile directories then consume them via symlinks.

- `system_prompt/*` extensions build the system prompt in stages by reading profile-level files such as `pre_system_manual.md`, `post_system_manual.md`, `pre_behaviour.md`, `post_behaviour.md`, and `system_ready.md` from `/a0/agents/${CONTAINER_NAME}/prompts/` and `/a0/prompts/system/`.

From the agent's perspective, these extensions are the mechanism that turn prompt files in its profile and shared layers into a structured, multi-stage system prompt for each message loop.

##### System prompt staging pipeline

When the `system_prompt` extension point runs, Agent Zero first applies the base engine extensions located under `/a0/python/extensions/system_prompt/`, then any layered extensions from `/a0/agents/${CONTAINER_NAME}/extensions/system_prompt/` (typically symlinks into `_symlink`). In the `tbc-library` deployment described in this README, the overall staging looks like this:

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

#### Helpers
Helpers provide utility functions for advanced control.

##### System control helper (`system_control.py`)

`system_control.py` manages dynamic profile switching and global prompt-includes/system control tools, allowing agents to adapt modes (for example, workflow, philosophy, reasoning style, security posture) based on context while keeping concrete profile definitions in their own modules.

It acts as a central facade over the System Control config and override state:

- Uses a JSON configuration file (`system_control.json`, default path `/a0/tmp/system_control.json`) and an admin override lock file (default `/a0/tmp/admin_override.lock`), both overrideable via the environment variables `SYSTEM_CONTROL_FILE` and `SYSTEM_CONTROL_OVERRIDE`.
- Stores active profiles in a flat layout that distinguishes security from other modules:
  - For the security profile, uses the dedicated `security` and `security_profiles` sections (for example, `security.active_profile` and `security_profiles[profile_name].prompt_includes`).
  - For all other profile modules (for example, `workflow_profile`, `philosophy_profile`, `reasoning_internal_profile`, `reasoning_interleaved_profile`, `reasoning_external_profile`), records only the active profile name under `prompt_modules[profile_module_name].active_profile`; available profiles and feature definitions for these modules come from their own `profiles.json` files under `control_layer/profile_modules/...`, not from `system_control.json`.
- Resolves prompt-include and System Control tool state by combining top-level `prompt_includes` and `system_control_tools` sections with any prompt-includes defined under the active security profile (for example, `security_profiles[active].prompt_includes`), and reports this via helpers such as `is_prompt_include_enabled`, `get_prompt_include_config`, `get_available_prompt_includes_and_controls`, `get_enabled_prompt_includes_and_controls`, and `get_security_state`. When the admin override lock is present, security-profile prompt-includes are treated as enabled regardless of their stored value.
- Provides explicit, module-based APIs such as `get_active_profile`, `set_active_profile`, `get_state`, `get_available_profiles`, and `run_profile_control` for profile-control tools, plus summary helpers (`get_all_profiles_state`, `get_all_profiles_extras`, `get_system_summary`) that extensions and prompts can use to surface concise, system-wide status.

#### Tools
Tools expand agent capabilities with new functions. Many core tools are implemented once under `layers/control_layer/agents/_symlink/tools` in the `tbc-library` repository on the host (visible inside the container at `/a0/control_layer/agents/_symlink/tools` and `/layers/control_layer/agents/_symlink/tools`) and exposed to each agent profile via symlinks in `layers/<agent>/agents/<agent>/tools` on the host (mounted at `/layers/<agent>/agents/<agent>/tools` inside the container).

- **Profile and prompt-include/System Control tools** (`prompt_include_control` as the primary SystemControl toggle, plus `security_profile_control`, `philosophy_profile_control`, `liminal_thinking_profile_control`, `reasoning_profile_control`, `workflow_profile_control`) use `system_control.py` to inspect and adjust active profiles and SystemControl prompt-includes/system control tools at runtime, subject to security constraints.
- **Base tool infrastructure** (`base_profile_control.py`) centralizes common dispatch and error handling for profile-control style tools.
- Additional tools such as `a2a_chat`, `memory`, `scheduler`, and `document_query` are documented by prompts in the `_symlink/prompts` directory and may be wired via extensions and SystemControl-managed configuration.

#### Dynamic system control and profiles

Beyond individual tools and helpers, the **tbc-library layer** (via `system_control.py` above) exposes a coordinated **System Control** subsystem that lets an Agent Zero instance dynamically adjust how it behaves, reasons, and applies operational principles at runtime.

- At the core is `system_control.py`, which acts as a facade over a JSON configuration file (by default `/a0/tmp/system_control.json`). It stores the active profile name for each profile module (for example, `security`, `workflow_profile`, `philosophy_profile`, `liminal_thinking_profile`, `reasoning_internal_profile`, `reasoning_interleaved_profile`, `reasoning_external_profile`) and manages global prompt-includes/system control tools. Available profiles and feature definitions for non-security modules live in their respective `profiles.json` files under `control_layer/profile_modules/...`, while `system_control.json` focuses on active selections and prompt-include/control state.
- This design allows the agent to adapt behaviour based on context (for example, switching between more cautious vs more exploratory modes) without changing core code or restarting the container.

**Why dynamic profiles?**

Dynamic profiles give Agent Zero a way to separate *what* it knows and *how* it operates:

- **Adaptive behaviour** – switch interaction patterns (for example, more guided and verbose explanations vs a concise/operator style) via workflow profiles.
- **Contextual reasoning** – adjust cognitive strategies for different problem types by selecting reasoning profiles that focus internal, interleaved, or external chains of thought.
- **Security and ethics** – enforce security posture and operational principles through security and philosophy profiles, controlling which tools are available and how they may be used.
- **Extensibility** – add new profile types or features over time while keeping the control surface centralized in `system_control.py`.

**Profile types managed by System Control**

In the `tbc-library` deployment, System Control typically manages these conceptual profile categories, each implemented as one or more profile modules under `control_layer/profile_modules/...`:

- **Security profile** (`security`) – governs security-related behaviour, access controls, and feature availability.
- **Philosophy profile** (`philosophy_profile`) – captures core operational principles, values, and decision-making frameworks.
- **Liminal thinking profile** (`liminal_thinking_profile`) – manages cognitive patterns for navigating ambiguity, transitions, and uncertain situations.
- **Workflow profile** (`workflow_profile`) – configures interaction style and workflow behaviour (for example, guided vs minimal, confirmation-heavy vs streamlined; see `workflow_profile_control`).
- **Internal reasoning profile** (`reasoning_internal_profile`) – controls private, non-user-facing reasoning traces used for complex problem-solving.
- **Interleaved reasoning profile** (`reasoning_interleaved_profile`) – manages reasoning that occurs between tool calls, coordinating longer chains of action and reflection.
- **External reasoning profile** (`reasoning_external_profile`) – controls user-facing reasoning exposition (for example, explicit thoughts or structured explanations), when enabled by security and workflow policies.

**Profile and prompt-include/System Control tools**

The following tools are thin, user- and agent-facing wrappers around `system_control.py` that manage prompt-includes/system control tools and profile state:

- `security_profile_control` – view or change the active security profile.
- `philosophy_profile_control` – manage high-level operational principles.
- `liminal_thinking_profile_control` – configure liminal thinking behaviour.
- `workflow_profile_control` – set workflow style and related behavioural switches.
- `reasoning_profile_control` – coordinate internal, interleaved, and external reasoning strategies as a combined reasoning profile.
- `prompt_include_control` – primary tool to enable or disable specific SystemControl prompt-includes and System Control tools.

Each of these tools calls into `system_control.py` to read or update the current configuration, which is persisted in `system_control.json`. Profile prompts under `control_layer/profile_modules/...` (for example, `control_layer/profile_modules/workflow_profile/workflow_profile.md` and the reasoning profile modules) then render this state into readable text, so both humans and agents can see which profiles are active and what they imply.

**Example: dynamic state**

At any given time, an Agent Zero instance might be operating with a configuration like:

- Security profile: `open` (with any admin override flags inactive).
- Philosophy profile: `default`.
- Liminal thinking profile: `default`.
- Workflow profile: `guided_verbose` (with an auto-confirmation feature enabled).
- Internal reasoning profile: `internal_cot_1`.
- Interleaved reasoning profile: `interleaved_cot_1`.
- External reasoning profile: `external_cot_1`.

This kind of configuration illustrates how the System Control subsystem turns abstract design goals (security posture, philosophy, reasoning strategy, workflow) into concrete, inspectable profiles that can be adjusted over time without changing the underlying engine or layered file structure.

### Prompts in Agent Zero
Prompts are the primary way agents describe their roles, tools, and lifecycle behavior. In the `tbc-library` repository on the host, most agent-visible prompt files in `layers/<agent>/agents/<agent>/prompts` are symlinks into the shared `_symlink` prompt library under `layers/control_layer/agents/_symlink/prompts` (seen inside the container at `/a0/control_layer/agents/_symlink/prompts` and `/layers/control_layer/agents/_symlink/prompts`). Those shared stubs typically include or route into the default system prompt tree at `/a0/prompts` (for example, `prompts/system` and any container-specific prompts under `/a0/prompts/container`). From the host, this same `/a0/prompts` tree is mirrored under `containers/${CONTAINER_NAME}/a0/prompts` via the `${AGENT_CONTAINER}:/a0` bind mount, while its shared content originates from `layers/common/prompts/...` via the `${COMMON_LAYER}/prompts/...` mounts described earlier.

- Files such as `agent.system.main.role.md` act as stable entrypoints that `{{ include ... }}` their actual text from the shared system prompt tree (for example, `prompts/system`), allowing central updates without changing agent profiles.
- Tool prompt stubs such as `agent.system.tool.prompt_include_control.md`, `agent.system.tool.security_profile_control.md`, and `agent.system.tool.scheduler.md` include shared descriptions from `prompts/system/tools`, keeping tool instructions consistent across agents.
- The TBC `agent_identity` prompt (at `prompts/tbc/agent_identity/agent_identity.md`) works with `agent_identity.py`, which implements `AgentIdentity(VariablesPlugin)`. It looks first in `agents/${CONTAINER_NAME}/prompts/<profile>.md` and then in `prompts/tbc/agent_identity/identities/<profile>.md`, and reports where the identity was found via `{{agent_identity_found_where}}`. This lets agents combine profile-specific and shared identities while keeping the actual identity text in separate, overrideable files.
  - The workflow profile prompt (`control_layer/profile_modules/workflow_profile/workflow_profile.md`) works with its local loader (`workflow_profile.py`) and `profiles.json` in the same module directory. The loader asks `SystemControl` for the active workflow profile for the `workflow_profile` module, loads the corresponding definition and any enabled features from `profiles.json` (and the associated `profiles/*.md` and `features/*.md` files), and supplies variables such as `{{status}}` and `{{profile_content}}` to the prompt template. This modularizes workflow behaviour into a control file, a profile module (code + `profiles.json` + markdown), and a prompt template while keeping everything driven by the same kwargs-enabled prompt pipeline.
  - The reasoning profiles view is composed from three separate profile modules under `control_layer/profile_modules` (`reasoning_internal_profile`, `reasoning_interleaved_profile`, `reasoning_external_profile`) together with a small reasoning overview prompt include (for example, `control_layer/prompt_includes/reasoning_profiles/reasoning_profiles_content.md`). Each reasoning module has its own loader and `profiles.json`, uses `SystemControl` to obtain its active profile, and renders its status/content, while the overview prompt arranges these three dimensions (internal, interleaved, external) into a single, readable reasoning configuration. This lets the agent treat its reasoning strategy as a coordinated but independently configurable set of profiles.

From inside the container, an agent can treat `/a0/agents/${CONTAINER_NAME}/prompts` as its live prompt directory while understanding that many files are symlinks to shared templates. Local overrides can be created by replacing specific symlinks with real files in the agent's profile.

### More About Agent Zero
_(Pending content.)_

## Final Thoughts

### The Boot Code Storybook is it Limited to Agent Zero?

Nope. I just really like it and it is so perfectly fitting for the narrative-technical development.

The project will likely expand into other areas and libraries as the public-facing side evolves. Future work may include custom programs and public projects, some as independent components and services and others more integrated. Think in terms of layers, where new tools or knowledge can be added modularly without altering the core structure.

The Boot Code Storybook is a living, breathing, evolving project. It is not limited to Agent Zero, but rather what you find here is a framework to take part in building an idea.

Use your imagination. You can also use Agent Zero to:

- create, maintain, and evolve other agents autonomously by leveraging self-revealing orchestration, and
- layer custom extensions and prompts to add new behaviors without touching the core engine.

This enables organic growth through experimentation and collaboration.

### Disclaimers

This is an ongoing live development project, and this README is a living document. Treat it as both a friendly welcome to the project and the primary, evolving source of instructions for how to work with tbc-library.

### Versioning

- tbc-library does not yet have a version assigned
- a0-template/.env.example currently is set to IMAGE_NAME=agent0ai/agent-zero:latest
- Development is in progress integrating the anticipated Agent Zero v097 upcoming Projects functionality with tbc-library

### Attribution

Many thanks to the existence of Agent Zero most notably the creator Jan as well as the community of the open source project.

https://github.com/agent0ai/agent-zero

### Glossary

- **Agent Zero**: An open-source AI framework for building customizable agents that learn and adapt.
- **Boot Code**: Persistent narrative and technical data that "activates" the system's creative feedback loop.
- **Feedback Machine**: The dynamic interplay between storytelling and code execution, enabling organic agent growth.
- **Finder**: A user who discovers and shares the secrets of The Boot Code Storybook.
- **Layers**: On the host, the `layers/` directory in the `tbc-library` repository; inside the container, the same content is exposed at `/layers` (with `/agent_layer` and `/common_layer` providing focused views). These abstracted directories hold shared and agent-specific configs and data, avoiding direct modifications to the Agent Zero engine.
- **Narrative Driven Development**: Building software where stories guide technical features and user experiences.
- **Self-Revealing Orchestration**: Bind mount system that provides agents with direct, transparent access to their own layers and structure.
- **Adaptability**: Willingness to revisit assumptions and adjust behavior when obstacles or new information appear.
