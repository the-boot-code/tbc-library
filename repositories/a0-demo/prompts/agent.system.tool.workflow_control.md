### workflow_control:
Manage workflow profiles and view workflow state.
Controls which workflow profile is active (default, guided).
Requires "workflow_control" feature to be enabled.

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

**Available profiles:** default, guided
**Note:** Workflow profiles load different behavioral instructions. Changes take effect on next message loop.
**No-Caching** These values may change without notifications make no assumptions do not mentally cache refer to [EXTRAS]
