from python.helpers.tool import Tool, Response
from control_layer.python.helpers.system_control import SystemControl


tool_key = "prompt_include_control"
tool_display_name = "Prompt include control tool"


class PromptIncludeControlTool(Tool):
    async def execute(self, action: str = "", **kwargs):
        system = SystemControl()

        # Check if tool itself is enabled via SystemControl
        if not system.is_prompt_include_enabled(tool_key):
            return Response(
                message=f"{tool_display_name} is disabled by current security profile. Admin override required.",
                break_loop=False,
            )

        if action == "get_all":
            return await self._get_all(system)
        elif action == "get_entry":
            return await self._get_entry(system, kwargs)
        elif action == "set_entry":
            return await self._set_entry(system, kwargs)
        else:
            return Response(
                message=f"Unknown action '{action}'. Available: get_all, get_entry, set_entry",
                break_loop=False,
            )

    async def _get_all(self, system: SystemControl) -> Response:
        """List all prompt-includes and System Control tools with effective status and source."""
        available = system.get_available_prompt_includes_and_controls()
        state = system.get_security_state()

        lines = [
            "=== Prompt Include Status (SystemControl) ===",
            f"Total prompt-includes: {len(available)}",
            "",
        ]

        for name in sorted(available):
            is_enabled = system.is_prompt_include_enabled(name)
            entry_state = state["entries"].get(name, {})
            source = entry_state.get("source", "not_found")
            status = "ENABLED" if is_enabled else "disabled"
            lines.append(f"  - {name}: {status} (via {source})")

        message = "\n".join(lines)
        extra_lines = [
            "",
            "Notes:",
            "  - Status reflects the effective state after any security profile overrides.",
            "  - 'via <source>' shows where the enable/disable decision is coming from.",
            "  - Use action='set_entry' with entry=\"name\" and enabled=true/false to change a specific prompt-include.",
        ]
        if extra_lines:
            if message:
                message = "\n".join([message, *extra_lines])
            else:
                message = "\n".join(extra_lines)

        return Response(message=message, break_loop=False)

    async def _get_entry(self, system: SystemControl, kwargs: dict) -> Response:
        entry = kwargs.get("entry", "")

        if not entry:
            # Show all prompt-includes and System Control tools
            state = system.get_security_state()
            lines = ["System prompt-includes/System Control tools:"]
            for name, info in state["entries"].items():
                enabled = info.get("enabled", False)
                status = "ENABLED" if enabled else "disabled"
                source = info.get("source", "not_found")
                lines.append(f"  - {name}: {status} (via {source})")
            return Response(message="\n".join(lines), break_loop=False)

        # Show specific prompt-include or System Control tool
        available = system.get_available_prompt_includes_and_controls()
        if entry not in available:
            return Response(
                message=f"Entry '{entry}' (prompt-include/System Control tool) not found. Available: {', '.join(available)}",
                break_loop=False,
            )

        is_enabled = system.is_prompt_include_enabled(entry)
        config = system.get_prompt_include_config(entry)

        state = system.get_security_state()
        source = state["entries"].get(entry, {}).get("source", "not_found")

        lines = [
            f"Entry: {entry}",
            f"Status: {'ENABLED' if is_enabled else 'disabled'}",
            f"Source: {source}",
            f"Config: {config}",
        ]

        return Response(message="\n".join(lines), break_loop=False)

    async def _set_entry(self, system: SystemControl, kwargs: dict) -> Response:
        entry = kwargs.get("entry", "")
        enabled_str = kwargs.get("enabled", "")

        if not entry:
            available = system.get_available_prompt_includes_and_controls()
            return Response(
                message=f"Missing 'entry' parameter. Available prompt-includes/system control tools: {', '.join(available)}",
                break_loop=False,
            )

        if enabled_str == "":
            return Response(
                message="Missing 'enabled' parameter. Use: enabled=true or enabled=false",
                break_loop=False,
            )

        # Parse boolean
        if isinstance(enabled_str, bool):
            enabled = enabled_str
        else:
            value = str(enabled_str).lower()
            if value in ["true", "1", "yes"]:
                enabled = True
            elif value in ["false", "0", "no"]:
                enabled = False
            else:
                return Response(
                    message=f"Invalid 'enabled' value: {enabled_str}. Use: true or false",
                    break_loop=False,
                )

        result = system.set_prompt_include_option(entry, enabled)

        if not result.get("success", False):
            error = result.get("error", "Unknown error")
            msg = f"Failed to change entry: {error}"
            return Response(message=msg, break_loop=False)

        status = "enabled" if result["new_value"] else "disabled"
        lines = [
            f"✓ Entry '{entry}' {status}",
            "",
        ]

        if "note" in result:
            lines.append(f"Note: {result['note']}")
            lines.append("")

        is_actually_enabled = system.is_prompt_include_enabled(entry)
        if is_actually_enabled != enabled:
            lines.append(
                f"⚠ Entry is currently {'ENABLED' if is_actually_enabled else 'DISABLED'} due to active security profile override",
            )
        else:
            lines.append(
                f"Entry is now {'ENABLED' if is_actually_enabled else 'DISABLED'}",
            )

        return Response(
            message="\n".join(lines),
            break_loop=False,
        )
