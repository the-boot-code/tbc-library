from python.helpers.tool import Tool, Response
from python.helpers.system_control import SystemControl
from .base_profile_control import BaseProfileControlTool


class LiminalThinkingProfileControlTool(BaseProfileControlTool):
    """
    Tool for managing liminal thinking profiles and features.
    Allows agent to view, switch profiles, and enable/disable features.
    
    FUTURE OPTION 2 NOTES:
    - Consider automated profile discovery from instruction files
    - Template-based response formatting for profile descriptions
    - Dynamic action registration from instruction metadata
    """
    
    # Configuration for base class
    profile_type = "liminal_thinking"
    available_actions = ["get_status", "get_profile", "set_profile", "enable_feature", "disable_feature", "list_features"]
    
    def __init__(self):
        super().__init__()
        # Map actions to handler methods
        self.action_handlers = {
            "get_status": self._handle_get_status,
            "get_profile": self._handle_get_profile,
            "set_profile": self._handle_set_profile,
            "enable_feature": self._handle_enable_feature,
            "disable_feature": self._handle_disable_feature,
            "list_features": self._handle_list_features,
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
        
        features = state.get('features', {})
        if features:
            for feature, config in features.items():
                enabled = config.get('enabled', False)
                status = "ENABLED" if enabled else "disabled"
                lines.append(f"  - {feature}: {status}")
        else:
            lines.append("  - (No features enabled for this profile)")
        
        lines.extend([
            "",
            "Available Profiles:",
            "  - default: Balanced liminal awareness for general tasks",
            "  - deep: Maximum exploration for complex problems",
            "  - transitional: Specialized for change management",
            "  - emergent: Optimized for pattern detection",
            "",
            "Available Features:",
            "  - threshold_awareness: Systematic threshold detection",
            "  - ambiguity_embracement: Productive uncertainty exploration",
            "  - metamorphic_insight: Transformative dissolution",
            "  - paradox_navigation: Paradox as portal to insight",
            "  - emergence_detection: Self-organizing pattern recognition",
            "  - phase_shift_catalyst: Deliberate state transitions",
            "  - void_space_illumination: Wisdom from emptiness",
            "  - bridge_building: Cross-domain connection",
            "  - fluid_state_cognition: Adaptive fluidity"
        ])
        
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
            "Note: The new profile prompt will be loaded on the next message loop."
        ]
        
        # Get new state to show impact
        state = system.get_liminal_thinking_state()
        features = state.get('features', {})
        if features:
            lines.append("")
            lines.append("Profile features:")
            for feature, config in features.items():
                enabled = config.get('enabled', False)
                status = "ENABLED" if enabled else "DISABLED"
                lines.append(f"  - {feature}: {status}")
        
        return Response(
            message="\n".join(lines),
            break_loop=False
        )
    
    async def _handle_enable_feature(self, system: SystemControl, kwargs: dict) -> Response:
        """Enable a specific liminal thinking feature"""
        feature = kwargs.get("feature", "")
        
        if not feature:
            return Response(
                message="Missing 'feature' parameter. Use list_features action to see available features.",
                break_loop=False
            )
        
        # Attempt to enable feature
        result = system.enable_liminal_thinking_feature(feature)
        
        if not result["success"]:
            error = result.get("error", "Unknown error")
            return Response(
                message=f"Failed to enable feature: {error}",
                break_loop=False
            )
        
        lines = [
            f"✓ {result['message']}",
            "",
            f"Profile: {result['profile']}",
            f"Feature: {result['feature']}",
            "",
            "Note: Feature will be active on the next message loop."
        ]
        
        return Response(
            message="\n".join(lines),
            break_loop=False
        )
    
    async def _handle_disable_feature(self, system: SystemControl, kwargs: dict) -> Response:
        """Disable a specific liminal thinking feature"""
        feature = kwargs.get("feature", "")
        
        if not feature:
            return Response(
                message="Missing 'feature' parameter. Use list_features action to see available features.",
                break_loop=False
            )
        
        # Attempt to disable feature
        result = system.disable_liminal_thinking_feature(feature)
        
        if not result["success"]:
            error = result.get("error", "Unknown error")
            return Response(
                message=f"Failed to disable feature: {error}",
                break_loop=False
            )
        
        lines = [
            f"✓ {result['message']}",
            "",
            f"Profile: {result['profile']}",
            f"Feature: {result['feature']}"
        ]
        
        return Response(
            message="\n".join(lines),
            break_loop=False
        )
    
    async def _handle_list_features(self, system: SystemControl, kwargs: dict) -> Response:
        """List all available liminal thinking features"""
        lines = [
            "=== Available Liminal Thinking Features ===",
            "",
            "Core Features:",
            "  - threshold_awareness: Actively scan for and navigate liminal thresholds",
            "  - ambiguity_embracement: Transform uncertainty into insight",
            "  - metamorphic_insight: Generate breakthroughs through dissolution",
            "  - paradox_navigation: Use paradoxes as portals to deeper truth",
            "",
            "Advanced Features:",
            "  - emergence_detection: Detect and leverage self-organizing patterns",
            "  - phase_shift_catalyst: Deliberately shift between cognitive states",
            "  - void_space_illumination: Extract wisdom from cognitive emptiness",
            "  - bridge_building: Connect disparate elements through liminal pathways",
            "  - fluid_state_cognition: Maintain adaptive fluidity across contexts",
            "",
            "Usage:",
            "  - enable_feature: Enable a specific feature in current profile",
            "  - disable_feature: Disable a specific feature in current profile",
            "  - set_profile: Switch to profile with pre-configured feature sets"
        ]
        
        # Show current state
        state = system.get_liminal_thinking_state()
        features = state.get('features', {})
        
        if features:
            lines.extend([
                "",
                f"Currently Active (in '{state['active_profile']}' profile):"
            ])
            for feature, config in features.items():
                if config.get('enabled', False):
                    lines.append(f"  ✓ {feature}")
        
        return Response(
            message="\n".join(lines),
            break_loop=False
        )
    
    # Required base class methods for liminal thinking-specific functionality
    
    def _get_available_profiles(self) -> list[str]:
        """Get available liminal thinking profiles"""
        return self.system.get_available_liminal_thinking_profiles()
