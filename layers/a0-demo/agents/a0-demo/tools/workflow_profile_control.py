from python.helpers.tool import Tool, Response
from python.helpers.system_control import SystemControl


class WorkflowProfileControlTool(Tool):
    """
    Tool for managing workflow profiles.
    Allows agent to view and switch between workflow profiles.
    """
    
    async def execute(self, action: str = "", **kwargs):
        """
        Execute workflow control action.
        
        Actions:
        - get_status: View full workflow state
        - get_profile: View active workflow profile
        - set_profile: Change active workflow profile (requires: profile="name")
        """
        
        system = SystemControl()
        
        # Check if tool itself is enabled
        if not system.is_feature_enabled("workflow_profile_control"):
            return Response(
                message="Workflow control tool is disabled by current security profile. Admin override required.",
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
        """Get current workflow state"""
        state = system.get_workflow_state()
        
        # Format response
        lines = [
            "=== Workflow Status ===",
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
            lines.append("  - (No features defined)")
        
        return Response(
            message="\n".join(lines),
            break_loop=False
        )
    
    async def _get_profile(self, system: SystemControl) -> Response:
        """Get current active workflow profile"""
        profile_name = system.get_active_workflow_profile()
        available = system.get_available_workflow_profiles()
        
        lines = [
            f"Active Workflow Profile: {profile_name}",
            f"Available Profiles: {', '.join(available)}"
        ]
        
        return Response(
            message="\n".join(lines),
            break_loop=False
        )
    
    async def _set_profile(self, system: SystemControl, kwargs: dict) -> Response:
        """Change active workflow profile"""
        profile = kwargs.get("profile", "")
        
        if not profile:
            available = system.get_available_workflow_profiles()
            return Response(
                message=f"Missing 'profile' parameter. Available profiles: {', '.join(available)}",
                break_loop=False
            )
        
        # Attempt to change profile
        result = system.set_active_workflow_profile(profile)
        
        if not result["success"]:
            error = result.get("error", "Unknown error")
            available = result.get("available_profiles", [])
            msg = f"Failed to change workflow profile: {error}"
            if available:
                msg += f"\nAvailable profiles: {', '.join(available)}"
            return Response(message=msg, break_loop=False)
        
        # Success - format detailed response
        lines = [
            f"✓ Workflow profile changed: {result['previous_profile']} → {result['new_profile']}",
            "",
            "Workflow configuration updated. Changes take effect immediately.",
            "",
            "Note: The new workflow profile prompt will be loaded on the next message loop."
        ]
        
        # Get new state to show impact
        state = system.get_workflow_state()
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