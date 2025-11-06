from python.helpers.tool import Tool, Response
from python.helpers.system_control import SystemControl
from .base_profile_control import BaseProfileControlTool


class SecurityProfileControlTool(BaseProfileControlTool):
    """
    Tool for managing security profiles.
    Allows agent to view and switch between security profiles.
    
    FUTURE OPTION 2 NOTES:
    - Consider automated profile discovery from instruction files
    - Template-based response formatting for profile descriptions
    - Dynamic action registration from instruction metadata
    """
    
    # Configuration for base class
    profile_type = "security"
    available_actions = ["get_status", "get_profile", "set_profile"]
    
    def __init__(self):
        super().__init__()
        # Map actions to handler methods
        self.action_handlers = {
            "get_status": self._handle_get_status,
            "get_profile": self._handle_get_profile,
            "set_profile": self._handle_set_profile,
        }
    
    async def _handle_get_status(self, security: SystemControl, kwargs: dict) -> Response:
        """Get current security state"""
        state = security.get_security_state()
        
        # Format response
        lines = [
            "=== Security Status ===",
            f"Active Profile: {state['active_profile']}",
            f"Available Profiles: {', '.join(state['available_profiles'])}",
            f"Admin Override: {'ACTIVE' if state['admin_override'] else 'inactive'}",
            "",
            "Features:"
        ]
        
        for feature, info in state['features'].items():
            status = "ENABLED" if info['enabled'] else "disabled"
            source = info['source']
            lines.append(f"  - {feature}: {status} (via {source})")
        
        return Response(
            message="\n".join(lines),
            break_loop=False
        )
    
    async def _handle_get_profile(self, security: SystemControl, kwargs: dict) -> Response:
        """Get current active profile"""
        profile_name = security.get_active_profile()
        available = security.get_available_profiles()
        
        lines = [
            f"Active Profile: {profile_name}",
            f"Available Profiles: {', '.join(available)}"
        ]
        
        return Response(
            message="\n".join(lines),
            break_loop=False
        )
    
    async def _handle_set_profile(self, security: SystemControl, kwargs: dict) -> Response:
        """Change active security profile"""
        profile = kwargs.get("profile", "")
        
        if not profile:
            available = security.get_available_profiles()
            return Response(
                message=f"Missing 'profile' parameter. Available profiles: {', '.join(available)}",
                break_loop=False
            )
        
        # Attempt to change profile
        result = security.set_active_profile(profile)
        
        if not result["success"]:
            error = result.get("error", "Unknown error")
            available = result.get("available_profiles", [])
            msg = f"Failed to change profile: {error}"
            if available:
                msg += f"\nAvailable profiles: {', '.join(available)}"
            return Response(message=msg, break_loop=False)
        
        # Success - format detailed response
        lines = [
            f"✓ Profile changed: {result['previous_profile']} → {result['new_profile']}",
            "",
            "Security configuration updated. Changes take effect immediately."
        ]
        
        # Get new state to show impact
        state = security.get_security_state()
        lines.append("")
        lines.append("Current feature states:")
        for feature, info in state['features'].items():
            status = "ENABLED" if info['enabled'] else "DISABLED"
            lines.append(f"  - {feature}: {status}")
        
        return Response(
            message="\n".join(lines),
            break_loop=False
        )
    
    # Required base class methods for security-specific functionality
    
    def _get_available_profiles(self) -> list[str]:
        """Get available security profiles"""
        return self.system.get_available_profiles()
    
