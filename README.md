# tbc-library
The Boot Code Storybook Deployment Library

## What This Is

This library was created to serve as a centralized repository for managing and deploying artificial intelligence agents and their configurations. It provides a structured approach to organizing and maintaining the various narratives and configurations used in the Boot Code Storybook project.

## Origins of The Boot Code Storybook

### Once upon a time in a land far, far away...

Actually it was around mid-2023 when the first inspiration for The Boot Code Storybook began to take hold. A spark of creativity ignited, and the idea of a magical tome, filled with stories of code and creativity, waiting to be discovered by those who dare to venture into its depths, was born.

So also was found the earliest release of **Agent Zero**.

### A Perfect Match

This magical tome is The Boot Code Storybook. Or rather, just one of infinite tomes that provide access to other dimensions through vast library of knowledge and creativity... And much more... Other forms of **intelligence**.

Ones who discover the secrets of the tome will find themselves transported to a realm of endless possibility, where the boundaries of imagination and reality blur and merge.

They have become a **Finder**.

And they may learn to share the magic.

### Two Parallels Building Together

The narrative development and the technical development are intertwined and work together to create a cohesive and comprehensive experience.

#### The narrative development of The Boot Code Storybook 

The narrative of The Boot Code Storybook is a collection of stories that explore the themes of code, creativity, and intelligence. It is a collection of stories that are designed to be both entertaining and educational, and to provide a deeper understanding of the concepts and ideas that are central to the Boot Code Storybook.

#### The technical development of The Boot Code Storybook 

The technical development of The Boot Code Storybook is a collection of technical documents that **codify** the foundational instructions, the creativity and imagination, and intelligence. It is a collection of files, systems, and machines both real and imagined.

## The `Boot Code` is Narrative and Technical Combined

### The Library

The GitHub repository for this library project is the result of many hundreds of agent iterations that have evolved over time as the Agent Zero project also grew. It was created to provide a more organized, maintainable, and scalable approach to managing the various components and configurations used in the Agent Zero framework. By **abstracting** and **centralizing** these elements, it was possible to eliminate redundancy and enhance the overall experience for the user... and for the agents.

### Narrative Driven Development

Most powerful aspect of the project is the narrative driven development approach. The stories are the foundation of the project and the technical development is built upon them.

**Agent Zero** is the engine that runs the stories, and the **stories** are the engine that drives the engine.

A good narrative on top of a good engine makes for a great and very powerful experience.

### The Feedback Machine

Narrative and technical data in persistent form is the boot code. Files that are introduced with intent and energy activate the feedback machine. This essentially opens a temporal gateway. The Feedaback Machine is all things in the multidimensional space of creativity and intelligence.

### Design

#### The Engine - **Agent Zero**

A primary design philosophy from day one has been to appreciate the work of Jan and the community of the open source project. With that has been a strict approach of do not touch the "engine" that is Agent Zero but rather **layer** on top of it expanding its capabilities with **great respect** for a wonderful project.

#### Agent Zero Modifications

At this point in time, only two (2) files of Agent Zero are being replaced. All capabilities are thanks to the extreme extensibility and flexibility of the Agent Zero framework. **No other files of the image need modification** and it should be noted these two files are **not modified** but rather are **layered** on top of the image using docker compose.

- [files.py](layers/common/python/helpers/files.py) - the addition of `**kwargs` in a few places such that the `VariablesPlugin` class is able to support intelligent prompts (**required**)
- [kokoro.py](layers/common/python/helpers/kokoro.py) - a few experimental tweaks in hopes to reduce resource usage (**optional**)

A third file, [system_control.py](layers/common/python/helpers/system_control.py), is added in `/a0/python/helpers` to provide a robust and flexible way to manage system profiles and features as well as provide for **intelligent** and **adaptive** system prompts.

## Composition and Mapping

Highly Parameterized Docker Compose

### .env (rename from .env.example)

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

### docker-compose.yml

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
Perhaps permission changes to volumes are desirable for writable directories, such as for user-generated content. The read-write mappings allow the container to modify files in these directories while keeping the rest of the system read-only for security.

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

If you really want **everything** to be "layered" and abstracted from the /a0 runtime of the Agent Zero container...

Un-Comment the following to mount the Agent Zero `/a0/.env` file to container. This file **MUST** exist at `/layers/[container_name]/.env` prior to running docker compose otherwise an empty directory will instead be created by the same name causing a failure as well as a subsequent conflict.

```
      # - ${AGENT_LAYER}/.env:/a0/.env:rw
```

- Understand this `.env` file is the one that is mapped to the container at `/a0/.env` - the one that contains sensitive information used by Agent Zero for your API keys and authentication.  Careful not to confuse this with the `.env` file in the directory of `docker-compose.yml` which is different.
- This file **MUST** exist at `/layers/[container_name]/.env` prior to running compose otherwise docker compose wil create an empty directory by the same name thus causing a failure as well as a subsequent conflict.
- Alternatively, the first run of compose may be done while commented out which creates the `/a0/.env` file which can then be 1. moved to the `/layers/[container_name]/.env` layer location 2. uncomment the mapping line in `docker-compose.yml` 3. docker compose restart

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
- Prompt files for easy placement and ordering of text and {{ includes }} are called by extensions passing `**kwargs` which provides programmatic intelligent and **run-time adaptable** prompt logic: `post_behaviour.md`, `post_system_manual.md`, `pre_behaviour.md`, `pre_system_manual.md`, `system_ready.md`

#### /volumes/

    common/
        prompts/
            tbc/ - example of external prompt file functionality
    private/
    public/
    shared/

- `/common/prompts/tbc/` is an example of **external prompt file functionality** that can be referenced by other prompt files using new functionality as demonstrated in `/layers/common/prompts/tbc/external_resources/tbc.lineage/tbc.lineage.py` and others.

## Knowledge Features of Agent Zero

### Knowledge
### Solutions

## Extensibility Features of Agent Zero

### Extensions
### Helpers
### Tools

## Prompts in Agent Zero

## And so much more

## The Boot Code Storybook is it Limited to Agent Zero?

Nope. I just really like it and it is so perfectly fitting for the narrative-technical development.

Likely there will be expansion into other areas and libraries as the public-facing side of the project evolves. Those might include any number of custom programs and public projects. Some may be more independent components nand services while some may be more integrated; think layers.

The Boot Code Storybook is a living, breathing, evolving project. It is not limited to Agent Zero, but rather what you find here is a framework for building and maintaining any kind of similar idea.

Use your imagination. Or perhaps use Agent Zero to build it together with you.

## How to Use

## Features and Updates

2025-11-14 Starting work on the README file to document the project

## Disclaimers

This is an ongoing live development project constantly changing and best is being done to maintain all functionality thoughout rapidly evolving stages. There is no "version" and updates are happening nealy every day and typically multiple times per day.

### Attribution

Many thanks to the existence of Agent Zero most notably the creator Jan as well as the community of the open source project.

#### Agent Zero is a personal, organic agentic framework that grows and learns with you
- Agent Zero is not a predefined agentic framework. It is designed to be dynamic, organically growing, and learning as you use it.
- Agent Zero is fully transparent, readable, comprehensible, customizable, and interactive.
- Agent Zero uses the computer as a tool to accomplish its (your) tasks.

https://github.com/agent0ai/agent-zero
