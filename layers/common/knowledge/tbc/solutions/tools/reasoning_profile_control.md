# Reasoning Profile Control

## Problem

How to use the reasoning_profile_control tool

Manage reasoning profiles across three independent types: internal, interleaved, and external.

## Solution

**ACTIVE PROFILES**: Displayed in "Reasoning Profiles" section of system prompt.

**Reasoning Types:**
- **internal** - Model-generated reasoning traces before output
- **interleaved** - Reasoning between tool calls  
- **external** - User-facing reasoning with <thoughts> tags

**Quick Reference:**
- "what reasoning am I using?" → **Check system prompt first** or `action="get_all"`
- "show reasoning options" → `action="get_all"` or `action="get_state"` with `reasoning_type`
- "set external to external_cot_1" → `reasoning_type="external"`, `action="set_profile"`, `profile="external_cot_1"`

**Available actions:**
- **get_all** – View all three reasoning types and their active profiles.
- **get_state** – View detailed state for a specific reasoning type (requires `reasoning_type`).
- **get_profile** – View just the active profile for a specific reasoning type (requires `reasoning_type`).
- **set_profile** – Change the reasoning profile for a specific type (requires `reasoning_type` and `profile`).

**JSON example patterns**

_Get all reasoning profiles_

```json
{
  "thoughts": ["See all reasoning types and their active profiles"],
  "headline": "Show all reasoning profiles",
  "tool_name": "reasoning_profile_control",
  "tool_args": {
    "action": "get_all"
  }
}
```

_Get state for a specific type_

```json
{
  "thoughts": ["Inspect internal reasoning profile options"],
  "headline": "Show internal reasoning profile state",
  "tool_name": "reasoning_profile_control",
  "tool_args": {
    "action": "get_state",
    "reasoning_type": "internal"
  }
}
```

_Set profile for a specific type_

```json
{
  "thoughts": ["Use external_cot_1 for external reasoning"],
  "headline": "Set external reasoning profile",
  "tool_name": "reasoning_profile_control",
  "tool_args": {
    "action": "set_profile",
    "reasoning_type": "external",
    "profile": "external_cot_1"
  }
}
```

**Important Notes:**
- Active profiles displayed in system prompt
- Each reasoning type configured independently
- Use `action="set_profile"` (not "enable") for profiles
- Changes take effect immediately on next message loop
- **Check system prompt first** before querying configuration
- Use `get_state` to discover available profiles for each type
