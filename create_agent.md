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

---

### Quick usage patterns (for agents)

#### Create a new agent with `create_agent.sh` via `code_execution_tool`

From inside the container, run the script only as a **local instrument**:

- `cd` to the instrument directory (for example
  `/a0/instruments/default/main/tbc-library`) and run
  `./create_agent.sh ...`

Outside this container (for example on a remote host that has the same
library checked out), `create_agent.sh` can also be run from the library root
by `cd`-ing there and invoking `./create_agent.sh ...`. This is informational
only for this document.

The JSON pattern below shows the in-container **instrument** call. Adjust the
`code` field only if some external automation is calling it from a library
root instead.

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
    "code": "cd /a0/instruments/default/main/tbc-library && ./create_agent.sh a0-template a0-myagent dest_display=\"My Agent\" port_base=500 knowledge_dir=tbc no_docker=true"
  }
}
```

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

- `source` – existing container under `containers/` (for example `a0-template`).
- `dest` – new container name (for example `a0-myagent`).

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

- `dest` and `dest_profile` must be lowercase letters, digits, dashes;
  must start with letter or digit.
- `port_base` must be an integer in `[0, 654]`.
- `containers/<dest>` must not already exist.

#### Minimal clone

```bash
./create_agent.sh a0-template a0-myagent
```

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
- runs `docker compose up -d` unless `no_docker` is set.

#### Full example without starting Docker

```bash
./create_agent.sh a0-template a0-myagent \
  dest_display="My Agent" dest_profile=myagent-profile source_profile=a0-template-copy \
  port_base=500 knowledge_dir=tbc \
  root_password=CHANGE_ME auth_login=myuser auth_password=mypassword \
  no_docker=true
```

### Help and examples

For additional usage patterns and argument combinations, consult the
`create_agent.sh` help and examples:

```bash
./create_agent.sh --help
./create_agent.sh --examples
```

