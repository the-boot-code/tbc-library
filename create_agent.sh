#!/bin/bash

# Usage: ./create_agent.sh <source_container> <dest_container> <source_display> <dest_display> [port_base] [knowledge_dir]
# Example: ./create_agent.sh a0-template a0-myagent Template MyAgent 600
# Example with knowledge_dir: ./create_agent.sh a0-template a0-myagent Template MyAgent 600 custom
# Example with defaults: ./create_agent.sh a0-template a0-myagent Template MyAgent

if [ $# -lt 4 ] || [ $# -gt 6 ]; then
  echo "Usage: $0 <source_container> <dest_container> <source_display> <dest_display> [port_base] [knowledge_dir]"
  echo "Example: $0 a0-template a0-myagent Template MyAgent 600"
  echo "Example with knowledge_dir: $0 a0-template a0-myagent Template MyAgent 600 custom"
  echo "Example with defaults: $0 a0-template a0-myagent Template MyAgent"
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

TEMPLATE_NAME=$1
NEW_AGENT=$2
TEMPLATE_DISPLAY=$3
MY_DISPLAY=$4
if [ $# -ge 5 ]; then
  PORT_BASE=$5
fi
if [ $# -eq 6 ]; then
  KNOWLEDGE_DIR=$6
fi

echo "Creating agent: $NEW_AGENT from $TEMPLATE_NAME"

# Step 1: Check if source container exists
if [ ! -d "$REPO_ROOT/containers/$TEMPLATE_NAME" ]; then
  echo "Error: Source container $TEMPLATE_NAME not found in $REPO_ROOT/containers/."
  exit 1
fi

# Step 2: Check if container already exists
if [ -d "$REPO_ROOT/containers/$NEW_AGENT" ]; then
  echo "Error: Container directory $REPO_ROOT/containers/$NEW_AGENT already exists. Remove it manually if you want to recreate."
  exit 1
fi

# Step 3: Copy container directory
cp -r "$REPO_ROOT/containers/$TEMPLATE_NAME" "$REPO_ROOT/containers/$NEW_AGENT"

# Step 4: Enter container directory
cd "$REPO_ROOT/containers/$NEW_AGENT"

# Step 5: Copy .env file if not exists
if [ ! -f .env ]; then
  cp .env.example .env
fi

# Step 6: Update CONTAINER_NAME in .env
sed -i "s/$TEMPLATE_NAME/$NEW_AGENT/" .env

# Step 7: Update PORT_BASE in .env if provided
if [ -n "$PORT_BASE" ]; then
  sed -i "s/^PORT_BASE=.*/PORT_BASE=$PORT_BASE/" .env
fi

# Step 8: Update KNOWLEDGE_DIR in .env if provided
if [ -n "$KNOWLEDGE_DIR" ]; then
  sed -i "s/^KNOWLEDGE_DIR=.*/KNOWLEDGE_DIR=$KNOWLEDGE_DIR/" .env
fi

if [ -n "$PORT_BASE" ] && [ -n "$KNOWLEDGE_DIR" ]; then
  echo "Updated .env: CONTAINER_NAME=$NEW_AGENT, PORT_BASE=$PORT_BASE, KNOWLEDGE_DIR=$KNOWLEDGE_DIR"
elif [ -n "$PORT_BASE" ]; then
  echo "Updated .env: CONTAINER_NAME=$NEW_AGENT, PORT_BASE=$PORT_BASE"
elif [ -n "$KNOWLEDGE_DIR" ]; then
  echo "Updated .env: CONTAINER_NAME=$NEW_AGENT, KNOWLEDGE_DIR=$KNOWLEDGE_DIR"
else
  echo "Updated .env: CONTAINER_NAME=$NEW_AGENT"
fi
echo "Note: Update PORT_BASE if needed for unique ports."

# Step 9: Create layers directory and .env from source if available, with new runtime ID
mkdir -p "$REPO_ROOT/layers/$NEW_AGENT"
if [ ! -f "$REPO_ROOT/layers/$NEW_AGENT/.env" ]; then
  if [ -f "$REPO_ROOT/layers/$TEMPLATE_NAME/.env" ]; then
    cp "$REPO_ROOT/layers/$TEMPLATE_NAME/.env" "$REPO_ROOT/layers/$NEW_AGENT/.env"
    # Generate a new A0_PERSISTENT_RUNTIME_ID
    NEW_ID=$(uuidgen 2>/dev/null || echo "$(date +%s)-$(($RANDOM % 10000))")
    sed -i "s/A0_PERSISTENT_RUNTIME_ID=.*/A0_PERSISTENT_RUNTIME_ID=$NEW_ID/" "$REPO_ROOT/layers/$NEW_AGENT/.env"
  else
    touch "$REPO_ROOT/layers/$NEW_AGENT/.env"
  fi
fi

# Step 10: Navigate to layers
cd "$REPO_ROOT/layers"

# Step 11: Copy layers contents, preserving existing files
rsync -a --ignore-existing "$TEMPLATE_NAME/" "$NEW_AGENT/"

# Step 12: Navigate back to container directory
cd "$REPO_ROOT/containers/$NEW_AGENT"

# Step 13: Uncomment the .env volume if .env exists
if [ -f "$REPO_ROOT/layers/$NEW_AGENT/.env" ]; then
  sed -i 's/# - \${AGENT_LAYER}\/.env:\/a0\/.env:rw/- ${AGENT_LAYER}\/.env:\/a0\/.env:rw/' docker-compose.yml
fi

# Step 14: Start Docker containers
docker compose up -d

# Step 15: Navigate to layers for agent customization
cd "$REPO_ROOT/layers"

# Step 15: Create agent profile directory
rm -rf "$NEW_AGENT/agents/$NEW_AGENT"
mkdir -p "$NEW_AGENT/agents/$NEW_AGENT"

# Step 16: Copy agent profile from template
cp -r "$TEMPLATE_NAME/agents/$TEMPLATE_NAME/"* "$NEW_AGENT/agents/$NEW_AGENT/"

# Step 17: Enter agent profile directory
cd "$NEW_AGENT/agents/$NEW_AGENT"

# Step 18: Update _context.md
sed -i "s/$TEMPLATE_NAME/$NEW_AGENT/g" _context.md

# Step 19: Update fw.initial_message.md
sed -i "s/Agent Zero $TEMPLATE_DISPLAY/Agent Zero $MY_DISPLAY/g" prompts/fw.initial_message.md

# Step 20: Update agent_init/_05_agent_name.py
sed -i "s/A0-$TEMPLATE_DISPLAY/A0-$MY_DISPLAY/g" extensions/agent_init/_05_agent_name.py

echo "Agent $NEW_AGENT created and customized successfully!"
echo "Sensitive .env layered in /layers/$NEW_AGENT/.env"
echo "Access at configured ports (check .env for PORT_BASE)."
