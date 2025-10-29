### reasoning_profile_control:
Manage reasoning profiles across three independent types: internal, interleaved, and external.

**YOUR ACTIVE PROFILES are displayed in the "Reasoning Profiles" section of your system prompt.**

**Reasoning Types:**
- **internal** - Model-generated reasoning traces before output
- **interleaved** - Reasoning between tool calls  
- **external** - User-facing reasoning with <thoughts> tags

**Quick Reference:**
- User asks "what reasoning am I using?" → **Check your system prompt first**, or use `action="get_all"`
- User asks "show me reasoning options" → Use `action="get_all"` or `action="get_status"` with specific `reasoning_type`
- User says "set external reasoning to external_cot_1" → Use `reasoning_type="external"`, `action="set_profile"`, `profile="external_cot_1"`

**Available Actions:**

**get_all** - View all three reasoning types and their active profiles
~~~json
{
    "thoughts": ["User wants to see current reasoning configuration across all types"],
    "headline": "Checking all reasoning profiles",
    "tool_name": "reasoning_profile_control",
    "tool_args": {
        "action": "get_all"
    }
}
~~~

**get_status** - View detailed state for a specific reasoning type (requires `reasoning_type`)
~~~json
{
    "thoughts": ["User wants to see available internal reasoning profiles"],
    "headline": "Checking internal reasoning profile status",
    "tool_name": "reasoning_profile_control",
    "tool_args": {
        "reasoning_type": "internal",
        "action": "get_status"
    }
}
~~~

**get_profile** - View just the active profile for a specific reasoning type (requires `reasoning_type`)
~~~json
{
    "thoughts": ["What interleaved reasoning profile am I currently using?"],
    "headline": "Checking active interleaved reasoning profile",
    "tool_name": "reasoning_profile_control",
    "tool_args": {
        "reasoning_type": "interleaved",
        "action": "get_profile"
    }
}
~~~

**set_profile** - Change reasoning profile for a specific type (requires `reasoning_type` and `profile`)
~~~json
{
    "thoughts": ["User wants external_cot_1 for external reasoning"],
    "headline": "Switching to external_cot_1 reasoning profile",
    "tool_name": "reasoning_profile_control",
    "tool_args": {
        "reasoning_type": "external",
        "action": "set_profile",
        "profile": "external_cot_1"
    }
}
~~~

**To discover available profiles:**
- Use `action="get_all"` to see all three reasoning types and their current profiles
- Use `action="get_status"` with a specific `reasoning_type` (internal, interleaved, or external) to see all available profiles for that type
- Each reasoning type has its own independent set of profiles

**Important Notes:**
- Your active profiles are displayed in your system prompt under "Reasoning Profiles"
- Each reasoning type (internal, interleaved, external) is configured independently
- Do NOT say "enable" - use `action="set_profile"` (these are profiles, not features)
- Profile changes take effect immediately on the next message loop
- **Always check your system prompt first** before making tool calls to query your configuration
- Do not hardcode profile names - use `get_status` to discover what profiles are available for each reasoning type
