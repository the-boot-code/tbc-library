# feature_control

## Problem

Manage individual features and controls (enable/disable options). Provides direct control over optional features and core system controls, independent of security profiles. Requires "feature_control" to be enabled.

**Available Actions:**
**get_feature** - View feature status (all features if no parameter)
**set_feature** - Enable/disable specific feature (requires `feature` and `enabled` parameters)

## Solution

**JSON Example Pattern:**
~~~json
{
    "thoughts": ["User request description"],
    "headline": "Action description",
    "tool_name": "feature_control",
    "tool_args": {
        "action": "action_name",
        "parameter": "value"
    }
}
~~~

**Additional Options:**
Use `action="get_feature"` (without parameter) to see all available features and controls.
- **Features**: Optional enhancements that can be enabled/disabled
- **Controls**: Core system components (disabling may affect functionality)

**Important Notes:**
- Active security profile may override these settings
- Lockdown profile disables this tool
- Values may change without notification - verify current state
