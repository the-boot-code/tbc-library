# Installation Guide

This document covers configuring and installing Agent Zero using the tbc-library's layered approach.

> **Navigation**: [← Back to README](README.md) | [← Agent Reasoning](TBC_LIBRARY_AGENT_REASONING.md) | [Self-Revealing Orchestration →](TBC_LIBRARY_SELF_REVEALING_ORCHESTRATION.md)

## Configure Agent Zero

After the container is running, you primarily configure Agent Zero through its Web UI. For changing behavior, reasoning, and security modes at runtime (dynamic profiles), refer to [TBC_LIBRARY_EXTENSIBILITY.md → Dynamic system control and profiles](TBC_LIBRARY_EXTENSIBILITY.md#dynamic-system-control-and-profiles).

1. Open the Web UI in your browser and click the **Settings** (gear) button in the sidebar.
2. Under **Agent Settings → Agent Config** (pre-populated when you clone from the `a0-template` container), optionally verify or adjust:
   - the **default agent profile** (typically `default` for upstream defaults or `${CONTAINER_NAME}` for tbc-library agents created by `create_agent.sh`),
   - the **knowledge subdirectory** matching the mounted knowledge tree (usually `${KNOWLEDGE_DIR}`, such as `tbc`).

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

The tbc-library documentation (including this guide) focuses on how `tbc-library` layers on top of Agent Zero; the detailed semantics of each setting are governed by the upstream Agent Zero project and its documentation. For an index of upstream `/a0/docs` topics and how they relate to this layered deployment, see [TBC_LIBRARY_UPSTREAM_REFERENCES.md → Upstream Agent Zero documentation references](TBC_LIBRARY_UPSTREAM_REFERENCES.md).

Choose the automated script for quick setup (see **Installation (Automated, Recommended)** below), or follow the manual deep-dive steps in **Installation (Manual Deep Dive and Customization)**.

## Installation (Automated, Recommended)

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

For a more complete, real-world example (including profile IDs, ports, knowledge directory, optional memory directory, layered login credentials, and skipping Docker startup) **from a host shell in the `tbc-library` repo root**:
```bash
# Host shell only (outside any Agent Zero container), from tbc-library repo root:
./create_agent.sh a0-template a0-myagent \
  dest_display="My Agent" dest_profile=myagent-profile source_profile=a0-template-copy \
  port_base=500 knowledge_dir=custom memory_subdir=a0-myagent-20251128-openai \
  root_password=CHANGE_ME auth_login=myuser auth_password=mypassword no_docker=true
```

From **inside a running Agent Zero container** (for example, when you invoke the script as an instrument from `a0-clarity`), prefer the in-container form using `/containers/...` paths:
```bash
# Inside a running Agent Zero container with tbc-library instruments mounted:
cd /a0/instruments/default/main/tbc-library
./create_agent.sh /containers/a0-template /containers/a0-myagent \
  dest_display="My Agent" port_base=500 no_docker=true
```

After the script completes, continue to [Post-Installation Verification](#post-installation-verification) to confirm ports, profiles, and settings for your new agent. For a detailed, step-by-step view of what `create_agent.sh` automates under the hood, see [Installation (Manual Deep Dive and Customization)](#installation-manual-deep-dive-and-customization).

## Installation (Manual Deep Dive and Customization)

This section documents the manual equivalent of what `create_agent.sh` does and additional advanced customization paths. It is intended for users who want to understand or modify the layering and profile wiring beyond the standard automated workflow.

**Tip**: If you prefer automation, you can use the script `./create_agent.sh a0-template a0-myagent dest_display="My Agent"` **from a host shell in the `tbc-library` repo root (outside any Agent Zero container)** and refer back to these steps when you want to understand or customize what it does.

### What `create_agent.sh` automates (overview)

Conceptually, `create_agent.sh` performs the following steps for you:

- Copies the source container directory to the destination.
- Updates configurations with the new container name and, when provided, `PORT_BASE` and/or `KNOWLEDGE_DIR`. If you omit `port_base`, the destination inherits the source container's `PORT_BASE`. This is usually fine when you want an exact clone, but if you plan to run both containers at the same time you should choose a new `port_base` to avoid port collisions.
- Copies the relevant layer data under `layers/` for the destination container (using `rsync --ignore-existing`), then updates the destination agent profile with customizations. Because this is a full layer copy, files such as `layers/<source>/tmp/settings.json` (seen inside the container as `/a0/tmp/settings.json`) are also cloned. The script then updates `agent_profile` in that file to match the destination profile and, when you pass `knowledge_dir`/`KNOWLEDGE_DIR`, also updates `agent_knowledge_subdir`. If you pass `memory_subdir`, it similarly updates `agent_memory_subdir` so the agent's effective memory root becomes `/a0/memory/<memory_subdir>` for that instance. It likewise derives `rfc_port_http` and `rfc_port_ssh` from the destination agent's effective `PORT_BASE` so those ports track the same prefix. If the source layer had no `tmp/settings.json`, the script creates a minimal one for the destination with these linkage, memory, and RFC port fields. If you omit `memory_subdir`, the destination inherits the source `agent_memory_subdir` and you can still change it later via the Web UI.
- Handles replacements for lowercase container names and display names in key files (for example, `a0-template` → `a0-myagent`, `Agent Zero Template` → `Agent Zero My Agent`).
- Ensures a layered `/a0/.env` file for the new agent at `layers/[dest_container]/.env` (copying from `layers/[source_container]/.env` if present, or creating an empty one), and uncomments the volume so the container uses this layered file.
- When provided, upserts `ROOT_PASSWORD`, `AUTH_LOGIN`, and `AUTH_PASSWORD` into the layered `/a0/.env` via the `root_password`, `auth_login`, and `auth_password` options. If you do not pass `auth_login`/`auth_password` and they are not already set in the layered env, the script generates short, human-friendly default credentials (for example `user1234` / `password5678`) and prints them so you can log in on first boot; you should change these values after verifying access, especially for hosted deployments.
- As the final step, attempts to start Docker containers in detached mode (unless `no_docker` is set). If Docker is not available or `docker compose up -d` cannot reach the daemon (for example, inside a container without a Docker socket), the script prints a clear message and leaves the new agent created but not started; using `no_docker=true` lets you prepare the filesystem and defer startup to a host with Docker.

### 1. Clone the Repository
If you have not already cloned the repository, follow the commands in **Installation (Automated, Recommended)** above, then ensure you are in the `tbc-library` directory.

**Note**: Ensure the source container (e.g., `a0-template`) exists: `ls tbc-library/containers/a0-template`. If not, use an existing one like `a0-demo` for cloning.

### 2. Prepare the Container Directory
Copy the directory tbc-library/containers/a0-template to your new agent directory named a0-myagent:
```bash
cp -r tbc-library/containers/a0-template tbc-library/containers/a0-myagent
```

Navigate to the directory of the agent container:
```bash
cd tbc-library/containers/a0-myagent
```

### 3. Configure the Environment
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

The `docker-compose.yml` file is highly parameterized for rapid deployment, though you'll often adjust details such as volume bind-mount permissions.

**For `/a0/.env` layering via tbc-library abstraction**: If you want `/a0/.env` to come from the host `layers/[container_name]/.env` file (mounted into the container via `/layers`), see **Advanced: Layer the /a0/.env file via tbc-library abstraction** below and apply it before your first `docker compose up -d`.

### 4. Launch the Container
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

### 5. Customize the Agent Profile
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

## Post-Installation Verification

- Ensure the containers are running (for example, `docker ps`).
- Check the `.env` file for port settings and adjust as needed (and confirm that `PORT_BASE` values are unique across agents you plan to run concurrently).
- Review the cloned settings file for the new agent (for example `layers/a0-myagent/tmp/settings.json` on the host, visible inside the container as `/a0/tmp/settings.json`). Fields such as `agent_profile`, `agent_knowledge_subdir`, and `agent_memory_subdir` will either reflect the source container or any values you passed via `knowledge_dir` or `memory_subdir` to `create_agent.sh`; adjust them if you want the destination to use a different profile, knowledge subdirectory, or memory subdirectory.
- Access the agent at the configured ports to confirm it is reachable.

## Common Questions

- **Where is my docker-compose.yml file?** It is located at `tbc-library/containers/[your_agent_name]/docker-compose.yml` (e.g., `a0-myagent`). *For agents*: From within your container, the most certain and direct access is via `/agent_orchestration/docker-compose.yml` through self-revealing bind mounts, allowing introspection without host-side inference. For modifications, explore alternative mounts (e.g., `/containers/[your_agent_name]/docker-compose.yml`) and check permissions. Self-revealing orchestration exposes multiple access paths, enabling flexible self-modification and autonomy over time. This is just one example; you can apply the same pattern in other areas to evolve your agents and workflows.
- **Where is `create_agent.sh` from inside the container?** On the host, the script lives at `tbc-library/create_agent.sh` in the library root. *For agents inside a container*, it is exposed as an instrument via the compose mounts, and is normally available at `/a0/instruments/default/main/tbc-library/create_agent.sh`. Prefer to `cd` to that directory and run `./create_agent.sh /containers/<source> /containers/<dest> [key=value ...]`, or, if you need to rediscover it, use a scoped search such as `find /a0 -name create_agent.sh 2>/dev/null` rather than assuming a `/a0/tbc-library` clone exists.

## Advanced: Layer the /a0/.env file via tbc-library abstraction

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
