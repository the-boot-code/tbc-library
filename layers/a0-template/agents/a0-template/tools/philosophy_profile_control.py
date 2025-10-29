from python.helpers.tool import Tool, Response
from python.helpers.system_control import SystemControl


class PhilosophyProfileControlTool(Tool):
    """
    Tool for managing philosophy profiles.
    Allows agent to view and switch between philosophy profiles.
    """
    
    async def execute(self, action: str = "", **kwargs):
        """
        Execute philosophy control action.
        
        Actions:
        - get_status: View full philosophy state
        - get_profile: View active philosophy profile
        - set_profile: Change active philosophy profile (requires: profile="name")
        """
        
        system = SystemControl()
        
        # Check if tool itself is enabled
        if not system.is_feature_enabled("philosophy_profile_control"):
            return Response(
                message="Philosophy control tool is disabled by current security profile. Admin override required.",
                break_loop=False
            )
        
        # Route to action handlers
        if action == "get_status":
            return await self._get_status(system)
        elif action == "get_profile":
            return await self._get_profile(system)
        elif action == "set_profile":
            return await self._set_profile(system, kwargs)
        else:
            return Response(
                message=f"Unknown action '{action}'. Available: get_status, get_profile, set_profile",
                break_loop=False
            )
    
    async def _get_status(self, system: SystemControl) -> Response:
        """Get current philosophy state"""
        state = system.get_philosophy_state()
        
        # Format response
        lines = [
            "=== Philosophy Profile Status ===",
            f"Active Profile: {state['active_profile']}",
            f"Available Profiles: {', '.join(state['available_profiles'])}",
            "",
            "Profile Features:"
        ]
        
        for feature, config in state.get('features', {}).items():
            enabled = config.get('enabled', False)
            status = "ENABLED" if enabled else "disabled"
            lines.append(f"  - {feature}: {status}")
        
        if not state.get('features'):
            lines.append("  - (No features defined for this profile)")
        
        lines.append("")
        lines.append("Available Profiles:")
        lines.append("  - default: Balanced, general-purpose principles")
        lines.append("  - research: Academic rigor, evidence-based, citation standards")
        lines.append("  - creative: Innovation, divergent thinking, exploration")
        lines.append("  - analytical: Systematic decomposition, logical rigor")
        lines.append("  - collaborative: Consensus-building, stakeholder consideration")
        lines.append("  - efficiency: Speed optimization, satisficing, resource conservation")
        lines.append("  - safety: Risk mitigation, harm prevention, conservative defaults")
        
        return Response(
            message="\n".join(lines),
            break_loop=False
        )
    
    async def _get_profile(self, system: SystemControl) -> Response:
        """Get current active philosophy profile"""
        profile_name = system.get_active_philosophy_profile()
        available = system.get_available_philosophy_profiles()
        
        lines = [
            f"Active Philosophy Profile: {profile_name}",
            f"Available Profiles: {', '.join(available)}"
        ]
        
        return Response(
            message="\n".join(lines),
            break_loop=False
        )
    
    async def _set_profile(self, system: SystemControl, kwargs: dict) -> Response:
        """Change active philosophy profile"""
        profile = kwargs.get("profile", "")
        
        if not profile:
            available = system.get_available_philosophy_profiles()
            return Response(
                message=f"Missing 'profile' parameter. Available profiles: {', '.join(available)}",
                break_loop=False
            )
        
        # Attempt to change profile
        result = system.set_active_philosophy_profile(profile)
        
        if not result["success"]:
            error = result.get("error", "Unknown error")
            available = result.get("available_profiles", [])
            msg = f"Failed to change philosophy profile: {error}"
            if available:
                msg += f"\nAvailable profiles: {', '.join(available)}"
            return Response(message=msg, break_loop=False)
        
        # Success - format detailed response
        lines = [
            f"✓ Philosophy profile changed: {result['previous_profile']} → {result['new_profile']}",
            "",
            "Philosophy configuration updated. Changes take effect immediately.",
            "",
            "Note: The new philosophy profile prompt will be loaded on the next message loop."
        ]
        
        # Get new state to show impact
        state = system.get_philosophy_state()
        if state.get('features'):
            lines.append("")
            lines.append("Profile features:")
            for feature, config in state['features'].items():
                enabled = config.get('enabled', False)
                status = "ENABLED" if enabled else "DISABLED"
                lines.append(f"  - {feature}: {status}")
        
        return Response(
            message="\n".join(lines),
            break_loop=False
        )
