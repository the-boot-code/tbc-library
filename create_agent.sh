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

# Step 1: Check if container already exists
if [ -d "containers/$NEW_AGENT" ]; then
  echo "Error: Container directory containers/$NEW_AGENT already exists. Remove it manually if you want to recreate."
  exit 1
fi

# Step 2: Copy container directory
cp -r containers/$TEMPLATE_NAME containers/$NEW_AGENT

# Step 3: Enter container directory
cd containers/$NEW_AGENT

# Step 4: Copy .env file
cp .env.example .env

# Step 5: Update CONTAINER_NAME in .env
sed -i "s/$TEMPLATE_NAME/$NEW_AGENT/" .env

# Step 6: Update PORT_BASE in .env if provided
if [ -n "$PORT_BASE" ]; then
  sed -i "s/^PORT_BASE=.*/PORT_BASE=$PORT_BASE/" .env
fi

# Step 7: Update KNOWLEDGE_DIR in .env if provided
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

# Step 8: Create layers directory and empty .env if not exists
mkdir -p ../../layers/$NEW_AGENT
if [ ! -f ../../layers/$NEW_AGENT/.env ]; then
  touch ../../layers/$NEW_AGENT/.env
fi

# Step 9: Start Docker containers
docker compose up -d

# Step 10: Navigate to layers
cd ../../layers

# Step 11: Copy layers contents, preserving existing files
rsync -a --ignore-existing $TEMPLATE_NAME/ $NEW_AGENT/

# Step 12: Create agent profile directory
rm -rf $NEW_AGENT/agents/$NEW_AGENT
mkdir -p $NEW_AGENT/agents/$NEW_AGENT

# Step 13: Copy agent profile from template
cp -r $TEMPLATE_NAME/agents/$TEMPLATE_NAME/* $NEW_AGENT/agents/$NEW_AGENT/

# Step 14: Enter agent profile directory
cd $NEW_AGENT/agents/$NEW_AGENT

# Step 15: Update _context.md
sed -i "s/$TEMPLATE_NAME/$NEW_AGENT/g" _context.md

# Step 16: Update fw.initial_message.md
sed -i "s/Agent Zero $TEMPLATE_DISPLAY/Agent Zero $MY_DISPLAY/g" prompts/fw.initial_message.md

# Step 17: Update agent_init/_05_agent_name.py
sed -i "s/A0-$TEMPLATE_DISPLAY/A0-$MY_DISPLAY/g" extensions/agent_init/_05_agent_name.py

echo "Layering /a0/.env for security..."
cd ../../../../containers/$NEW_AGENT
if [ ! -s ../../layers/$NEW_AGENT/.env ]; then
  docker cp $NEW_AGENT:/a0/.env ../../layers/$NEW_AGENT/.env
  echo "Copied generated .env to layers."
else
  echo "Preserving existing .env in layers."
fi
sed -i 's/# - \${AGENT_LAYER}\/.env:\/a0\/.env:rw/- ${AGENT_LAYER}\/.env:\/a0\/.env:rw/' docker-compose.yml
docker compose restart
cd ../../../../  # Back to root

echo "Agent $NEW_AGENT created and customized successfully!"
echo "Sensitive .env handled in /layers/$NEW_AGENT/.env"
echo "Access at configured ports (check .env for PORT_BASE)."
