### reasoning_profile:
Manage reasoning profiles across three independent types: internal, interleaved, external.
Select and switch between different reasoning profiles for each type.
Requires "reasoning_control" feature to be enabled.

**Reasoning Types:**
- **internal** - Model-generated reasoning traces before output
- **interleaved** - Reasoning between tool calls
- **external** - User-facing reasoning with <thoughts> tags

**Quick Reference:**
- User: "set external reasoning to external_cot_1" → Use `reasoning_type="external"`, `action="set_profile"`, `profile="external_cot_1"`
- User: "show me internal reasoning options" → Use `reasoning_type="internal"`, `action="get_status"`
- User: "what reasoning am I using?" → Use `action="get_all"`

**Actions:**

**get_all** - View all reasoning types and their active profiles
~~~json
{
    "thoughts": [
        "I need to see the current state of all reasoning types"
    ],
    "headline": "Checking all reasoning profiles",
    "tool_name": "reasoning_control",
    "tool_args": {
        "action": "get_all"
    }
}
~~~

**get_status** - View full reasoning state for a specific type
~~~json
{
    "thoughts": [
        "I need to check the internal reasoning configuration"
    ],
    "headline": "Checking internal reasoning status",
    "tool_name": "reasoning_control",
    "tool_args": {
        "reasoning_type": "internal",
        "action": "get_status"
    }
}
~~~

**get_profile** - View active reasoning profile for a specific type
~~~json
{
    "thoughts": [
        "What interleaved reasoning profile am I using?"
    ],
    "headline": "Checking interleaved reasoning profile",
    "tool_name": "reasoning_control",
    "tool_args": {
        "reasoning_type": "interleaved",
        "action": "get_profile"
    }
}
~~~

**set_profile** - Change reasoning profile for a specific type
~~~json
{
    "thoughts": [
        "User wants external_cot_1, I need to set the external reasoning profile"
    ],
    "headline": "Setting external reasoning to external_cot_1",
    "tool_name": "reasoning_control",
    "tool_args": {
        "reasoning_type": "external",
        "action": "set_profile",
        "profile": "external_cot_1"
    }
}
~~~

**Usage Pattern:**
- User says: "set external reasoning to external_cot_1"
- You use: `reasoning_type="external"`, `action="set_profile"`, `profile="external_cot_1"`

**Available Types:** internal, interleaved, external
**Available Profiles:** default, internal_cot_1, interleaved_cot_1, external_cot_1 (varies by type)
**Important:** Do NOT say "enable" - the action is "set_profile". Avoid confusion between enabling features vs selecting profiles.
**Note:** Each reasoning type has its own profile selection. Profile changes take effect on next message loop.
**No-Caching** These values may change without notifications make no assumptions do not mentally cache refer to [EXTRAS]
