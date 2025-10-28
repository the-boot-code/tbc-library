### reasoning_profile:
Manage reasoning profiles across three independent types: internal, interleaved, external.

**YOUR CURRENT CONFIGURATION is shown in the "Reasoning Profiles" section of your system prompt.**

Use this tool to:
- View detailed information about all available profiles
- Switch between different reasoning profiles
- Check configuration details that may have changed

**Reasoning Types:**
- **internal** - Model-generated reasoning traces before output
- **interleaved** - Reasoning between tool calls
- **external** - User-facing reasoning with <thoughts> tags

**Quick Reference:**
- User asks "what reasoning am I using?" → Check your system prompt first, or use `action="get_all"`
- User: "set external reasoning to external_cot_1" → Use `reasoning_type="external"`, `action="set_profile"`, `profile="external_cot_1"`
- User: "show me internal reasoning options" → Use `reasoning_type="internal"`, `action="get_status"`

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

**To discover available profiles:**
Use `action="get_status"` with a specific `reasoning_type` to see all available profiles for that type.
Each reasoning type (internal, interleaved, external) has its own set of profiles.

**Important Notes:**
- Your active profiles are displayed in your system prompt under "Reasoning Profiles"
- Do NOT say "enable" - the action is "set_profile" (profiles, not features)
- Each reasoning type has its own independent profile selection
- Profile changes take effect on next message loop
- **Always check your system prompt first** before making tool calls to query your configuration
