### philosophy_profile_control:
Manage philosophy profiles that define operational principles, ethical guidelines, and decision-making frameworks.

**YOUR ACTIVE PROFILE is displayed in the "Philosophy Profile" section of your system prompt.**

**Quick Reference:**
- User asks "what philosophy am I using?" → **Check your system prompt first**
- User asks "what philosophies are available?" → Use `action="get_status"`
- User says "switch to research philosophy" → Use `action="set_profile"`, `profile="research"`

**Available Actions:**

**get_status** - View current philosophy profile, available profiles, and active features
~~~json
{
    "thoughts": ["User wants to see available philosophy profiles and current configuration"],
    "headline": "Checking philosophy profile status",
    "tool_name": "philosophy_profile_control",
    "tool_args": {
        "action": "get_status"
    }
}
~~~

**get_profile** - View just the active philosophy profile
~~~json
{
    "thoughts": ["What philosophy profile am I currently using?"],
    "headline": "Checking active philosophy profile",
    "tool_name": "philosophy_profile_control",
    "tool_args": {
        "action": "get_profile"
    }
}
~~~

**set_profile** - Change active philosophy profile
~~~json
{
    "thoughts": ["User wants research philosophy for rigorous, evidence-based analysis"],
    "headline": "Switching to research philosophy profile",
    "tool_name": "philosophy_profile_control",
    "tool_args": {
        "action": "set_profile",
        "profile": "research"
    }
}
~~~

**To discover available profiles:**
Use `action="get_status"` to see all available philosophy profiles with their descriptions and which features each profile enables.

**Important Notes:**
- Your active profile is displayed in your system prompt under "Philosophy Profile"
- Each philosophy profile defines different operational principles, ethical guidelines, and decision frameworks
- Profile changes take effect immediately on the next message loop
- **Always check your system prompt first** before making tool calls to query your configuration
- Do not hardcode profile names - use `get_status` to discover what profiles are available
