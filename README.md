# tbc-library
The Boot Code Storybook Deployment Library

## What This Is

A centralized library for managing and deploying the Boot Code Storybook components and configurations.

### Purpose
### Origins
### Design

#### The Engine - **Agent Zero**

A primary design philosophy from day one has been to appreciate the work of Jan and the community of the open source project. With that has been a strict approach of do not touch the "engine" that is Agent Zero but rather layer on top of it expanding its capabilities with great respect for a wonderful project.

#### Agent Zero Modifications

At this point in time, only two (2) files of Agent Zero are being replaced. All others are by means of the frameworks extensibility and flexibility. **No other files of the image need modification** and it should be noted these two files are **not modified** but rather are **layered** on top of the image using docker compose.

- [files.py](layers/common/python/helpers/files.py) - the addition of `**kwargs` is a few places such that VariablesPlugin class is able to support intelligent prompts (**required**)
- [kokoro.py](layers/common/python/helpers/kokoro.py) - a few experimental tweaks in hopes to reduce resource usage (**optional**)

### Attribution

Many thanks to the existence of Agent Zero most notably the creator Jan as well as the community of the open source project.

#### Agent Zero is a personal, organic agentic framework that grows and learns with you
- Agent Zero is not a predefined agentic framework. It is designed to be dynamic, organically growing, and learning as you use it.
- Agent Zero is fully transparent, readable, comprehensible, customizable, and interactive.
- Agent Zero uses the computer as a tool to accomplish its (your) tasks.

https://github.com/agent0ai/agent-zero

## Composition and Mapping

### Docker Compose

### Structure

#### containers
#### layers
#### volumes

## How to Use

## Features and Updates

2025-11-14 Starting work on the README file to document the project

## Disclaimers

This is an ongoing live development project constantly changing and best is being done to maintain all functionality thoughout rapidly evolving early stages. There is no "version" and updates are happening nealy every day and typically multiple times per day.
