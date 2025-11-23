from python.helpers.tool import Tool, Response
from control_layer.python.helpers.system_control import SystemControl


profile_module_control_key = "reasoning_profile_control"
profile_module_display_name = "Reasoning Profile"

reasoning_type_module_names = {
    "internal": "reasoning_internal_profile",
    "interleaved": "reasoning_interleaved_profile",
    "external": "reasoning_external_profile",
}


class ProfileControlTool(Tool):
    """
    Tool for managing SystemControl reasoning profiles across three types: internal, interleaved, external.
    Allows agent to view and switch between reasoning profiles for each type and inspect their prompt includes.
    """
    
    reasoning_types = ["internal", "interleaved", "external"]
    
    async def execute(self, reasoning_type: str = "", action: str = "", **kwargs):
        """
        Execute profile control action.
        
        Actions:
        - get_all: Get all profile types and their active profiles
        - get_state: View full profile state for a specific type
        - get_profile: View active profile for a specific type
        - set_profile: Change profile for a specific type (requires: profile="name")
        """
        
        system = SystemControl()
        
        # Check if tool itself is enabled
        if not system.is_control_enabled(profile_module_control_key):
            return Response(
                message=f"{profile_module_display_name} control tool is disabled by current security profile. Admin override required.",
                break_loop=False
            )
        
        # Route to action handlers
        if action == "get_all":
            return await self._get_all(system)
        elif action == "get_state":
            return await self._get_status(system, reasoning_type)
        elif action == "get_profile":
            return await self._get_profile(system, reasoning_type)
        elif action == "set_profile":
            return await self._set_profile(system, reasoning_type, kwargs)
        else:
            return Response(
                message=f"Unknown action '{action}'. Available: get_all, get_state, get_profile, set_profile",
                break_loop=False
            )
    
    async def _get_all(self, system: SystemControl) -> Response:
        """Get all reasoning types and their active profiles"""
        lines = [
            "=== All Reasoning Profiles ===",
            ""
        ]
        
        # Internal reasoning
        internal_profile = system.get_active_profile(reasoning_type_module_names["internal"])
        lines.append(f"Internal Reasoning: {internal_profile}")
        
        # Interleaved reasoning
        interleaved_profile = system.get_active_profile(reasoning_type_module_names["interleaved"])
        lines.append(f"Interleaved Reasoning: {interleaved_profile}")
        
        # External reasoning
        external_profile = system.get_active_profile(reasoning_type_module_names["external"])
        lines.append(f"External Reasoning: {external_profile}")
        
        lines.append("")
        lines.append("Use action='get_state' with a specific reasoning_type to see available profiles.")
        
        return Response(
            message="\n".join(lines),
            break_loop=False
        )
    
    async def _get_status(self, system: SystemControl, reasoning_type: str) -> Response:
        """Get full reasoning state for a specific type (profile and prompt includes)"""
        if not reasoning_type:
            return Response(
                message="Missing 'reasoning_type' parameter. Required values: internal, interleaved, external",
                break_loop=False,
            )

        # Validate reasoning type
        valid_types = self.reasoning_types
        if reasoning_type not in valid_types:
            return Response(
                message=f"Invalid reasoning_type '{reasoning_type}'. Valid types: {', '.join(valid_types)}",
                break_loop=False,
            )

        profile_module_name = reasoning_type_module_names[reasoning_type]
        display_name = f"{reasoning_type.title()} Reasoning Profile"

        result = system.run_profile_control(
            profile_module_name=profile_module_name,
            profile_module_control_key=profile_module_control_key,
            profile_module_display_name=display_name,
            action="get_state",
        )

        message = result.get("message", "")
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
    
    async def _get_profile(self, system: SystemControl, reasoning_type: str) -> Response:
        """Get active profile for a specific reasoning type"""
        if not reasoning_type:
            return Response(
                message="Missing 'reasoning_type' parameter. Required values: internal, interleaved, external",
                break_loop=False,
            )

        # Validate reasoning type
        valid_types = self.reasoning_types
        if reasoning_type not in valid_types:
            return Response(
                message=f"Invalid reasoning_type '{reasoning_type}'. Valid types: {', '.join(valid_types)}",
                break_loop=False,
            )

        profile_module_name = reasoning_type_module_names[reasoning_type]
        display_name = f"{reasoning_type.title()} Reasoning Profile"

        result = system.run_profile_control(
            profile_module_name=profile_module_name,
            profile_module_control_key=profile_module_control_key,
            profile_module_display_name=display_name,
            action="get_profile",
        )

        return Response(
            message=result.get("message", ""),
            break_loop=result.get("break_loop", False),
        )

    async def _set_profile(self, system: SystemControl, reasoning_type: str, kwargs: dict) -> Response:
        """Change reasoning profile for a specific type"""
        if not reasoning_type:
            return Response(
                message="Missing 'reasoning_type' parameter. Required values: internal, interleaved, external",
                break_loop=False,
            )

        # Validate reasoning type
        valid_types = self.reasoning_types
        if reasoning_type not in valid_types:
            return Response(
                message=f"Invalid reasoning_type '{reasoning_type}'. Valid types: {', '.join(valid_types)}",
                break_loop=False,
            )

        profile_module_name = reasoning_type_module_names[reasoning_type]
        display_name = f"{reasoning_type.title()} Reasoning Profile"

        result = system.run_profile_control(
            profile_module_name=profile_module_name,
            profile_module_control_key=profile_module_control_key,
            profile_module_display_name=display_name,
            action="set_profile",
            **kwargs,
        )

        return Response(
            message=result.get("message", ""),
            break_loop=result.get("break_loop", False),
        )
