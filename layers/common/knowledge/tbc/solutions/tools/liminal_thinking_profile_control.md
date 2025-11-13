# Liminal Thinking Profile Control

## Problem

How to use tool 'liminal_thinking_profile_control'

Manage liminal thinking profiles for navigating transitional states, thresholds, and uncertainty. Control cognitive enhancement features for deliberate engagement with liminal spaces.

## Solution

**ACTIVE PROFILE**: Displayed in "Liminal Thinking Profile" section of system prompt.

**Quick Reference:**
- "what profile am I using?" → **Check system prompt first**
- "what profiles available?" → `action="get_status"`
- "switch to deep" → `action="set_profile"`, `profile="deep"`
- "enable threshold awareness" → `action="enable_feature"`, `feature="threshold_awareness"`

**Available Actions:**

**get_status** - View current profile, available profiles, and active features
**get_profile** - View just the active profile
**set_profile** - Change active profile (requires `profile` parameter)
**enable_feature** - Enable specific feature (requires `feature` parameter)
**disable_feature** - Disable specific feature (requires `feature` parameter)

**JSON Example Pattern:**
~~~json
{
    "thoughts": ["User request description"],
    "headline": "Action description",
    "tool_name": "liminal_thinking_profile_control",
    "tool_args": {
        "action": "action_name",
        "parameter": "value"
    }
}
~~~

**list_features** - View all available features with descriptions

**Profiles & Features:**
Use `action="get_status"` to discover available profiles and features. Key profiles: default (clean), balanced (general), deep (complex), transitional (change), emergent (patterns). Features include threshold_awareness, ambiguity_embracement, metamorphic_insight, paradox_navigation, emergence_detection, phase_shift_catalyst, void_space_illumination, bridge_building, fluid_state_cognition.

**Important Notes:**
- Active profile displayed in system prompt
- Changes take effect immediately on next message loop
- **Check system prompt first** before querying configuration
- Use `get_status` to discover available options (don't hardcode)
- Features can be enabled/disabled independently
- Deep profile has higher computational cost
