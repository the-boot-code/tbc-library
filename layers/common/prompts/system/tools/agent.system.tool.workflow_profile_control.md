### workflow_profile_control:
Manage workflow profiles that define behavioral instructions and interaction patterns.

**YOUR ACTIVE PROFILE is displayed in the "Workflow Profile" section of your system prompt.**

**Quick Reference:**
- User asks "what workflow am I using?" → **Check your system prompt first**
- User asks "what workflows are available?" → Use `action="get_status"`
- User says "switch to guided workflow" → Use `action="set_profile"`, `profile="guided"`

**Available Actions:**

**get_status** - View current workflow profile, available profiles, and active features
~~~json
{
    "thoughts": ["User wants to see available workflow profiles and current configuration"],
    "headline": "Checking workflow profile status",
    "tool_name": "workflow_profile_control",
    "tool_args": {
        "action": "get_status"
    }
}
~~~

**get_profile** - View just the active workflow profile
~~~json
{
    "thoughts": ["What workflow profile am I currently using?"],
    "headline": "Checking active workflow profile",
    "tool_name": "workflow_profile_control",
    "tool_args": {
        "action": "get_profile"
    }
}
~~~

**set_profile** - Change active workflow profile
~~~json
{
    "thoughts": ["User wants guided workflow for this interactive task"],
    "headline": "Switching to guided workflow profile",
    "tool_name": "workflow_profile_control",
    "tool_args": {
        "action": "set_profile",
        "profile": "guided"
    }
}
~~~

**To discover available profiles:**
Use `action="get_status"` to see all available workflow profiles with their descriptions and which features each profile enables.

**Important Notes:**
- Your active profile is displayed in your system prompt under "Workflow Profile"
- Each workflow profile loads different behavioral instructions and interaction patterns
- Profile changes take effect immediately on the next message loop
- **Always check your system prompt first** before making tool calls to query your configuration
- Do not hardcode profile names - use `get_status` to discover what profiles are available
