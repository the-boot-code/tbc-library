### prompt_include_control

Primary tool for toggling optional SystemControl prompt-includes and System Control tools.

Writes configuration to the `prompt_includes` and `system_control_tools` sections in
`system_control.json`. The **effective** enabled/disabled state may still be overridden by the
active security profile (and admin override).

Available actions: `get_all`, `get_entry`, `set_entry`.

Reference solution `prompt_include_control` for detailed tool usage instructions and examples.
