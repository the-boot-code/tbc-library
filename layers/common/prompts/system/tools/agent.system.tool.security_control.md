### security_control:
Manage security profiles and view security state.
Controls which security profile is active (open, restricted, lockdown).
Requires "security_control" feature to be enabled.

**Actions:**

**get_status** - View full security state (profile, admin override, all features)
~~~json
{
    "thoughts": [
        "I need to check the current security configuration"
    ],
    "headline": "Checking security status",
    "tool_name": "security_control",
    "tool_args": {
        "action": "get_status"
    }
}
~~~

**get_profile** - View active security profile
~~~json
{
    "thoughts": [
        "What security profile am I currently using?"
    ],
    "headline": "Checking active profile",
    "tool_name": "security_control",
    "tool_args": {
        "action": "get_profile"
    }
}
~~~

**set_profile** - Change active security profile
~~~json
{
    "thoughts": [
        "I need to switch to restricted profile for this task"
    ],
    "headline": "Switching to restricted profile",
    "tool_name": "security_control",
    "tool_args": {
        "action": "set_profile",
        "profile": "restricted"
    }
}
~~~

**Available profiles:** open, restricted, lockdown

**Important Notes:**
- Lockdown profile disables this tool
- Admin override required to escape lockdown
- Profile changes may occur without notification - always verify current state with this tool
