### feature_control:
Manage individual feature options (enable/disable features).
Controls feature settings independent of security profiles.
Requires "feature_control" feature to be enabled.

**Actions:**

**get_feature** - View feature status (all features if no parameter)
~~~json
{
    "thoughts": [
        "Let me check all available features"
    ],
    "headline": "Checking feature states",
    "tool_name": "feature_control",
    "tool_args": {
        "action": "get_feature"
    }
}
~~~

**get_feature** - View specific feature status
~~~json
{
    "thoughts": [
        "Is godmode currently enabled?"
    ],
    "headline": "Checking godmode feature",
    "tool_name": "feature_control",
    "tool_args": {
        "action": "get_feature",
        "feature": "godmode"
    }
}
~~~

**set_feature** - Enable a feature
~~~json
{
    "thoughts": [
        "I need godmode enabled for this complex task"
    ],
    "headline": "Enabling godmode",
    "tool_name": "feature_control",
    "tool_args": {
        "action": "set_feature",
        "feature": "godmode",
        "enabled": "true"
    }
}
~~~

**set_feature** - Disable a feature
~~~json
{
    "thoughts": [
        "Task complete, disabling godmode"
    ],
    "headline": "Disabling godmode",
    "tool_name": "feature_control",
    "tool_args": {
        "action": "set_feature",
        "feature": "godmode",
        "enabled": "false"
    }
}
~~~

**Available features:** godmode, omni, security_control, feature_control
**Note:** Active security profile may override feature settings. Lockdown profile disables this tool.
**No-Caching** These value may change without notifications make no assumptions do not mentally cache refer to [EXTRAS]
