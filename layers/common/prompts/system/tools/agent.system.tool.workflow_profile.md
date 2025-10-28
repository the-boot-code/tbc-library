### workflow_profile:
Manage workflow profiles and view workflow state.

**YOUR ACTIVE PROFILE is shown in the "Workflow Profile" section of your system prompt.**

Use this tool to:
- View detailed information about all available profiles
- Switch between different workflow profiles
- Check configuration details that may have changed

**Actions:**

**get_status** - View full workflow state (profile, features)
~~~json
{
    "thoughts": [
        "I need to check the current workflow configuration"
    ],
    "headline": "Checking workflow status",
    "tool_name": "workflow_control",
    "tool_args": {
        "action": "get_status"
    }
}
~~~

**get_profile** - View active workflow profile
~~~json
{
    "thoughts": [
        "What workflow profile am I currently using?"
    ],
    "headline": "Checking active workflow profile",
    "tool_name": "workflow_control",
    "tool_args": {
        "action": "get_profile"
    }
}
~~~

**set_profile** - Change active workflow profile
~~~json
{
    "thoughts": [
        "I should switch to guided mode for this interactive task"
    ],
    "headline": "Switching to guided workflow",
    "tool_name": "workflow_control",
    "tool_args": {
        "action": "set_profile",
        "profile": "guided"
    }
}
~~~

**To discover available profiles:**
Use `action="get_status"` to see all available workflow profiles and their details.

**Important Notes:**
- Your active profile is displayed in your system prompt under "Workflow Profile"
- Each workflow profile loads different behavioral instructions and interaction patterns
- Profile changes take effect on next message loop
- **Always check your system prompt first** before making tool calls to query your configuration
- To see all available profiles and what they do, use the `get_status` action
