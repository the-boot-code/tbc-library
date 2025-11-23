from python.helpers.tool import Tool, Response
from control_layer.python.helpers.system_control import SystemControl


profile_module_name = "philosophy_profile"
profile_module_control_key = "philosophy_profile_control"
profile_module_display_name = "Philosophy Profile"


class ProfileControlTool(Tool):
    """
    Tool for managing SystemControl profiles.
    Allows the agent to view and switch between profiles and inspect their prompt includes.
    """
    
    async def execute(self, action: str = "", **kwargs):
        """
        Execute profile control action.

        Actions:
        - get_state: View current profile, available profiles, and active features
        - get_profile: View just the active profile
        - set_profile: Change active profile (requires: profile="name")
        """
        
        system = SystemControl()
        
        # Check if tool itself is enabled
        if not system.is_control_enabled(profile_module_control_key):
            return Response(
                message=f"{profile_module_display_name} control tool is disabled by current security profile. Admin override required.",
                break_loop=False
            )
        
        result = system.run_profile_control(
            profile_module_name=profile_module_name,
            profile_module_control_key=profile_module_control_key,
            profile_module_display_name=profile_module_display_name,
            action=action,
            **kwargs,
        )

        message = result.get("message", "")
        if action == "get_state":
            extra_lines = []
            if extra_lines:
                if message:
                    message = "\n".join([message, *extra_lines])
                else:
                    message = "\n".join(extra_lines)

        return Response(
            message=message,
            break_loop=result.get("break_loop", False),
        )
