# Agent creation instrument: `create_agent.sh`

## Problem

- You are an in-container agent in this deployment environment.
- You sometimes need to **create or clone Agent Zero containers** (peers in the deployment, as new containers or clones).

This is done via the instrument script `create_agent.sh`, invoked through a
terminal execution tool (for example `code_execution_tool`).

## Solution

Use this document as a **usage guide** for `create_agent.sh` only:

- in this deployment, the script is mounted inside the container at
  `/a0/instruments/default/main/tbc-library/create_agent.sh` via the
  docker-compose configuration; if this ever changes, you can always
  locate it safely with:

  ```bash
  find /a0 -name create_agent.sh 2>/dev/null
  ```

### Quick checklist (for agents inside this container)

- **Where/how to run**
  - Invoke `create_agent.sh` via a terminal tool such as
    `code_execution_tool` and treat it only as a **local instrument**.
  - `cd /a0/instruments/default/main/tbc-library` (or rediscover the
    path with `find /a0 -name create_agent.sh 2>/dev/null`).
- **How to call it**
  - Always use absolute `/containers/...` paths for `source` and `dest`
    (for example `/containers/a0-template` → `/containers/a0-myagent`).
  - Do **not** call it from `/a0/work_dir` with bare names like
    `./create_agent.sh a0-template a0-myagent`.
- **Dependencies and Docker**
  - `rsync` must already be installed in this environment; if the script
    reports it missing, summarize that and stop—do **not** try to
    install it (or any system package) yourself.
  - Prefer `no_docker=true` when running inside the container; assume
    a host or external orchestrator is responsible for `docker compose`.
- **Ports and collisions**
  - If you omit `port_base`, the destination keeps the source
    container's `PORT_BASE`. This is fine for an exact clone but may
    cause port conflicts if both run at the same time.
  - Choose a unique `port_base` when you expect source and destination
    to be running concurrently.
- **Settings and RFC ports**
  - The script clones or creates `tmp/settings.json` under the
    destination layer (visible in-container as `/a0/tmp/settings.json`).
  - It updates `agent_profile` to match `dest_profile`, and, when you
    pass `knowledge_dir`, it updates `agent_knowledge_subdir`.
  - If you pass `memory_subdir`, it updates `agent_memory_subdir` so
    the agent's effective memory root becomes `/a0/memory/<memory_subdir>`
    for that destination (with the host-side mirror at
    `layers/<dest>/memory/<memory_subdir>`).
  - It also derives `rfc_port_http` and `rfc_port_ssh` from `PORT_BASE`
    so they track the same prefix.
  - If you omit `memory_subdir`, `agent_memory_subdir` will initially
    reflect the source container until you or a human adjust it.
- **Layered env and auth**
  - The layered env at `layers/<dest>/.env` (mounted as `/a0/.env`)
    holds `ROOT_PASSWORD`, `AUTH_LOGIN`, and `AUTH_PASSWORD` when used.
  - If `auth_login` / `auth_password` are not already set and you do
    not pass them, the script generates short defaults such as
    `user1234` / `password5678` and prints them so the user can log in.
- **Safety rules**
  - Never run destructive commands like `rm -rf /containers/...` or
    `rm -rf /layers/...` without explicit user instruction.
  - Never attempt to install or upgrade system packages from inside the
    container to "fix" script dependencies.
- **After running**
  - Summarize for the user: new container name and paths, effective
    `PORT_BASE`, any `knowledge_dir`, where the settings and layered
    env live, whether Docker was started, and any generated UI
    credentials.
  - To locate the new agent's `behaviour.md`, apply the **Config-First
    Rule**: read `agent_memory_subdir` from `/a0/tmp/settings.json`.
    See [TBC_LIBRARY_AGENT_REASONING.md → Config-First Rule](layers/common/knowledge/default/main/tbc-library/TBC_LIBRARY_AGENT_REASONING.md#config-first-rule).

---

### Quick usage patterns (for agents)

From inside this container, the canonical bash pattern is:

```bash
cd /a0/instruments/default/main/tbc-library
./create_agent.sh /containers/<source> /containers/<dest> [key=value ...]
```

---

### Creating an agent with `create_agent.sh`

Invocation form (run from your chosen working directory, for example the
instrument directory described above):

```bash
./create_agent.sh <source> <dest> [key=value ...]
```

Positional arguments:

- `source` – existing container under `containers/`: `a0-template` (host) or
  `/containers/a0-template` (in-container).
- `dest` – new container under `containers/`: `a0-myagent` (host) or
  `/containers/a0-myagent` (in-container).

Optional `key=value` arguments (any order):

- `dest_display` – human-readable name used in prompts and greetings.
- `dest_profile` – profile id under `layers/<dest>/agents/` (default: `<dest>`).
- `source_profile` – profile id to copy from the source (default: `<source>`).
- `port_base` – base for HTTP/SSH/etc ports (matches `.env.example`). If you omit
  this argument, the destination keeps whatever `PORT_BASE` value the source
  container had in its `.env`. That is usually fine when you intentionally want
  an exact clone, but if you plan to run both containers at the same time you
  should choose a new `port_base` to avoid port collisions.
- `knowledge_dir` – value for `KNOWLEDGE_DIR` in the destination `.env`.
- `memory_subdir` – optional memory subdirectory name. When set, updates
  `agent_memory_subdir` in `/a0/tmp/settings.json` so the agent uses
  `/a0/memory/<memory_subdir>` as its memory root (host mirror
  `layers/<dest>/memory/<memory_subdir>`).
- `no_docker` – if set, skip `docker compose up -d`.
- `root_password`, `auth_login`, `auth_password` – values written into the
  layered `/a0/.env` file at `layers/<dest>/.env`. If you omit
  `auth_login`/`auth_password` and the layered env does not already define
  them, the script will generate short, human-friendly default credentials
  (for example `user1234` / `password5678`) and print them in its output so
  you have something to use for the first login (you should change them
  after verifying access, especially on hosted deployments).

Constraints:

- `dest` and `dest_profile` must be lowercase letters, digits, dashes; must
  start with letter or digit.
- `port_base` must be an integer in `[0, 654]`.
- The destination **container directory** must not already exist (for example
  `containers/<dest>` from the repo root, or `/containers/<dest>` inside the
  container).

What the script does (simplified):

- copies `containers/<source>` → `containers/<dest>`.
- ensures `.env` exists and sets `CONTAINER_NAME=<dest>`; updates
  `PORT_BASE` / `KNOWLEDGE_DIR` if provided.
- ensures `layers/<dest>/.env` exists (cloned from source if present),
  with a fresh `A0_PERSISTENT_RUNTIME_ID`.
- copies `layers/<source>/` → `layers/<dest>/` via `rsync --ignore-existing`.
  This includes any `tmp/settings.json` file under the source layer (for
  example `layers/<source>/tmp/settings.json` and its in-container view at
  `/a0/tmp/settings.json`). When present, the script updates
  `agent_profile` in that file to match `dest_profile`, and if you passed
  `knowledge_dir` it also updates `agent_knowledge_subdir` accordingly.
  If you passed `memory_subdir`, it updates `agent_memory_subdir` so the
  destination agent uses `/a0/memory/<memory_subdir>` as its memory
  root (with the corresponding layered path at
  `layers/<dest>/memory/<memory_subdir>`). It also derives
  `rfc_port_http` and `rfc_port_ssh` from the destination agent's
  effective `PORT_BASE` so those ports stay consistent with the
  orchestration `.env`. If no `tmp/settings.json` existed for the source,
  the script creates a minimal one for the destination with these linkage,
  memory, and port fields when relevant. If you omit `memory_subdir`,
  `agent_memory_subdir` will initially reflect the source container until
  you or a human adjust it for the destination.
- recreates `layers/<dest>/agents/<dest_profile>` from
  `layers/<source>/agents/<source_profile>` and edits key files
  (`_context.md`, `prompts/fw.initial_message.md`, and
  `extensions/agent_init/_05_agent_name.py` when present) to use
  the new profile id and display name.
- uncomments the `/a0/.env` volume mapping if `layers/<dest>/.env` exists.
- attempts to run `docker compose up -d` unless `no_docker` is set; if Docker
  is not available or cannot reach the daemon (for example, inside a container
  without a Docker socket), it prints a clear message and leaves the agent
  created but not started.

#### Docker awareness and safety for agents

- Inside this container you usually do **not** control Docker itself
  (installation, daemon, or socket). Do not try to install Docker, modify
  sockets, or "fix" Docker from here.
- Prefer `no_docker=true` when running `create_agent.sh` in-container so a
  human or external orchestrator can start the stack later on a host with
  Docker.
- If the script prints either of these messages:

  - `Agent <dest> created and customized successfully, but Docker is not installed or not on PATH.`
  - `Agent <dest> created and customized, but 'docker compose up -d' failed.`

  treat both as: **filesystem and configuration prepared; startup deferred**.
  Summarize this to the user and recommend:

  > I created and customized `<dest>`, but Docker is not available from this
  > environment. Please run `docker compose up -d` in `containers/<dest>` on a
  > host with Docker if you want it running.

- Do **not** install system packages (for example `rsync` via `apt-get`/`yum`)
  or delete `/containers/...` and `/layers/...` directories on your own. If
  dependencies are missing or a destination already exists, explain the
  situation and wait for explicit user instructions.

---

### Examples (for agents and humans)

#### In-container instrument JSON (correct pattern)

```json
{
  "thoughts": [
    "Clone a new agent container a0-myagent from a0-template without starting Docker yet"
  ],
  "headline": "Create new agent container",
  "tool_name": "code_execution_tool",
  "tool_args": {
    "runtime": "terminal",
    "session": 0,
    "code": "cd /a0/instruments/default/main/tbc-library && ./create_agent.sh /containers/a0-template /containers/a0-myagent dest_display=\"My Agent\" port_base=500 knowledge_dir=tbc no_docker=true"
  }
}
```

#### In-container bare-name error example

```bash
# Inside container (incorrect example: using bare names will fail as shown below)
cd /a0/instruments/default/main/tbc-library && ./create_agent.sh a0-template a0-myagent
# Error: When running inside the container, source and dest must be absolute /containers/... paths.
```

#### Minimal host-side clone

```bash
# Host shell (outside any Agent Zero container), from tbc-library repo root:
./create_agent.sh a0-template a0-myagent
```

#### Full host-side example without starting Docker

```bash
# Host shell (outside any Agent Zero container), from tbc-library repo root:
./create_agent.sh a0-template a0-myagent \
  dest_display="My Agent" dest_profile=myagent-profile source_profile=a0-template-copy \
  port_base=500 knowledge_dir=tbc memory_subdir=a0-myagent-20251128-openai \
  root_password=CHANGE_ME auth_login=myuser auth_password=mypassword \
  no_docker=true
```

### Help and additional patterns

For more combinations and edge cases, consult the script's built-in help
and examples from an appropriate shell context (host or container):

```bash
./create_agent.sh --help
./create_agent.sh --examples
```

