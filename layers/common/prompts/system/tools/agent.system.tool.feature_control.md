### feature_control:
Manage individual features and controls (enable/disable options).
Provides direct control over optional features and core system controls, independent of security profiles.
Requires "feature_control" to be enabled.

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

**Available Options:**
- **Features** (optional enhancements): `godmode`, `plinian_cognitive_matrix`, `model_overview`
- **Controls** (core system): `security_control`, `feature_control`, `workflow_control`, `reasoning_control`

**Important Notes:**
- Active security profile may override these settings
- Lockdown profile disables this tool
- Features are optional enhancements; Controls are core system components
- Disabling controls may affect system functionality
- Values may change without notification - always verify current state with this tool
