### reasoning_profile_control:
Manage reasoning profiles across three independent types: internal, interleaved, and external.

**ACTIVE PROFILES**: Displayed in "Reasoning Profiles" section of system prompt.

**Reasoning Types:**
- **internal** - Model-generated reasoning traces before output
- **interleaved** - Reasoning between tool calls  
- **external** - User-facing reasoning with <thoughts> tags

**Quick Reference:**
- "what reasoning am I using?" → **Check system prompt first** or `action="get_all"`
- "show reasoning options" → `action="get_all"` or `action="get_status"` with `reasoning_type`
- "set external to external_cot_1" → `reasoning_type="external"`, `action="set_profile"`, `profile="external_cot_1"`

**Available Actions:**
**get_all** - View all three reasoning types and their active profiles
**get_status** - View detailed state for specific reasoning type (requires `reasoning_type`)
**get_profile** - View just active profile for specific reasoning type (requires `reasoning_type`)
**set_profile** - Change reasoning profile for specific type (requires `reasoning_type` and `profile`)

**JSON Example Pattern:**
~~~json
{
    "thoughts": ["User request description"],
    "headline": "Action description",
    "tool_name": "reasoning_profile_control",
    "tool_args": {
        "action": "action_name",
        "reasoning_type": "internal|interleaved|external",
        "parameter": "value"
    }
}
~~~

**Important Notes:**
- Active profiles displayed in system prompt
- Each reasoning type configured independently
- Use `action="set_profile"` (not "enable") for profiles
- Changes take effect immediately on next message loop
- **Check system prompt first** before querying configuration
- Use `get_status` to discover available profiles for each type
