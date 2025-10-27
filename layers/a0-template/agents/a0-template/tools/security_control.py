from python.helpers.tool import Tool, Response
from python.helpers.system_control import SystemControl


class SecurityControlTool(Tool):
    """
    Tool for managing security profiles.
    Allows agent to view and switch between security profiles.
    """
    
    async def execute(self, action: str = "", **kwargs):
        """
        Execute security control action.
        
        Actions:
        - get_status: View full security state
        - get_profile: View active profile
        - set_profile: Change active security profile (requires: profile="name")
        """
        
        security = SystemControl()
        
        # Check if tool itself is enabled
        if not security.is_feature_enabled("security_control"):
            return Response(
                message="Security control tool is disabled by current security profile. Admin override required.",
                break_loop=False
            )
        
        # Route to action handlers
        if action == "get_status":
            return await self._get_status(security)
        elif action == "get_profile":
            return await self._get_profile(security)
        elif action == "set_profile":
            return await self._set_profile(security, kwargs)
        else:
            return Response(
                message=f"Unknown action '{action}'. Available: get_status, get_profile, set_profile",
                break_loop=False
            )
    
    async def _get_status(self, security: SystemControl) -> Response:
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
    
    async def _get_profile(self, security: SystemControl) -> Response:
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
    
    async def _set_profile(self, security: SystemControl, kwargs: dict) -> Response:
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
    
