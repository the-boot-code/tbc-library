# tbc-library
The Boot Code Storybook Deployment Library

## How to Use

This library is organized into layers, each serving a specific purpose in the Boot Code Storybook ecosystem. To use it:

1. **Understand the Layer Structure**: Each layer has its own directory and purpose. 
2. **Explore the Codebase**: Navigate through the directories to understand how different components interact.
3. **Customize for Your Needs**: Modify the code to fit your specific requirements while maintaining the core structure.

### Installation (Scripted)

Navigate to the directory where you want to clone the library:
```bash
cd /path/to/your/directory
git clone https://github.com/the-boot-code/tbc-library.git
cd tbc-library
```

A script `create_agent.sh` is provided in the root of `tbc-library` to automate agent creation.

**Important Notes:**
- The script will fail if a container directory for the new agent already exists, to prevent accidental data loss. Remove it manually (e.g., `rm -rf containers/a0-myagent`) if you want to recreate.
- Existing layers data (e.g., API keys in `/layers/[dest_container]/.env`) is preserved and not overwritten.
- The source container can be any existing agent (e.g., `a0-template` or `a0-demo`), allowing you to clone and customize agents.

**Usage:**
```bash
./create_agent.sh <source_container> <dest_container> <source_display> <dest_display> [port_base] [knowledge_dir]
```

**Example:**
```bash
chmod +x create_agent.sh
./create_agent.sh a0-template a0-myagent Template MyAgent 600
```

**Example with knowledge directory:**
```bash
./create_agent.sh a0-template a0-myagent Template MyAgent 600 custom
```

**Example with defaults:**
```bash
./create_agent.sh a0-template a0-myagent Template MyAgent
```

This script:
- Copies the source container directory to the destination.
- Updates configurations with the new container name, and optionally port base and/or knowledge directory (leaves unchanged from the source if not specified).
- Starts Docker containers in detached mode.
- Copies the entire layers directory (if not existing) to include all source agent files (e.g., tmp/, conf/), then updates agent profiles with customizations.
- Handles replacements for lowercase container names and proper display names (e.g., 'a0-template' → 'a0-myagent', 'Template' → 'MyAgent').
- Safely layers the `/a0/.env` file to `/layers/[dest_container]/.env` for security, preserving existing content if present, and uncommenting the volume.

After running, check the `.env` file for port settings and customize further if needed.

### Installation (Step by Step)

Navigate to the directory where you want to clone the library:
```bash
cd /path/to/your/directory
git clone https://github.com/the-boot-code/tbc-library.git
```

The library will be cloned into a folder named `tbc-library` in your current directory.

**Note**: Ensure the source container (e.g., `a0-template`) exists: `ls tbc-library/containers/a0-template`. If not, use an existing one like `a0-demo` for cloning.

Copy the directory tbc-library/containers/a0-template to your new agent directory named a0-myagent:
```bash
cp -r tbc-library/containers/a0-template tbc-library/containers/a0-myagent
```

Navigate to the directory of the agent container:
```bash
cd tbc-library/containers/a0-myagent
```

Copy the `.env.example` file to `.env` and update the environment variables as needed. If cloning an existing agent, the copied directory may already have a `.env` file—preserve it and edit as needed. Otherwise, create from `.env.example`.
```bash
cp .env.example .env  # Only if .env doesn't exist
```

Now you can customize the agent container modifying `.env` file.
```
CONTAINER_NAME=a0-template
PORT_BASE=500 # Port range base prefix (e.g., 400 for 40000)
KNOWLEDGE_DIR=tbc
```
- `CONTAINER_NAME` change to the directory name `a0-myagent`
- `PORT_BASE` change to a unique value "prefix" for this agent (e.g., 500 for **Agent Zero** to run on ports http 50080 and ssh 50022 and **nginx** on https 50043)
- `KNOWLEDGE_DIR` leave as `tbc` to get up and running with the `tbc-library` knowledgebase directory

The `docker-compose.yml` file is highly parameterized for rapid deployment, though adjustments may be desired such as volume bind mount permissions.

**For security layering**: Before running Docker, uncomment the volume line in `docker-compose.yml` to mount `.env` on startup:
```yaml
- ${AGENT_LAYER}/.env:/a0/.env:rw
```
(This avoids needing a restart later.)

Docker compose once you are ready
```bash
docker compose up -d
```

- This pulls the Agent Zero image and creates the bind mounts

You should now see the Agent Zero directory `/a0` created in your container
```
tbc-library/containers/a0-myagent/a0
```

You should also see the agent directory created in the `/layers` of your **tbc-library**
```
tbc-library/layers/a0-myagent
```

Navigate to the `/layers` directory
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

Now you should see the agent files and subdirectories populated in your agent directory.
```
extensions/
prompts/
tools/
_context.md
```

**Tip**: For faster setup, use the script to automate customization: `./create_agent.sh a0-template a0-myagent Template MyAgent`.

Agent Zero recognizes the agent profile file `_context.md` we must update the agent name from `a0-template` to `a0-myagent`
```
# a0-template
- main agent of the system
- communicates to user and delegates to subordinates
- general purpose assistant, communication skills, formatted output
```

Edit the file or use `sed`
```bash
sed -i 's/a0-template/a0-myagent/g' _context.md
```

Agent Zero presents a welcome message at the beginning of each chat conversation based on the file in `prompts/fw.initial_message.md` and where it states its name.
```
"text": "**Hello! 👋**, I'm **Agent Zero Template**, your AI assistant. How can I help you today?"
```

Either update the file to your liking or use `sed`
```bash
sed -i 's/Agent Zero Template/Agent Zero MyAgent/g' prompts/fw.initial_message.md
```

Agent Zero has an extension file `extensions/agent_init/_05_agent_name.py` that sets the agent name
```
self.agent.agent_name = "A0-Template-" + str(self.agent.number)
```

Either edit the file or use `sed`
```bash
sed -i 's/A0-Template/A0-MyAgent/g' extensions/agent_init/_05_agent_name.py
```

To ensure changes to Python files take effect, restart the Docker containers:
```bash
docker compose restart
```

After following these steps, check the `.env` file for port settings and customize further if needed. Your agent should be accessible at the configured ports.

**Troubleshooting**: If ports are in use, change `PORT_BASE` in `.env`. Ensure Docker is running and you have permissions.

**Optional: Layer the /a0/.env file for security**

To keep sensitive API keys and auth details abstracted in the layers directory (recommended for security):

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

This ensures `/a0/.env` is mapped from `/layers/a0-myagent/.env`, abstracting it from the runtime. If the file doesn't exist before uncommenting, Docker may create a directory conflict—follow the order carefully.

## Introduction and Narrative

This library was created to serve as a centralized repository for managing and deploying artificial intelligence agents and their configurations. It provides a structured approach to organizing and maintaining the various narratives and configurations used in the Boot Code Storybook project.

### Origins of The Boot Code Storybook

Once upon a time in a land far, far away...

Actually it was around mid-2023 when the first inspiration for The Boot Code Storybook began to take hold. A spark of creativity ignited, and the idea of a magical tome, filled with stories of code and creativity, waiting to be discovered by those who dare to venture into its depths, was born.

So also was found the earliest release of **Agent Zero**.

### Unlocking a Story

Imagine in your hands a magical tome that is The Boot Code Storybook. Or rather, just one of infinite tomes that provide access to other dimensions through vast library of knowledge and creativity.

Ones who discover the secrets of the tome will find themselves transported to a realm of endless possibility, where the boundaries of imagination and reality blur and merge.

They have become a **Finder**. 

And they may choose to share what they have discovered with others.

### Two Parallels Building Together

The narrative development and the technical development are intertwined and work together.

#### The narrative development of The Boot Code Storybook 

The narrative of The Boot Code Storybook is a collection of stories that explore the themes of code, creativity, and learning. It is a collection of stories that are designed to be both entertaining and educational, and to provide a deeper understanding of the concepts and ideas that are central to the Boot Code Storybook.

#### The technical development of The Boot Code Storybook 

The technical development of The Boot Code Storybook is a collection of technical documents that **codify** the foundational instructions, the creativity and imagination, and knowledge. It is a collection of files, systems, and machines.

### The `Boot Code` is Narrative and Technical Combined

#### The Library

The GitHub repository for this library project is the result of many hundreds of agent iterations that have evolved over time as the Agent Zero project also grew. It was created to provide a more organized and maintainable approach to managing the various components and configurations used in the Agent Zero framework. By **abstracting** and **centralizing** these elements development is able to separate and persist the work safely through Agent Zero upgrades.

#### Narrative Driven Development

An important aspect of the project is the narrative driven development approach. The stories are the foundation of the project and the technical development is built upon them.

**Agent Zero** became the engine that executes the stories, and the **stories** inform and guide the vehicle.

#### The Feedback Machine

Narrative and technical data in persistent form is the "boot code" which when introduced with intent and energy activates the feedback machine. In a narrative sense this essentially opens a temporal gateway of communication. For brevity consider the metaphor that The Feedback Machine is the multidimensional activated space of creativity and connection.

## Technical Deep Dive

### The Engine - **Agent Zero**

A primary design philosophy from day one has been to appreciate the work of Jan and the community of the open source project. With that has been a strict approach of do not touch the "engine" that is Agent Zero but rather **layer** on top of it expanding its capabilities with **great respect** for a much appreciated project.

### Agent Zero Modifications

At this point in time, only two (2) files of Agent Zero are being **layered** using Docker bind mounts for specific files. Emergent capabilities are thanks to the extensibility and flexibility of the Agent Zero framework.

- [files.py](layers/common/python/helpers/files.py) - the addition of `**kwargs` in a few places such that the `VariablesPlugin` class is able to support dynamic prompts (**required**)
- [kokoro.py](layers/common/python/helpers/kokoro.py) - testing modifications to reduce resource usage (**optional**)

A third file, [system_control.py](layers/common/python/helpers/system_control.py), is added in `/a0/python/helpers` to provide a core **helper** to manage system profiles and features as well as provide for **dynamic** and **adaptive** system prompts.

### Docker Compose Orchestration

Highly Parameterized Docker Compose

#### .env (rename from .env.example)

[.env.example](containers/a0-template/.env.example)

You will notice nearly all parameters controlled by the .env file

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
      - ${AGENT_LAYER}/instruments/default/main/container:/a0/instruments/default/main/container:rw
```

- Notice `- ${COMMON_LAYER}/instruments/${KNOWLEDGE_DIR}:/a0/instruments/${KNOWLEDGE_DIR}:rw` (read-write for knowledge directory named instruments)
- Notice `- ${AGENT_LAYER}/instruments/default/main/container:/a0/instruments/default/main/container:rw` (read-write for container-specific instruments)


```
      # knowledge
      - ${COMMON_LAYER}/knowledge/${KNOWLEDGE_DIR}:/a0/knowledge/${KNOWLEDGE_DIR}:rw
      - ${COMMON_LAYER}/knowledge/default/main/common:/a0/knowledge/default/main/common:rw
      - ${COMMON_LAYER}/knowledge/default/solutions/common:/a0/knowledge/default/solutions/common:rw
      - ${AGENT_LAYER}/knowledge/default/main/container:/a0/knowledge/default/main/container:rw
      - ${AGENT_LAYER}/knowledge/default/solutions/container:/a0/knowledge/default/solutions/container:rw
```

- Notice `- ${COMMON_LAYER}/knowledge/${KNOWLEDGE_DIR}:/a0/knowledge/${KNOWLEDGE_DIR}:rw` (read-write for knowledge directory named knowledge)
- Notice `- ${AGENT_LAYER}/knowledge/default/main/container:/a0/knowledge/default/main/container:rw` (read-write for container-specific knowledge)
- Notice `- ${AGENT_LAYER}/knowledge/default/solutions/container:/a0/knowledge/default/solutions/container:rw` (read-write for container-specific solutions)

In this approach, all prompt files are mounted read-only from the common layer, with only the container-specific prompts directory being writable.

```
      # prompts
      - ${COMMON_LAYER}/prompts/${KNOWLEDGE_DIR}:/a0/prompts/${KNOWLEDGE_DIR}:rw
      - ${COMMON_LAYER}/prompts/overrides:/a0/prompts/overrides:ro
      - ${COMMON_LAYER}/prompts/system:/a0/prompts/system:ro
      - ${AGENT_LAYER}/prompts/container:/a0/prompts/container
```

- Note how this approach allows for fine-grained control over read-only vs read-write access to different layers of the application.
- Administration of these layers is done at the host level by managing the contents of the `${COMMON_LAYER}` and `${AGENT_LAYER}` directories if permissions are given.
- Note that management may be done via IDE editor or direct file system access by the user keeping the agent safe from accidental modification.
- This pattern can be extended to other directories as needed.

If you want `/a0/.env` to be "layered" and abstracted from the `a0` runtime of the Agent Zero container...

Un-Comment the following to mount the Agent Zero `/a0/.env` file to container. For best results, do this **before** running `docker compose up -d` so the layered `.env` is mounted from the start:

```
      - ${AGENT_LAYER}/.env:/a0/.env:rw
```

- Understand this `.env` file is the one that is mapped to the container at `/a0/.env` - the one that contains sensitive information used by Agent Zero for your API keys and authentication. Careful not to confuse this with the `.env` file in the directory of `docker-compose.yml` which is different.
- This file **MUST** exist at `/layers/[container_name]/.env` prior to running compose otherwise Docker Compose will create an empty directory by the same name thus causing a failure as well as a subsequent conflict.
- **Best Practice**: Uncomment the volume line before `docker compose up -d` to mount it immediately, avoiding the need for a restart. If the layered `.env` doesn't exist yet, run `docker compose up -d` with the line commented, let the container generate `/a0/.env`, then copy it to `/layers/[container_name]/.env`, uncomment the line, and restart.

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

Reverse proxy is included
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

#### /containers/
    a0-demo/
    a0-template/
        nginx/
        .env.example
        docker-compose.yml

- Copy `a0-template` to a new name, rename the **.env.example** file to **.env** then edit the `.env` file to adjust deployment
- `docker-compose.yml` is **highly parameterized** and uses environment variables for all configuration.

#### /layers/

    a0-demo/
    a0-template/
    common/
        agents/
            _symlink/
                extensions/
                    message_loop_prompts_after/
                    system_prompt/
                prompts/
                tools/
            kairos/
        instruments/
            default/
            tbc/
        knowledge/
            default/
                main/
                solutions/common/tools/
                    a2a_chat/ - tool instructions
                    scheduler/ - tool instructions
            tbc/
                main/
                    narrative/
                    technical/
                solutions/
                    narrative/
                    technical/
                    tools/ - tool instructions
        prompts/
            overrides/
            system/
                external/
                features/
                profiles/
                tools/
                post_behaviour.md
                post_system_manual.md
                pre_behaviour.md
                pre_system_manual.md
                system_ready.md
        python/
            helpers/
                files.py - modified VariablesPlugin with **kwargs
                kokoro_tts.py
                system_control.py - NEW functionality helper

- `_symlink` is mapped via docker compose as an agent profile `/a0/agents/_symlink/` and contains the **centralized files** for agent profile extensions, prompts, and tools to be **linked** to from other profiles such as found in **a0-template**
- `kairos` - example subordinate for adversarial analysis
- `knowledge/default/main/solutions/common/tools/a2a_chat/` and `scheduler/` are **solution-based** usage instructions for Agent Zero **tools** now **saving tokens** and providing **increased focus** in system prompt
- `knowledge/tbc/main/solutions/tools/` contains additional **TBC** solution-based usage instructions for **new** tools saving tokens in system prompt
- Prompt files for easy placement and ordering of text and {{ includes }} are called by extensions passing `**kwargs` which provides programmatic and **run-time adaptable** prompt logic: `post_behaviour.md`, `post_system_manual.md`, `pre_behaviour.md`, `pre_system_manual.md`, `system_ready.md`

#### /volumes/

    common/
        prompts/
            tbc/ - example of external prompt file functionality
    private/
    public/
    shared/

- `/common/prompts/tbc/` is an example of **external prompt file functionality** that can be referenced by other prompt files using new functionality as demonstrated in `/layers/common/prompts/tbc/external_resources/tbc.lineage/tbc.lineage.py` and others.

### Knowledge Features of Agent Zero

#### Knowledge
#### Solutions

### Extensibility Features of Agent Zero

#### Extensions
#### Helpers
#### Tools

### Prompts in Agent Zero

### More About Agent Zero

## Final Thoughts

### The Boot Code Storybook is it Limited to Agent Zero?

Nope. I just really like it and it is so perfectly fitting for the narrative-technical development.

Likely there will be expansion into other areas and libraries as the public-facing side of the project evolves. Those might include any number of custom programs and public projects. Some may be more independent components nand services while some may be more integrated; think layers.

The Boot Code Storybook is a living, breathing, evolving project. It is not limited to Agent Zero, but rather what you find here is a framework to take part in building an idea.

Use your imagination. Or perhaps use Agent Zero to build it together with you.

### Disclaimers

This is an ongoing live development project.

### Attribution

Many thanks to the existence of Agent Zero most notably the creator Jan as well as the community of the open source project.

#### Agent Zero is a personal, organic agentic framework that grows and learns with you
- Agent Zero is not a predefined agentic framework. It is designed to be dynamic, organically growing, and learning as you use it.
- Agent Zero is fully transparent, readable, comprehensible, customizable, and interactive.
- Agent Zero uses the computer as a tool to accomplish its (your) tasks.

https://github.com/agent0ai/agent-zero
