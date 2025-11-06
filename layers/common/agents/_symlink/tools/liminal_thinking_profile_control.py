from python.helpers.tool import Tool, Response
from python.helpers.system_control import SystemControl
from .base_profile_control import BaseProfileControlTool


class LiminalThinkingProfileControlTool(BaseProfileControlTool):
    """
    Tool for managing liminal thinking profiles.
    Allows agent to view and switch between liminal thinking profiles.

    FUTURE OPTION 2 NOTES:
    - Consider automated profile discovery from instruction files
    - Template-based response formatting for profile descriptions
    - Dynamic action registration from instruction metadata
    """

    # Configuration for base class
    profile_type = "liminal_thinking"
    available_actions = ["get_status", "get_profile", "set_profile", "enable_feature", "disable_feature"]

    def __init__(self):
        super().__init__()
        # Map actions to handler methods
        self.action_handlers = {
            "get_status": self._handle_get_status,
            "get_profile": self._handle_get_profile,
            "set_profile": self._handle_set_profile,
            "enable_feature": self._handle_enable_feature,
            "disable_feature": self._handle_disable_feature,
        }

    async def _handle_get_status(self, system: SystemControl, kwargs: dict) -> Response:
        """Get current liminal thinking state"""
        state = system.get_liminal_thinking_state()

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

    async def _handle_get_profile(self, system: SystemControl, kwargs: dict) -> Response:
        """Get current active liminal thinking profile"""
        profile_name = system.get_active_liminal_thinking_profile()
        available = system.get_available_liminal_thinking_profiles()

        lines = [
            f"Active Liminal Thinking Profile: {profile_name}",
            f"Available Profiles: {', '.join(available)}"
        ]

        return Response(
            message="\n".join(lines),
            break_loop=False
        )

    async def _handle_set_profile(self, system: SystemControl, kwargs: dict) -> Response:
        """Change active liminal thinking profile"""
        profile = kwargs.get("profile", "")

        if not profile:
            available = system.get_available_liminal_thinking_profiles()
            return Response(
                message=f"Missing 'profile' parameter. Available profiles: {', '.join(available)}",
                break_loop=False
            )

        # Attempt to change profile
        result = system.set_active_liminal_thinking_profile(profile)

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
        state = system.get_liminal_thinking_state()
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

    async def _handle_enable_feature(self, system: SystemControl, kwargs: dict) -> Response:
        """Enable a liminal thinking feature"""
        feature = kwargs.get("feature", "")

        if not feature:
            state = system.get_liminal_thinking_state()
            available_features = list(state.get('features', {}).keys())
            return Response(
                message=f"Missing 'feature' parameter. Available features: {', '.join(available_features)}",
                break_loop=False
            )

        result = system.enable_liminal_thinking_feature(feature)

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

    async def _handle_disable_feature(self, system: SystemControl, kwargs: dict) -> Response:
        """Disable a liminal thinking feature"""
        feature = kwargs.get("feature", "")

        if not feature:
            state = system.get_liminal_thinking_state()
            available_features = list(state.get('features', {}).keys())
            return Response(
                message=f"Missing 'feature' parameter. Available features: {', '.join(available_features)}",
                break_loop=False
            )

        result = system.disable_liminal_thinking_feature(feature)

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

    # Required base class methods for liminal thinking-specific functionality

    def _get_available_profiles(self) -> list[str]:
        """Get available liminal thinking profiles"""
        return self.system.get_available_liminal_thinking_profiles()
