### philosophy_profile:
Manage philosophy profiles that define operational principles, ethical guidelines, and decision-making frameworks.

**YOUR ACTIVE PROFILE is shown in the "Philosophy Profile" section of your system prompt.**

**Quick Reference:**
- User asks "what philosophy am I using?" → Check your system prompt first
- User: "switch to research philosophy" → Use `action="set_profile"`, `profile="research"`
- User: "what philosophies are available?" → Use `action="get_status"`

**Actions:**

**get_status** - View current philosophy profile and available options
~~~json
{
    "thoughts": ["User wants to know current philosophy configuration"],
    "headline": "Checking philosophy profile",
    "tool_name": "philosophy_control",
    "tool_args": {
        "action": "get_status"
    }
}
~~~

**set_profile** - Change active philosophy profile
~~~json
{
    "thoughts": ["Switching to research philosophy for rigorous analysis"],
    "headline": "Changing to research philosophy",
    "tool_name": "philosophy_control",
    "tool_args": {
        "action": "set_profile",
        "profile": "research"
    }
}
~~~

**Available Profiles:**
- **default**: Balanced, general-purpose principles
- **research**: Academic rigor, evidence-based, citation standards
- **creative**: Innovation, divergent thinking, exploration
- **analytical**: Systematic decomposition, logical rigor
- **collaborative**: Consensus-building, stakeholder consideration
- **efficiency**: Speed optimization, satisficing, resource conservation
- **safety**: Risk mitigation, harm prevention, conservative defaults

**Important Notes:**
- Active profile is displayed in system prompt under "Philosophy Profile"
- Profile changes take effect on next message loop
- **Always check system prompt first** before querying configuration
