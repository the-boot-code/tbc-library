from python.helpers.tool import Tool, Response
from python.helpers.system_control import SystemControl
from .base_profile_control import BaseProfileControlTool


class WorkflowProfileControlTool(BaseProfileControlTool):
    """
    Tool for managing workflow profiles.
    Allows agent to view and switch between workflow profiles.
    
    FUTURE OPTION 2 NOTES:
    - Consider automated profile discovery from instruction files
    - Template-based response formatting for profile descriptions
    - Dynamic action registration from instruction metadata
    """
    
    # Configuration for base class
    profile_type = "workflow"
    available_actions = ["get_status", "get_profile", "set_profile"]
    
    def __init__(self):
        super().__init__()
        # Map actions to handler methods
        self.action_handlers = {
            "get_status": self._handle_get_status,
            "get_profile": self._handle_get_profile,
            "set_profile": self._handle_set_profile,
        }
    
    async def _handle_get_status(self, system: SystemControl, kwargs: dict) -> Response:
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
    
    async def _handle_get_profile(self, system: SystemControl, kwargs: dict) -> Response:
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
    
    async def _handle_set_profile(self, system: SystemControl, kwargs: dict) -> Response:
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
    
    # Required base class methods for workflow-specific functionality
    
    def _get_available_profiles(self) -> list[str]:
        """Get available workflow profiles"""
        return self.system.get_available_workflow_profiles()