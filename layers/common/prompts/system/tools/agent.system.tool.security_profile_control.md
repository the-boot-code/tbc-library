### security_profile_control:
Manage security profiles that control feature access and operational restrictions.

**YOUR ACTIVE PROFILE is displayed in the "Security Profile" section of your system prompt.**

**Quick Reference:**
- User asks "what security profile am I using?" → **Check your system prompt first**
- User asks "what security profiles are available?" → Use `action="get_status"`
- User says "switch to restricted profile" → Use `action="set_profile"`, `profile="restricted"`

**Available Actions:**

**get_status** - View current security profile, available profiles, admin override status, and feature restrictions
~~~json
{
    "thoughts": ["User wants to see available security profiles and current restrictions"],
    "headline": "Checking security profile status",
    "tool_name": "security_profile_control",
    "tool_args": {
        "action": "get_status"
    }
}
~~~

**get_profile** - View just the active security profile
~~~json
{
    "thoughts": ["What security profile am I currently using?"],
    "headline": "Checking active security profile",
    "tool_name": "security_profile_control",
    "tool_args": {
        "action": "get_profile"
    }
}
~~~

**set_profile** - Change active security profile
~~~json
{
    "thoughts": ["User wants restricted profile for enhanced security"],
    "headline": "Switching to restricted security profile",
    "tool_name": "security_profile_control",
    "tool_args": {
        "action": "set_profile",
        "profile": "restricted"
    }
}
~~~

**To discover available profiles:**
Use `action="get_status"` to see all available security profiles with their feature restrictions and current admin override status.

**Important Notes:**
- Your active profile is displayed in your system prompt under "Security Profile"
- Each security profile controls which features and tools are available
- Lockdown profile may disable this tool - admin override required to escape lockdown
- Profile changes take effect immediately on the next message loop
- Security profile changes may occur without notification - verify current state if behavior seems restricted
- **Always check your system prompt first** before making tool calls to query your configuration
- Do not hardcode profile names - use `get_status` to discover what profiles are available
