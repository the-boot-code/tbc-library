from python.helpers.tool import Tool, Response
from control_layer.python.helpers.system_control import SystemControl


profile_module_name = "security"
profile_module_control_key = "security_profile_control"
profile_module_display_name = "Security Profile"


class SecurityProfileControlTool(Tool):
    """
    Tool for managing SystemControl security profiles.
    Allows agent to view and switch between security profiles and inspect their prompt includes.
    """
    
    async def execute(self, action: str = "", **kwargs):
        """
        Execute profile control action.
        
        Actions:
        - get_state: View full profile state
        - get_profile: View active profile
        - set_profile: Change active profile (requires: profile="name")
        """
        
        system = SystemControl()
        
        # Check if tool itself is enabled
        if not system.is_control_enabled(profile_module_control_key):
            return Response(
                message=f"{profile_module_display_name} control tool is disabled by current security profile. Admin override required.",
                break_loop=False
            )
        
        # Route to action handlers
        if action == "get_state":
            return await self._get_status(system)
        elif action == "get_profile":
            return await self._get_profile(system)
        elif action == "set_profile":
            return await self._set_profile(system, kwargs)
        else:
            return Response(
                message=f"Unknown action '{action}'. Available: get_state, get_profile, set_profile",
                break_loop=False
            )
    
    async def _get_status(self, system: SystemControl) -> Response:
        """Get current security state (profile and prompt-includes/system control tools)"""
        state = system.get_security_state()
        
        # Format response
        lines = [
            f"=== {profile_module_display_name} Status (SystemControl) ===",
            f"Active {profile_module_display_name}: {state['active_profile']}",
            f"Available {profile_module_display_name}s: {', '.join(state['available_profiles'])}",
            f"Admin Override: {'ACTIVE' if state['admin_override'] else 'inactive'}",
            "",
            "System prompt includes and controls:"
        ]
        
        for name, info in state['entries'].items():
            status = "ENABLED" if info['enabled'] else "disabled"
            source = info['source']
            lines.append(f"  - {name}: {status} (via {source})")
        
        message = "\n".join(lines)
        extra_lines = [
            "",
            "Notes:",
            "  - Status shows the active security profile and all available profiles.",
            "  - Prompt-includes and control tools may be overridden by this profile or admin override.",
            "  - 'via <source>' on each entry indicates where its enable/disable decision comes from.",
        ]
        if extra_lines:
            if message:
                message = "\n".join([message, *extra_lines])
            else:
                message = "\n".join(extra_lines)

        return Response(
            message=message,
            break_loop=False
        )
    
    async def _get_profile(self, system: SystemControl) -> Response:
        """Get current active profile"""
        profile_name = system.get_active_profile(profile_module_name)
        choices = system.get_profile_choices(profile_module_name)
        available = choices.get("available_profiles", [])
        
        lines = [
            f"Active {profile_module_display_name}: {profile_name}",
            f"Available Profiles: {', '.join(available)}",
        ]
        
        return Response(
            message="\n".join(lines),
            break_loop=False
        )
    
    async def _set_profile(self, system: SystemControl, kwargs: dict) -> Response:
        """Change active profile"""
        profile = kwargs.get("profile", "")
        
        if not profile:
            choices = system.get_profile_choices(profile_module_name)
            available = choices.get("available_profiles", [])
            return Response(
                message=f"Missing 'profile' parameter. Available profiles: {', '.join(available)}",
                break_loop=False
            )
        
        # Attempt to change profile
        result = system.set_active_profile(profile_module_name, profile)
        
        if not result.get("success", False):
            error = result.get("error", "Unknown error")
            available = result.get("available_profiles", [])
            msg = f"Failed to change {profile_module_display_name.lower()}: {error}"
            if available:
                msg += f"\nAvailable profiles: {', '.join(available)}"
            return Response(message=msg, break_loop=False)
        
        # Success - format detailed response, handling both changed and no-op cases
        previous_profile = result.get("previous_profile")
        new_profile = result.get("new_profile")

        if previous_profile is not None and new_profile is not None:
            # Profile actually changed
            lines = [
                f"✓ {profile_module_display_name} changed: {previous_profile} → {new_profile}",
                "",
                "Security configuration updated. Changes take effect immediately.",
            ]
        else:
            # No-op success (e.g. already on this profile)
            active = result.get("profile") or system.get_active_profile(profile_module_name)
            message = result.get(
                "message",
                f"Already on {profile_module_display_name.lower()} '{active}'",
            )
            lines = [
                message,
                "",
                f"Active {profile_module_display_name}: {active}",
            ]
        
        # Get new state to show impact
        state = system.get_security_state()
        lines.append("")
        lines.append("Current prompt-includes/system control tools:")
        for name, info in state['entries'].items():
            status = "ENABLED" if info['enabled'] else "DISABLED"
            lines.append(f"  - {name}: {status}")
        
        return Response(
            message="\n".join(lines),
            break_loop=False
        )
    
