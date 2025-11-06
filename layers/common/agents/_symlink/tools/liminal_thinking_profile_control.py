from python.helpers.tool import Tool, Response
from python.helpers.system_control import SystemControl


class LiminalThinkingProfileControlTool(Tool):
    """
    Tool for managing liminal thinking profiles.
    Allows agent to view and switch between liminal thinking profiles.
    """
    
    async def execute(self, action: str = "", **kwargs):
        """
        Execute liminal thinking control action.
        
        Actions:
        - get_status: View full liminal thinking state
        - get_profile: View active liminal thinking profile
        - set_profile: Change active liminal thinking profile (requires: profile="name")
        - enable_feature: Enable a liminal thinking feature (requires: feature="name")
        - disable_feature: Disable a liminal thinking feature (requires: feature="name")
        """
        
        system = SystemControl()
        
        # Check if tool itself is enabled
        if not system.is_feature_enabled("liminal_thinking_profile_control"):
            return Response(
                message="Liminal thinking control tool is disabled by current security profile. Admin override required.",
                break_loop=False
            )
        
        # Route to action handlers
        if action == "get_status":
            return await self._get_status(system)
        elif action == "get_profile":
            return await self._get_profile(system)
        elif action == "set_profile":
            return await self._set_profile(system, kwargs)
        elif action == "enable_feature":
            return await self._enable_feature(system, kwargs)
        elif action == "disable_feature":
            return await self._disable_feature(system, kwargs)
        else:
            return Response(
                message=f"Unknown action '{action}'. Available: get_status, get_profile, set_profile, enable_feature, disable_feature",
                break_loop=False
            )
    
    async def _get_status(self, system: SystemControl) -> Response:
        """Get current liminal thinking state"""
        state = system.get_state("liminal_thinking")

        # Format response
        lines = [
            "=== Liminal Thinking Profile Status ===",
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
        lines.append("  - default: Standard liminal thinking approach")
        lines.append("  - (additional profiles loaded from external configuration)")

        return Response(
            message="\n".join(lines),
            break_loop=False
        )

    async def _get_profile(self, system: SystemControl) -> Response:
        """Get current active liminal thinking profile"""
        profile_name = system.get_active_profile("liminal_thinking")
        available = system.get_available_profiles("liminal_thinking")

        lines = [
            f"Active Liminal Thinking Profile: {profile_name}",
            f"Available Profiles: {', '.join(available)}"
        ]

        return Response(
            message="\n".join(lines),
            break_loop=False
        )

    async def _set_profile(self, system: SystemControl, kwargs: dict) -> Response:
        """Change active liminal thinking profile"""
        profile = kwargs.get("profile", "")

        if not profile:
            available = system.get_available_profiles("liminal_thinking")
            return Response(
                message=f"Missing 'profile' parameter. Available profiles: {', '.join(available)}",
                break_loop=False
            )

        # Attempt to change profile
        result = system.set_active_profile("liminal_thinking", profile)

        if not result["success"]:
            error = result.get("error", "Unknown error")
            available = result.get("available_profiles", [])
            msg = f"Failed to change liminal thinking profile: {error}"
            if available:
                msg += f"\nAvailable profiles: {', '.join(available)}"
            return Response(message=msg, break_loop=False)

        # Success - format detailed response
        lines = [
            f"✓ Liminal thinking profile changed: {result['previous_profile']} → {result['new_profile']}",
            "",
            "Liminal thinking configuration updated. Changes take effect immediately.",
            "",
            "Note: The new liminal thinking profile prompt will be loaded on the next message loop."
        ]

        # Get new state to show impact
        state = system.get_state("liminal_thinking")
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

    async def _enable_feature(self, system: SystemControl, kwargs: dict) -> Response:
        """Enable a liminal thinking feature"""
        feature = kwargs.get("feature", "")

        if not feature:
            state = system.get_state("liminal_thinking")
            available_features = list(state.get('features', {}).keys())
            return Response(
                message=f"Missing 'feature' parameter. Available features: {', '.join(available_features)}",
                break_loop=False
            )

        result = system.enable_feature("liminal_thinking", feature)

        if not result["success"]:
            error = result.get("error", "Unknown error")
            return Response(
                message=f"Failed to enable feature '{feature}': {error}",
                break_loop=False
            )

        return Response(
            message=f"✓ Feature '{feature}' enabled successfully",
            break_loop=False
        )

    async def _disable_feature(self, system: SystemControl, kwargs: dict) -> Response:
        """Disable a liminal thinking feature"""
        feature = kwargs.get("feature", "")

        if not feature:
            state = system.get_state("liminal_thinking")
            available_features = list(state.get('features', {}).keys())
            return Response(
                message=f"Missing 'feature' parameter. Available features: {', '.join(available_features)}",
                break_loop=False
            )

        result = system.disable_feature("liminal_thinking", feature)

        if not result["success"]:
            error = result.get("error", "Unknown error")
            return Response(
                message=f"Failed to disable feature '{feature}': {error}",
                break_loop=False
            )

        return Response(
            message=f"✓ Feature '{feature}' disabled successfully",
            break_loop=False
        )
