# prompt_include_control

## Problem

Manage individual SystemControl prompt-includes and System Control tools (enable/disable options).
This tool updates the `prompt_includes` and `system_control_tools` sections of `system_control.json`.
The effective enabled/disabled state can still be overridden by the active security profile (and
admin override).

**Available actions:**

- **get_all** – List all prompt-includes and System Control tools, showing effective status and
  configuration source.
- **get_entry** – Inspect a specific entry. When `entry` is omitted, returns a summary of all
  entries.
- **set_entry** – Enable or disable a specific entry (requires `entry` and `enabled`).

## Solution

**JSON example patterns**

_Get all entries_

```json
{
  "thoughts": ["Review current SystemControl prompt-includes/tools"],
  "headline": "List prompt include status",
  "tool_name": "prompt_include_control",
  "tool_args": {
    "action": "get_all"
  }
}
```

_Get a single entry_

```json
{
  "thoughts": ["Check if reasoning_profiles aggregate include is enabled"],
  "headline": "Check reasoning_profiles status",
  "tool_name": "prompt_include_control",
  "tool_args": {
    "action": "get_entry",
    "entry": "reasoning_profiles"
  }
}
```

_Enable or disable an entry_

```json
{
  "thoughts": ["Enable reasoning_external_profile prompt include"],
  "headline": "Enable external reasoning profile include",
  "tool_name": "prompt_include_control",
  "tool_args": {
    "action": "set_entry",
    "entry": "reasoning_external_profile",
    "enabled": true
  }
}
```

**Important notes**

- Active security profile may override the stored setting when computing the effective status.
- The `prompt_include_control` tool itself is gated by SystemControl; it must be enabled as a
  prompt-include.
- Values may change over time; use `get_all` or `get_entry` to confirm current state before
  relying on it.
