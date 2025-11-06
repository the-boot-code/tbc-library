### security_profile_control:
Manage security profiles controlling feature access and operational restrictions.

**ACTIVE PROFILE**: Displayed in "Security Profile" section of system prompt.

**Quick Reference:**
- "what security profile am I using?" → **Check system prompt first**
- "what security profiles available?" → `action="get_status"`
- "switch to restricted" → `action="set_profile"`, `profile="restricted"`

**Available Actions:**
**get_status** - View current profile, available profiles, admin override status, and feature restrictions
**get_profile** - View just the active security profile
**set_profile** - Change active security profile (requires `profile` parameter)

**JSON Example Pattern:**
~~~json
{
    "thoughts": ["User request description"],
    "headline": "Action description",
    "tool_name": "security_profile_control",
    "tool_args": {
        "action": "action_name",
        "parameter": "value"
    }
}
~~~

**Important Notes:**
- Active profile displayed in system prompt
- Each security profile controls available features and tools
- Lockdown profile may disable this tool (admin override required)
- Changes take effect immediately on next message loop
- Security changes may occur without notification
- **Check system prompt first** before querying configuration
- Use `get_status` to discover available profiles
