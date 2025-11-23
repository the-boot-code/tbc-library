# Agent creation instrument: `create_agent.sh`

## Problem

- You are an in-container agent in this deployment environment.
- You sometimes need to **create or clone Agent Zero containers** (peers in the deployment, as new containers or clones).

This is done via the instrument script `create_agent.sh`. You must:

- express its use as **concrete tool calls** (for example `code_execution_tool`)
- choose appropriate arguments (`source`, `dest`, `dest_display`, `port_base`,
  `knowledge_dir`, etc.) without depending on hidden implementation details

## Solution

Use this document as a **usage guide** for `create_agent.sh` only:

- treat `create_agent.sh` as an orchestration instrument you invoke via
  `code_execution_tool` from inside the container
- use the JSON patterns below as templates when requesting new agents
- in this deployment, the script is mounted inside the container at
  `/a0/instruments/default/main/tbc-library/create_agent.sh` via the
  docker-compose configuration; if this ever changes, you can always
  locate it safely with:

  ```bash
  find /a0 -name create_agent.sh 2>/dev/null
  ```

---

### Quick usage patterns (for agents)

#### Create a new agent with `create_agent.sh` via `code_execution_tool`

From inside the container, run the script only as a **local instrument** and
you **must** use absolute `/containers/...` paths for the first two
arguments:

- `cd` to the instrument directory (for example
  `/a0/instruments/default/main/tbc-library`) and run
  `./create_agent.sh /containers/<source> /containers/<dest> [key=value ...]`

Outside this container (for example on a remote host that has the same
library checked out), `create_agent.sh` can also be run from the library root
by `cd`-ing there and invoking `./create_agent.sh ...`. This is informational
only for this document.

Use this pattern when forming `code_execution_tool` requests. Detailed
arguments, constraints, and behavior are described in the sections below; all
concrete JSON and shell examples are collected later in this document.

If `code_execution_tool` is unavailable or restricted by policy, do not attempt
to run this command.

---

### Creating an agent with `create_agent.sh`

Invocation form (run from your chosen working directory, for example the
instrument directory described above):

```bash
./create_agent.sh <source> <dest> [key=value ...]
```

Positional arguments:

- `source` – existing container under `containers/`. When running from the repo
  root, pass a **name** (for example `a0-template`). When running inside the
  container, you **must** pass an absolute **path** (for example
  `/containers/a0-template`).
- `dest` – new container under `containers/`. When running from the repo root,
  pass a **name** (for example `a0-myagent`). When running inside the
  container, you **must** pass an absolute **path** (for example
  `/containers/a0-myagent`).

Optional `key=value` arguments (any order):

- `dest_display` – human-readable name used in prompts and greetings.
- `dest_profile` – profile id under `layers/<dest>/agents/` (default: `<dest>`).
- `source_profile` – profile id to copy from the source (default: `<source>`).
- `port_base` – base for HTTP/SSH/etc ports (matches `.env.example`).
- `knowledge_dir` – value for `KNOWLEDGE_DIR` in the destination `.env`.
- `no_docker` – if set, skip `docker compose up -d`.
- `root_password`, `auth_login`, `auth_password` – values written into the
  layered `/a0/.env` file at `layers/<dest>/.env`.

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

- When you invoke `create_agent.sh` from inside a container, you usually do
  *not* control Docker itself (installation, daemon, or socket). You should not
  try to install Docker or modify Docker sockets from inside the container.
- Prefer `no_docker=true` if you only need to prepare the new agent's
  filesystem and configuration; a human or external orchestrator can start it
  later on a host with Docker.
- Do **not** attempt to install system packages such as `rsync` (for example
  via `apt-get` or `yum`) from inside the container in order to satisfy
  `create_agent.sh` dependencies. Instead, report that `rsync` (or another
  dependency) is missing and instruct the user or a host-level orchestrator to
  install it on the image/host before re-running the script.
- Do **not** delete `/containers/...` or `/layers/...` directories on your own
  (for example with `rm -rf`). If `create_agent.sh` reports that a destination
  container directory already exists, summarize this to the user and wait for
  explicit instructions (for example, to remove or rename the destination)
  rather than making destructive changes by default.
- If the script prints:

  `Agent <dest> created and customized successfully, but Docker is not installed or not on PATH.`

  treat this as a **successful creation** with no containers started. Summarize
  this to the user and stop; do not attempt host-level fixes.
- If the script prints:

  `Agent <dest> created and customized, but 'docker compose up -d' failed.`

  assume the environment lacks access to the Docker daemon or compose plugin.
  Summarize that the new agent is created but not started, and instruct the
  user to run `docker compose up -d` from a suitable host. Do not repeatedly
  retry or attempt to repair Docker from inside the container.

##### Example user-facing summaries

- After a "Docker not installed or not on PATH" message:

  > I successfully created and customized the new agent container `<dest>`, but
  > this environment does not have Docker available to start it. The new
  > container and its layered configuration are in place; please run
  > `docker compose up -d` in `containers/<dest>` from a host with Docker
  > installed if you want it running.

- After a "'docker compose up -d' failed" message:

  > I successfully created and customized the new agent container `<dest>`, but
  > `docker compose up -d` could not reach the Docker daemon or compose
  > plugin from this environment. The container definition and layered env are
  > ready; please start it later by running `docker compose up -d` in
  > `containers/<dest>` on a host with Docker access.

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
  port_base=500 knowledge_dir=tbc \
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

