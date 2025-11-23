### security_profile_control
Manage SystemControl security profiles that govern prompt-includes and operational restrictions.

**ACTIVE PROFILE**: Displayed in the "Security Profile" section of the system prompt.

**Quick reference:**
- "what security profile am I using?" → **Check system prompt first**
- "what security profiles available?" → `action="get_state"`
- "switch to restricted" → `action="set_profile"`, `profile="restricted"`

**Available actions:**
- **get_state** – View full security state: active profile, available profiles, admin override,
  and effective prompt-include/control restrictions.
- **get_profile** – View just the active security profile and available profiles.
- **set_profile** – Change active security profile (requires `profile` parameter).

**JSON example pattern:**
~~~json
{
  "thoughts": ["User request description"],
  "headline": "Adjust security profile",
  "tool_name": "security_profile_control",
  "tool_args": {
    "action": "set_profile",
    "profile": "restricted"
  }
}
~~~

**Important notes:**
- Active profile is always displayed in the system prompt.
- Each security profile controls which prompt-includes and tools are available.
- Lockdown profile may disable this tool (admin override required).
- Changes take effect on the next message loop.
- Security configuration may change without separate notification; use `get_state` to inspect
  current configuration.
