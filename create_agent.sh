#!/bin/bash

# Usage: ./create_agent.sh <source> <dest> [key=value ...]
# Optional keys: dest_display, dest_profile, source_profile, port_base, knowledge_dir, no_docker, root_password, auth_login, auth_password
# Example: ./create_agent.sh a0-template a0-myagent dest_display=MyAgent port_base=500
# Example with knowledge_dir: ./create_agent.sh a0-template a0-myagent dest_display=MyAgent port_base=500 knowledge_dir=custom
# Example without starting Docker: ./create_agent.sh a0-template a0-myagent dest_display=MyAgent port_base=500 no_docker=true
# Example with defaults: ./create_agent.sh a0-template a0-myagent

print_help() {
  cat <<EOF
create_agent.sh - clone an agent container and prepare its env and Docker stack.

Usage:
  $0 <source> <dest> [key=value ...]

Required arguments:
  source                      Existing template container name (directory under containers/)
  dest                        New agent container name (directory will be created; must be filesystem-safe)

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
#   1: SOURCE_CONTAINER (required, positional)
#   2: DEST_CONTAINER   (required, positional)
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
SOURCE_CONTAINER=$1
DEST_CONTAINER=$2

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
if [ ! -d "$REPO_ROOT/containers/$SOURCE_CONTAINER" ]; then
  echo "Error: Source container $SOURCE_CONTAINER not found in $REPO_ROOT/containers/."
  exit 1
fi

# Check if container already exists
if [ -d "$REPO_ROOT/containers/$DEST_CONTAINER" ]; then
  echo "Error: Container directory $REPO_ROOT/containers/$DEST_CONTAINER already exists. Remove it manually if you want to recreate."
  exit 1
fi

# Copy container directory
cp -r "$REPO_ROOT/containers/$SOURCE_CONTAINER" "$REPO_ROOT/containers/$DEST_CONTAINER"

# Enter container directory
cd "$REPO_ROOT/containers/$DEST_CONTAINER"

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
mkdir -p "$REPO_ROOT/layers/$DEST_CONTAINER"
if [ ! -f "$REPO_ROOT/layers/$DEST_CONTAINER/.env" ]; then
  if [ -f "$REPO_ROOT/layers/$SOURCE_CONTAINER/.env" ]; then
    cp "$REPO_ROOT/layers/$SOURCE_CONTAINER/.env" "$REPO_ROOT/layers/$DEST_CONTAINER/.env"
    # Generate a new A0_PERSISTENT_RUNTIME_ID
    NEW_ID=$(uuidgen 2>/dev/null || echo "$(date +%s)-$(($RANDOM % 10000))")
    sed -i "s|^A0_PERSISTENT_RUNTIME_ID=.*|A0_PERSISTENT_RUNTIME_ID=$NEW_ID|" "$REPO_ROOT/layers/$DEST_CONTAINER/.env"
  else
    touch "$REPO_ROOT/layers/$DEST_CONTAINER/.env"
  fi
fi

LAYERED_ENV_FILE="$REPO_ROOT/layers/$DEST_CONTAINER/.env"

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

# Ensure source profile directory exists under layers
if [ ! -d "$REPO_ROOT/layers/$SOURCE_CONTAINER/agents/$SOURCE_PROFILE" ]; then
  echo "Error: Source profile $SOURCE_PROFILE not found under $REPO_ROOT/layers/$SOURCE_CONTAINER/agents/." >&2
  exit 1
fi

# Navigate to layers
cd "$REPO_ROOT/layers"

# Copy layers contents, preserving existing files
rsync -a --ignore-existing "$SOURCE_CONTAINER/" "$DEST_CONTAINER/"

# Navigate back to container directory
cd "$REPO_ROOT/containers/$DEST_CONTAINER"

# Uncomment the layered .env volume so it mounts into the container as /a0/.env
if [ -f "$REPO_ROOT/layers/$DEST_CONTAINER/.env" ]; then
  sed -i 's/# - \${AGENT_LAYER}\/\.env:\/a0\/\.env:rw/- ${AGENT_LAYER}\/\.env:\/a0\/\.env:rw/' docker-compose.yml
fi

# Navigate to layers for agent customization
cd "$REPO_ROOT/layers"

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
cd "$REPO_ROOT/containers/$DEST_CONTAINER"

# Start Docker containers as the final step (unless no_docker is set)
if [ -n "$NO_DOCKER" ]; then
  echo "Agent $DEST_CONTAINER created and customized successfully (Docker not started)."
  echo "Sensitive layered env for /a0/.env is at /layers/$DEST_CONTAINER/.env"
  echo "You can start the agent later with: docker compose up -d (in containers/$DEST_CONTAINER)."
else
  docker compose up -d
  echo "Agent $DEST_CONTAINER created, customized, and started successfully!"
  echo "Sensitive layered env for /a0/.env is at /layers/$DEST_CONTAINER/.env"
  echo "Access at configured ports (check orchestration .env for PORT_BASE)."
fi
