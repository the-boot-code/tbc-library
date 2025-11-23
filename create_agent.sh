#!/bin/bash

# Usage: ./create_agent.sh <source> <dest> [key=value ...]
# Optional keys: dest_display, dest_profile, source_profile, port_base, knowledge_dir, no_docker, root_password, auth_login, auth_password
# Example: ./create_agent.sh a0-template a0-myagent dest_display=MyAgent port_base=500
# Example with knowledge_dir: ./create_agent.sh a0-template a0-myagent dest_display=MyAgent port_base=500 knowledge_dir=custom
# Example without starting Docker: ./create_agent.sh a0-template a0-myagent dest_display=MyAgent port_base=500 no_docker=true
# Example with defaults: ./create_agent.sh a0-template a0-myagent
# Example from inside container using explicit paths:
#   ./create_agent.sh /containers/a0-template /containers/a0-myagent dest_display=MyAgent port_base=500 knowledge_dir=custom no_docker=true

print_help() {
  cat <<EOF
create_agent.sh - clone an agent container and prepare its env and Docker stack.

Usage:
  $0 <source> <dest> [key=value ...]

Required arguments:
  source                      Existing template container name or path (e.g. a0-template or /containers/a0-template)
  dest                        New agent container name or path (e.g. a0-myagent or /containers/a0-myagent; directory will be created; must be filesystem-safe)
                              When running inside a container (REPO_ROOT=/), source and dest must be absolute /containers/... paths.

Optional key=value arguments:
  dest_display=NAME           Human-readable name for the new agent (default: dest_profile)
  dest_profile=NAME           Agent profile id in the destination container (default: dest; lowercase letters, digits, dashes only)
  source_profile=NAME         Agent profile id in the source container (default: source)
  port_base=NUM               Base port (0-654) for this agent's services
  knowledge_dir=DIR           Knowledge directory name (template-dependent default if omitted)
  no_docker=BOOL              If set (e.g. no_docker=true), do not run "docker compose up -d"
  root_password=VALUE         Root password to place in the layered /a0/.env (ROOT_PASSWORD)
  auth_login=USERNAME         Default auth login to place in the layered /a0/.env (AUTH_LOGIN)
  auth_password=VALUE         Default auth password to place in the layered /a0/.env (AUTH_PASSWORD)

For detailed usage examples, run:
  $0 --examples
EOF
}

print_examples() {
  cat <<EOF
Usage examples:

  # 1) Minimal: only required arguments (all defaults)
  $0 a0-template a0-myagent

  # 2) Add a display name (profile id defaults to dest)
  $0 a0-template a0-myagent \
    dest_display=MyAgent

  # 3) Customize source and destination profile ids
  $0 a0-template a0-myagent \
    dest_display=MyAgent dest_profile=myagent-profile source_profile=a0-template-profile

  # 4) Add a port base
  $0 a0-template a0-myagent \
    dest_display=MyAgent dest_profile=myagent-profile source_profile=a0-template-profile port_base=500

  # 5) Add a custom knowledge directory
  $0 a0-template a0-myagent \
    dest_display=MyAgent dest_profile=myagent-profile source_profile=a0-template-profile port_base=500 knowledge_dir=custom

  # 6) Full configuration, without starting Docker
  $0 a0-template a0-myagent \
    dest_display=MyAgent dest_profile=myagent-profile source_profile=a0-template-profile port_base=500 knowledge_dir=custom no_docker=true

  # 7) Full configuration with layered login credentials (no Docker)
  $0 a0-template a0-myagent \
    dest_display="My Agent" dest_profile=myagent-profile source_profile=a0-template-copy port_base=500 knowledge_dir=custom \
    root_password=CHANGE_ME auth_login=myuser auth_password=mypassword no_docker=true
EOF
}

# ./create_agent.sh a0-template a0-myagent dest_display="My Agent" dest_profile=myagent-profile source_profile=a0-template-copy port_base=500 knowledge_dir=custom no_docker=true

# ROOT_PASSWORD=O4n7ewRnsYBM8x19gR0PNvMx4HW4Ktest
# AUTH_LOGIN=username1
# AUTH_PASSWORD=password1

# ./create_agent.sh a0-template a0-myagent dest_display="My Agent" dest_profile=myagent-profile source_profile=a0-template-copy port_base=500 knowledge_dir=custom root_password=O4n7ewRnsYBM8x19gR0PNvMx4HW4Ktest auth_login=username1 auth_password=password1 no_docker=true

validate_display_name() {
  local label="$1"
  local value="$2"

  if [ -z "$value" ]; then
    echo "Error: $label is empty." >&2
    exit 1
  fi

  case "$value" in
    -*)
      echo "Error: $label '$value' must not start with '-'." >&2
      exit 1
      ;;
  esac
}

validate_port_base() {
  local value="$1"

  if [ -z "$value" ]; then
    return 0
  fi

  case "$value" in
    *[!0-9]*)
      echo "Error: port_base '$value' must be a non-negative integer." >&2
      exit 1
      ;;
  esac

  if [ "$value" -lt 0 ] || [ "$value" -gt 654 ]; then
    echo "Error: port_base '$value' must be between 0 and 654." >&2
    exit 1
  fi
}

validate_linux_safe_name() {
  local label="$1"
  local value="$2"

  case "$value" in
    [a-z0-9][a-z0-9-]*)
      ;; # ok
    *)
      echo "Error: $label '$value' must use only lowercase letters, digits, and dashes, and must start with a letter or digit." >&2
      exit 1
      ;;
  esac
}

if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
  print_help
  exit 0
fi

if [ "$1" = "--examples" ]; then
  print_examples
  exit 0
fi

if [ $# -eq 0 ]; then
  print_help
  exit 0
fi

if [ $# -eq 1 ]; then
  echo "Error: Both source and dest are required; only one positional argument was provided ('$1')." >&2
  print_help
  exit 1
fi

if [ $# -lt 2 ] || [ $# -gt 11 ]; then
  print_help
  exit 1
fi

# Ensure required dependencies are available early
if ! command -v rsync >/dev/null 2>&1; then
  echo "Error: rsync is required by create_agent.sh but is not installed or not on PATH in this environment." >&2
  echo "Please install rsync on the host or image, then re-run this script." >&2
  exit 1
fi

# Determine the base directory of the script
SCRIPT_DIR=$(dirname "$0")
BASE_DIR=$(cd "$SCRIPT_DIR" && pwd)

# Find the repo root by looking for directories with containers/ and layers/
REPO_ROOT="$BASE_DIR"
while [ ! -d "$REPO_ROOT/containers" ] || [ ! -d "$REPO_ROOT/layers" ]; do
  if [ "$REPO_ROOT" = "/" ]; then
    echo "Error: Could not find repo root with containers/ and layers/ directories."
    exit 1
  fi
  REPO_ROOT=$(dirname "$REPO_ROOT")
done

# Arguments:
#   1: SOURCE (required, positional; container name or path)
#   2: DEST   (required, positional; container name or path)
#
# Optional args (3+), may appear in any order as key=value:
#   dest_display=...
#   dest_profile=...
#   source_profile=...
#   port_base=...
#   knowledge_dir=...
#   no_docker=...      (any non-empty value skips docker compose up -d)
#   root_password=...
#   auth_login=...
#   auth_password=...
RAW_SOURCE=$1
RAW_DEST=$2

CONTAINERS_ROOT="$REPO_ROOT/containers"
LAYERS_ROOT="$REPO_ROOT/layers"

# If running inside the container (REPO_ROOT=/), require /containers/... for both source and dest
if [ "$REPO_ROOT" = "/" ]; then
  if [[ "$RAW_SOURCE" != /containers/* || "$RAW_DEST" != /containers/* ]]; then
    echo "Error: When running inside the container, source and dest must be absolute /containers/... paths." >&2
    exit 1
  fi
fi

# Resolve source container name and path
if [[ "$RAW_SOURCE" == /* || "$RAW_SOURCE" == *"/"* ]]; then
  SOURCE_CONTAINER_PATH="$RAW_SOURCE"
  SOURCE_CONTAINER=$(basename "$SOURCE_CONTAINER_PATH")
else
  SOURCE_CONTAINER="$RAW_SOURCE"
  SOURCE_CONTAINER_PATH="$CONTAINERS_ROOT/$SOURCE_CONTAINER"
fi

# Resolve destination container name and path
if [[ "$RAW_DEST" == /* || "$RAW_DEST" == *"/"* ]]; then
  DEST_CONTAINER_PATH="$RAW_DEST"
  DEST_CONTAINER=$(basename "$DEST_CONTAINER_PATH")
else
  DEST_CONTAINER="$RAW_DEST"
  DEST_CONTAINER_PATH="$CONTAINERS_ROOT/$DEST_CONTAINER"
fi

# Defaults for optional arguments
SOURCE_PROFILE="$SOURCE_CONTAINER"
DEST_PROFILE="$DEST_CONTAINER"
DEST_DISPLAY=""
DEST_DISPLAY_SET=""
PORT_BASE=""
KNOWLEDGE_DIR=""
NO_DOCKER=""
ROOT_PASSWORD=""
AUTH_LOGIN=""
AUTH_PASSWORD=""

# Track any generated auth credentials so we can report them to the user
GENERATED_AUTH_LOGIN=""
GENERATED_AUTH_PASSWORD=""

# Parse remaining optional arguments (any order, key=value only)
shift 2
for arg in "$@"; do
  case "$arg" in
    dest_display=*|DEST_DISPLAY=*)
      DEST_DISPLAY="${arg#*=}"
      DEST_DISPLAY_SET=1
      ;;
    dest_profile=*|DEST_PROFILE=*)
      DEST_PROFILE="${arg#*=}"
      ;;
    source_profile=*|SOURCE_PROFILE=*)
      SOURCE_PROFILE="${arg#*=}"
      ;;
    port_base=*|PORT_BASE=*)
      PORT_BASE="${arg#*=}"
      ;;
    knowledge_dir=*|KNOWLEDGE_DIR=*)
      KNOWLEDGE_DIR="${arg#*=}"
      ;;
    no_docker=*|NO_DOCKER=*)
      NO_DOCKER="${arg#*=}"
      ;;
    root_password=*|ROOT_PASSWORD=*)
      ROOT_PASSWORD="${arg#*=}"
      ;;
    auth_login=*|AUTH_LOGIN=*)
      AUTH_LOGIN="${arg#*=}"
      ;;
    auth_password=*|AUTH_PASSWORD=*)
      AUTH_PASSWORD="${arg#*=}"
      ;;
    *)
      echo "Unexpected extra argument (use key=value after the first two positional args): $arg" >&2
      exit 1
      ;;
  esac
done

# If dest_display was not provided, default it to the (possibly overridden) DEST_PROFILE
if [ -z "$DEST_DISPLAY_SET" ]; then
  DEST_DISPLAY="$DEST_PROFILE"
fi

# Slug form of DEST_DISPLAY for agent_name (replace spaces with hyphens)
AGENT_NAME_SLUG="${DEST_DISPLAY// /-}"

validate_display_name "DEST_DISPLAY" "$DEST_DISPLAY"
validate_port_base "$PORT_BASE"

validate_linux_safe_name "DEST_CONTAINER" "$DEST_CONTAINER"
validate_linux_safe_name "DEST_PROFILE" "$DEST_PROFILE"

if [ "$SOURCE_CONTAINER" = "$DEST_CONTAINER" ]; then
  echo "Error: SOURCE_CONTAINER and DEST_CONTAINER must be different." >&2
  exit 1
fi

echo "Creating agent: $DEST_CONTAINER from $SOURCE_CONTAINER"

# Check if source container exists
if [ ! -d "$SOURCE_CONTAINER_PATH" ]; then
  echo "Error: Source container $SOURCE_CONTAINER not found at $SOURCE_CONTAINER_PATH."
  exit 1
fi

# Check if destination container directory already exists
if [ -d "$DEST_CONTAINER_PATH" ]; then
  echo "Error: Container directory $DEST_CONTAINER_PATH already exists. Remove it manually if you want to recreate."
  exit 1
fi

# Copy container directory
cp -r "$SOURCE_CONTAINER_PATH" "$DEST_CONTAINER_PATH"

# Enter container directory
cd "$DEST_CONTAINER_PATH"

# Ensure orchestration .env (used by docker compose) exists
if [ ! -f .env ]; then
  cp .env.example .env
fi

# Update CONTAINER_NAME in orchestration .env
sed -i "s|^CONTAINER_NAME=.*|CONTAINER_NAME=$DEST_CONTAINER|" .env

# Update PORT_BASE in .env if provided
if [ -n "$PORT_BASE" ]; then
  sed -i "s|^PORT_BASE=.*|PORT_BASE=$PORT_BASE|" .env
fi

# Update KNOWLEDGE_DIR in .env if provided
if [ -n "$KNOWLEDGE_DIR" ]; then
  sed -i "s|^KNOWLEDGE_DIR=.*|KNOWLEDGE_DIR=$KNOWLEDGE_DIR|" .env
fi

if [ -n "$PORT_BASE" ] && [ -n "$KNOWLEDGE_DIR" ]; then
  echo "Updated orchestration .env: CONTAINER_NAME=$DEST_CONTAINER, PORT_BASE=$PORT_BASE, KNOWLEDGE_DIR=$KNOWLEDGE_DIR"
elif [ -n "$PORT_BASE" ]; then
  echo "Updated orchestration .env: CONTAINER_NAME=$DEST_CONTAINER, PORT_BASE=$PORT_BASE"
elif [ -n "$KNOWLEDGE_DIR" ]; then
  echo "Updated orchestration .env: CONTAINER_NAME=$DEST_CONTAINER, KNOWLEDGE_DIR=$KNOWLEDGE_DIR"
else
  echo "Updated orchestration .env: CONTAINER_NAME=$DEST_CONTAINER"
fi
echo "Note: Update PORT_BASE if needed for unique ports."

# Create layered .env (host-side, mounted as /a0/.env) from source if available, with new runtime ID
mkdir -p "$LAYERS_ROOT/$DEST_CONTAINER"
if [ ! -f "$LAYERS_ROOT/$DEST_CONTAINER/.env" ]; then
  if [ -f "$LAYERS_ROOT/$SOURCE_CONTAINER/.env" ]; then
    cp "$LAYERS_ROOT/$SOURCE_CONTAINER/.env" "$LAYERS_ROOT/$DEST_CONTAINER/.env"
    # Generate a new A0_PERSISTENT_RUNTIME_ID
    NEW_ID=$(uuidgen 2>/dev/null || echo "$(date +%s)-$(($RANDOM % 10000))")
    sed -i "s|^A0_PERSISTENT_RUNTIME_ID=.*|A0_PERSISTENT_RUNTIME_ID=$NEW_ID|" "$REPO_ROOT/layers/$DEST_CONTAINER/.env"
  else
    touch "$LAYERS_ROOT/$DEST_CONTAINER/.env"
  fi
fi

LAYERED_ENV_FILE="$LAYERS_ROOT/$DEST_CONTAINER/.env"

# If root/auth values were provided, upsert them in the layered /a0/.env
if [ -n "$ROOT_PASSWORD" ]; then
  if grep -q '^ROOT_PASSWORD=' "$LAYERED_ENV_FILE"; then
    sed -i "s|^ROOT_PASSWORD=.*|ROOT_PASSWORD=$ROOT_PASSWORD|" "$LAYERED_ENV_FILE"
  else
    echo "ROOT_PASSWORD=$ROOT_PASSWORD" >> "$LAYERED_ENV_FILE"
  fi
fi

if [ -n "$AUTH_LOGIN" ]; then
  if grep -q '^AUTH_LOGIN=' "$LAYERED_ENV_FILE"; then
    sed -i "s|^AUTH_LOGIN=.*|AUTH_LOGIN=$AUTH_LOGIN|" "$LAYERED_ENV_FILE"
  else
    echo "AUTH_LOGIN=$AUTH_LOGIN" >> "$LAYERED_ENV_FILE"
  fi
fi

if [ -n "$AUTH_PASSWORD" ]; then
  if grep -q '^AUTH_PASSWORD=' "$LAYERED_ENV_FILE"; then
    sed -i "s|^AUTH_PASSWORD=.*|AUTH_PASSWORD=$AUTH_PASSWORD|" "$LAYERED_ENV_FILE"
  else
    echo "AUTH_PASSWORD=$AUTH_PASSWORD" >> "$LAYERED_ENV_FILE"
  fi
fi

# If no auth_login/auth_password were provided and the layered env still
# lacks them (or they are empty), generate defaults so hosted deployments
# that require credentials have something usable on first boot.
if [ -z "$AUTH_LOGIN" ]; then
  CURRENT_LOGIN=$(grep '^AUTH_LOGIN=' "$LAYERED_ENV_FILE" 2>/dev/null | sed 's/^AUTH_LOGIN=//')
  if [ -z "$CURRENT_LOGIN" ]; then
    LOGIN_SUFFIX=$(printf '%04d' $((RANDOM % 10000)))
    GENERATED_AUTH_LOGIN="user${LOGIN_SUFFIX}"
    if grep -q '^AUTH_LOGIN=' "$LAYERED_ENV_FILE" 2>/dev/null; then
      sed -i "s|^AUTH_LOGIN=.*|AUTH_LOGIN=$GENERATED_AUTH_LOGIN|" "$LAYERED_ENV_FILE"
    else
      echo "AUTH_LOGIN=$GENERATED_AUTH_LOGIN" >> "$LAYERED_ENV_FILE"
    fi
  fi
fi

if [ -z "$AUTH_PASSWORD" ]; then
  CURRENT_PASSWORD=$(grep '^AUTH_PASSWORD=' "$LAYERED_ENV_FILE" 2>/dev/null | sed 's/^AUTH_PASSWORD=//')
  if [ -z "$CURRENT_PASSWORD" ]; then
    PASSWORD_SUFFIX=$(printf '%04d' $((RANDOM % 10000)))
    GENERATED_AUTH_PASSWORD="password${PASSWORD_SUFFIX}"
    if grep -q '^AUTH_PASSWORD=' "$LAYERED_ENV_FILE" 2>/dev/null; then
      sed -i "s|^AUTH_PASSWORD=.*|AUTH_PASSWORD=$GENERATED_AUTH_PASSWORD|" "$LAYERED_ENV_FILE"
    else
      echo "AUTH_PASSWORD=$GENERATED_AUTH_PASSWORD" >> "$LAYERED_ENV_FILE"
    fi
  fi
fi

# Ensure source profile directory exists under layers
if [ ! -d "$LAYERS_ROOT/$SOURCE_CONTAINER/agents/$SOURCE_PROFILE" ]; then
  echo "Error: Source profile $SOURCE_PROFILE not found under $LAYERS_ROOT/$SOURCE_CONTAINER/agents/." >&2
  exit 1
fi

# Navigate to layers
cd "$LAYERS_ROOT"

# Copy layers contents, preserving existing files
rsync -a --ignore-existing "$SOURCE_CONTAINER/" "$DEST_CONTAINER/"

# If a settings.json exists under the destination layer, update a few
# fields so the new agent points at its own profile, and, when requested,
# its own knowledge subdirectory and RFC ports. If it does not exist,
# create a minimal one with those fields so downstream behaviour has a
# consistent starting point.
SETTINGS_JSON="$LAYERS_ROOT/$DEST_CONTAINER/tmp/settings.json"

# Determine effective PORT_BASE for RFC ports (argument wins; otherwise
# inherit from the destination orchestration .env if present).
EFFECTIVE_PORT_BASE="$PORT_BASE"
if [ -z "$EFFECTIVE_PORT_BASE" ] && [ -f "$REPO_ROOT/containers/$DEST_CONTAINER/.env" ]; then
  EFFECTIVE_PORT_BASE=$(grep '^PORT_BASE=' "$REPO_ROOT/containers/$DEST_CONTAINER/.env" | sed 's/^PORT_BASE=//')
fi

if [ -f "$SETTINGS_JSON" ]; then
  # Update agent_profile to match DEST_PROFILE
  if grep -q '"agent_profile"' "$SETTINGS_JSON"; then
    sed -i "s/\"agent_profile\"[[:space:]]*:[[:space:]]*\"[^\"]*\"/\"agent_profile\": \"$DEST_PROFILE\"/" "$SETTINGS_JSON"
  fi
  # If KNOWLEDGE_DIR was specified, update agent_knowledge_subdir as well
  if [ -n "$KNOWLEDGE_DIR" ] && grep -q '"agent_knowledge_subdir"' "$SETTINGS_JSON"; then
    sed -i "s/\"agent_knowledge_subdir\"[[:space:]]*:[[:space:]]*\"[^\"]*\"/\"agent_knowledge_subdir\": \"$KNOWLEDGE_DIR\"/" "$SETTINGS_JSON"
  fi

  # Derive RFC ports from the effective PORT_BASE so they stay aligned with
  # the orchestration .env configuration.
  if [ -n "$EFFECTIVE_PORT_BASE" ]; then
    RFC_HTTP="${EFFECTIVE_PORT_BASE}80"
    RFC_SSH="${EFFECTIVE_PORT_BASE}22"
    if grep -q '"rfc_port_http"' "$SETTINGS_JSON"; then
      sed -i "s/\"rfc_port_http\"[[:space:]]*:[[:space:]]*[0-9]\+/\"rfc_port_http\": $RFC_HTTP/" "$SETTINGS_JSON"
    fi
    if grep -q '"rfc_port_ssh"' "$SETTINGS_JSON"; then
      sed -i "s/\"rfc_port_ssh\"[[:space:]]*:[[:space:]]*[0-9]\+/\"rfc_port_ssh\": $RFC_SSH/" "$SETTINGS_JSON"
    fi
  fi
else
  # No existing settings file: create a minimal one using the destination
  # profile, effective knowledge directory, and RFC ports when available.
  DEST_KNOWLEDGE="$KNOWLEDGE_DIR"
  if [ -z "$DEST_KNOWLEDGE" ] && [ -f "$REPO_ROOT/containers/$DEST_CONTAINER/.env" ]; then
    DEST_KNOWLEDGE=$(grep '^KNOWLEDGE_DIR=' "$REPO_ROOT/containers/$DEST_CONTAINER/.env" | sed 's/^KNOWLEDGE_DIR=//')
  fi

  if [ -n "$EFFECTIVE_PORT_BASE" ]; then
    RFC_HTTP="${EFFECTIVE_PORT_BASE}80"
    RFC_SSH="${EFFECTIVE_PORT_BASE}22"
    cat > "$SETTINGS_JSON" <<EOF
{
    "agent_profile": "$DEST_PROFILE",
    "agent_knowledge_subdir": "${DEST_KNOWLEDGE:-tbc}",
    "rfc_port_http": $RFC_HTTP,
    "rfc_port_ssh": $RFC_SSH
}
EOF
  else
    cat > "$SETTINGS_JSON" <<EOF
{
    "agent_profile": "$DEST_PROFILE",
    "agent_knowledge_subdir": "${DEST_KNOWLEDGE:-tbc}"
}
EOF
  fi
fi

# Navigate back to container directory
cd "$REPO_ROOT/containers/$DEST_CONTAINER"

# Uncomment the layered .env volume so it mounts into the container as /a0/.env
if [ -f "$LAYERS_ROOT/$DEST_CONTAINER/.env" ]; then
  sed -i 's/# - \${AGENT_LAYER}\/\.env:\/a0\/\.env:rw/- ${AGENT_LAYER}\/\.env:\/a0\/\.env:rw/' docker-compose.yml
fi

# Navigate to layers for agent customization
cd "$LAYERS_ROOT"

# Create agent profile directory
rm -rf "$DEST_CONTAINER/agents/$DEST_PROFILE"
mkdir -p "$DEST_CONTAINER/agents/$DEST_PROFILE"

# Copy agent profile from template (source profile may differ from container name)
cp -r "$SOURCE_CONTAINER/agents/$SOURCE_PROFILE/"* "$DEST_CONTAINER/agents/$DEST_PROFILE/"

# Enter agent profile directory
cd "$DEST_CONTAINER/agents/$DEST_PROFILE"

# If a prompts file is named after the source profile, rename it to use DEST_PROFILE
if [ -d prompts ] && [ -f "prompts/$SOURCE_PROFILE.md" ]; then
  mv "prompts/$SOURCE_PROFILE.md" "prompts/$DEST_PROFILE.md"
fi

PROMPTS_PROFILE_FILE="prompts/$DEST_PROFILE.md"
if [ -f "$PROMPTS_PROFILE_FILE" ]; then
  sed -i "s/^Agent Profile: .*/Agent Profile: '$DEST_PROFILE'/" "$PROMPTS_PROFILE_FILE"
  sed -i "s/^Agent Full Name: .*/Agent Full Name: 'Agent Zero $DEST_DISPLAY'/" "$PROMPTS_PROFILE_FILE"
  sed -i "s/^Agent aka: .*/Agent aka: $DEST_DISPLAY/" "$PROMPTS_PROFILE_FILE"
  sed -i "s/^Agent Persona: .*/Agent Persona: $DEST_DISPLAY/" "$PROMPTS_PROFILE_FILE"
fi

# Update _context.md title to use DEST_PROFILE, if present
if [ -f _context.md ]; then
  sed -i "1s|^# .*|# $DEST_PROFILE|" _context.md
fi

# Update fw.initial_message.md greeting to use DEST_DISPLAY, if present
if [ -f prompts/fw.initial_message.md ]; then
  sed -i "s|^.*\"text\": \".*\"|        \"text\": \"**Hello! 👋**, I'm **Agent Zero $DEST_DISPLAY**, your AI assistant. How can I help you today?\"|" prompts/fw.initial_message.md
fi

# Update agent_init/_05_agent_name.py to use a slugified DEST_DISPLAY in agent_name, if present
if [ -f extensions/agent_init/_05_agent_name.py ]; then
  sed -i "s|self.agent.agent_name = .*|        self.agent.agent_name = \"A0-$AGENT_NAME_SLUG-\" + str(self.agent.number)|" extensions/agent_init/_05_agent_name.py
fi

# Navigate back to container directory for optional Docker start
cd "$DEST_CONTAINER_PATH"

# Start Docker containers as the final step (unless no_docker is set)
if [ -n "$NO_DOCKER" ]; then
  echo "Agent $DEST_CONTAINER created and customized successfully (Docker not started)."
  echo "Sensitive layered env for /a0/.env is at /layers/$DEST_CONTAINER/.env"
  if [ -n "$GENERATED_AUTH_LOGIN" ] || [ -n "$GENERATED_AUTH_PASSWORD" ]; then
    echo "Generated default UI credentials for this agent (change them after first login):"
    if [ -n "$GENERATED_AUTH_LOGIN" ]; then
      echo "  AUTH_LOGIN=$GENERATED_AUTH_LOGIN"
    fi
    if [ -n "$GENERATED_AUTH_PASSWORD" ]; then
      echo "  AUTH_PASSWORD=$GENERATED_AUTH_PASSWORD"
    fi
  fi
  echo "You can start the agent later with: docker compose up -d (in containers/$DEST_CONTAINER)."
else
  # If Docker CLI is not available at all, do not treat this as a creation failure.
  if ! command -v docker >/dev/null 2>&1; then
    echo "Agent $DEST_CONTAINER created and customized successfully, but Docker is not installed or not on PATH."
    echo "Sensitive layered env for /a0/.env is at /layers/$DEST_CONTAINER/.env"
    if [ -n "$GENERATED_AUTH_LOGIN" ] || [ -n "$GENERATED_AUTH_PASSWORD" ]; then
      echo "Generated default UI credentials for this agent (change them after first login):"
      if [ -n "$GENERATED_AUTH_LOGIN" ]; then
        echo "  AUTH_LOGIN=$GENERATED_AUTH_LOGIN"
      fi
      if [ -n "$GENERATED_AUTH_PASSWORD" ]; then
        echo "  AUTH_PASSWORD=$GENERATED_AUTH_PASSWORD"
      fi
    fi
    echo "You can start the agent later with: docker compose up -d (in containers/$DEST_CONTAINER) on a host with Docker installed."
    exit 0
  fi

  # Attempt to start the container stack. If this fails (for example, no Docker daemon
  # or no socket in this environment), surface a clear message but do not undo creation.
  if ! docker compose up -d; then
    echo "Agent $DEST_CONTAINER created and customized, but 'docker compose up -d' failed."
    echo "Sensitive layered env for /a0/.env is at /layers/$DEST_CONTAINER/.env"
    if [ -n "$GENERATED_AUTH_LOGIN" ] || [ -n "$GENERATED_AUTH_PASSWORD" ]; then
      echo "Generated default UI credentials for this agent (change them after first login):"
      if [ -n "$GENERATED_AUTH_LOGIN" ]; then
        echo "  AUTH_LOGIN=$GENERATED_AUTH_LOGIN"
      fi
      if [ -n "$GENERATED_AUTH_PASSWORD" ]; then
        echo "  AUTH_PASSWORD=$GENERATED_AUTH_PASSWORD"
      fi
    fi
    echo "You may be running without access to the Docker daemon or compose plugin (for example, inside a container without the Docker socket)."
    echo "Start the agent later from a host with Docker access using: docker compose up -d (in containers/$DEST_CONTAINER)."
    exit 1
  fi

  echo "Agent $DEST_CONTAINER created, customized, and started successfully!"
  echo "Sensitive layered env for /a0/.env is at /layers/$DEST_CONTAINER/.env"
  if [ -n "$GENERATED_AUTH_LOGIN" ] || [ -n "$GENERATED_AUTH_PASSWORD" ]; then
    echo "Generated default UI credentials for this agent (change them after first login):"
    if [ -n "$GENERATED_AUTH_LOGIN" ]; then
      echo "  AUTH_LOGIN=$GENERATED_AUTH_LOGIN"
    fi
    if [ -n "$GENERATED_AUTH_PASSWORD" ]; then
      echo "  AUTH_PASSWORD=$GENERATED_AUTH_PASSWORD"
    fi
  fi
  echo "Access at configured ports (check orchestration .env for PORT_BASE)."
fi
