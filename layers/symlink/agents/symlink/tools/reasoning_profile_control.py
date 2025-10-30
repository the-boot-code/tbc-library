from python.helpers.tool import Tool, Response
from python.helpers.system_control import SystemControl


class ReasoningProfileControlTool(Tool):
    """
    Tool for managing reasoning profiles across three types: internal, interleaved, external.
    Allows agent to view and switch between reasoning profiles for each type.
    """
    
    async def execute(self, reasoning_type: str = "", action: str = "", **kwargs):
        """
        Execute reasoning profile control action.
        
        Parameters:
        - reasoning_type: Type of reasoning (internal, interleaved, external) - required for most actions
        - action: Action to perform (get_all, get_status, get_profile, set_profile)
        
        Actions:
        - get_all: View all reasoning types and their active profiles (no reasoning_type needed)
        - get_status: View full state for a specific reasoning type (requires reasoning_type)
        - get_profile: View active profile for a specific reasoning type (requires reasoning_type)
        - set_profile: Change profile for a specific reasoning type (requires reasoning_type and profile)
        """
        
        system = SystemControl()
        
        # Check if tool itself is enabled
        if not system.is_feature_enabled("reasoning_profile_control"):
            return Response(
                message="Reasoning profile control tool is disabled by current security profile. Admin override required.",
                break_loop=False
            )
        
        # Route to action handlers
        if action == "get_all":
            return await self._get_all(system)
        elif action == "get_status":
            return await self._get_status(system, reasoning_type)
        elif action == "get_profile":
            return await self._get_profile(system, reasoning_type)
        elif action == "set_profile":
            return await self._set_profile(system, reasoning_type, kwargs)
        else:
            return Response(
                message=f"Unknown action '{action}'. Available: get_all, get_status, get_profile, set_profile",
                break_loop=False
            )
    
    async def _get_all(self, system: SystemControl) -> Response:
        """Get all reasoning types and their active profiles"""
        lines = [
            "=== All Reasoning Profiles ===",
            ""
        ]
        
        # Internal reasoning
        internal_profile = system.get_active_internal_reasoning_profile()
        lines.append(f"Internal Reasoning: {internal_profile}")
        
        # Interleaved reasoning
        interleaved_profile = system.get_active_interleaved_reasoning_profile()
        lines.append(f"Interleaved Reasoning: {interleaved_profile}")
        
        # External reasoning
        external_profile = system.get_active_external_reasoning_profile()
        lines.append(f"External Reasoning: {external_profile}")
        
        lines.append("")
        lines.append("Use action='get_status' with a specific reasoning_type to see available profiles.")
        
        return Response(
            message="\n".join(lines),
            break_loop=False
        )
    
    async def _get_status(self, system: SystemControl, reasoning_type: str) -> Response:
        """Get full reasoning state for a specific type"""
        if not reasoning_type:
            return Response(
                message="Missing 'reasoning_type' parameter. Required values: internal, interleaved, external",
                break_loop=False
            )
        
        # Validate reasoning type
        valid_types = ["internal", "interleaved", "external"]
        if reasoning_type not in valid_types:
            return Response(
                message=f"Invalid reasoning_type '{reasoning_type}'. Valid types: {', '.join(valid_types)}",
                break_loop=False
            )
        
        # Get state for specific type
        if reasoning_type == "internal":
            state = system.get_internal_reasoning_state()
        elif reasoning_type == "interleaved":
            state = system.get_interleaved_reasoning_state()
        else:  # external
            state = system.get_external_reasoning_state()
        
        # Format response
        lines = [
            f"=== {reasoning_type.title()} Reasoning Status ===",
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
        
        return Response(
            message="\n".join(lines),
            break_loop=False
        )
    
    async def _get_profile(self, system: SystemControl, reasoning_type: str) -> Response:
        """Get active profile for a specific reasoning type"""
        if not reasoning_type:
            return Response(
                message="Missing 'reasoning_type' parameter. Required values: internal, interleaved, external",
                break_loop=False
            )
        
        # Validate reasoning type
        valid_types = ["internal", "interleaved", "external"]
        if reasoning_type not in valid_types:
            return Response(
                message=f"Invalid reasoning_type '{reasoning_type}'. Valid types: {', '.join(valid_types)}",
                break_loop=False
            )
        
        # Get profile for specific type
        if reasoning_type == "internal":
            profile_name = system.get_active_internal_reasoning_profile()
            available = system.get_available_internal_reasoning_profiles()
        elif reasoning_type == "interleaved":
            profile_name = system.get_active_interleaved_reasoning_profile()
            available = system.get_available_interleaved_reasoning_profiles()
        else:  # external
            profile_name = system.get_active_external_reasoning_profile()
            available = system.get_available_external_reasoning_profiles()
        
        lines = [
            f"Active {reasoning_type.title()} Reasoning Profile: {profile_name}",
            f"Available Profiles: {', '.join(available)}"
        ]
        
        return Response(
            message="\n".join(lines),
            break_loop=False
        )
    
    async def _set_profile(self, system: SystemControl, reasoning_type: str, kwargs: dict) -> Response:
        """Change reasoning profile for a specific type"""
        if not reasoning_type:
            return Response(
                message="Missing 'reasoning_type' parameter. Required values: internal, interleaved, external",
                break_loop=False
            )
        
        # Validate reasoning type
        valid_types = ["internal", "interleaved", "external"]
        if reasoning_type not in valid_types:
            return Response(
                message=f"Invalid reasoning_type '{reasoning_type}'. Valid types: {', '.join(valid_types)}",
                break_loop=False
            )
        
        profile = kwargs.get("profile", "")
        if not profile:
            # Get available profiles for error message
            if reasoning_type == "internal":
                available = system.get_available_internal_reasoning_profiles()
            elif reasoning_type == "interleaved":
                available = system.get_available_interleaved_reasoning_profiles()
            else:  # external
                available = system.get_available_external_reasoning_profiles()
            
            return Response(
                message=f"Missing 'profile' parameter. Available {reasoning_type} profiles: {', '.join(available)}",
                break_loop=False
            )
        
        # Attempt to change profile
        if reasoning_type == "internal":
            result = system.set_active_internal_reasoning_profile(profile)
        elif reasoning_type == "interleaved":
            result = system.set_active_interleaved_reasoning_profile(profile)
        else:  # external
            result = system.set_active_external_reasoning_profile(profile)
        
        if not result["success"]:
            error = result.get("error", "Unknown error")
            available = result.get("available_profiles", [])
            msg = f"Failed to change {reasoning_type} reasoning profile: {error}"
            if available:
                msg += f"\nAvailable profiles: {', '.join(available)}"
            return Response(message=msg, break_loop=False)
        
        # Success - format detailed response
        lines = [
            f"✓ {reasoning_type.title()} reasoning profile changed: {result['previous_profile']} → {result['new_profile']}",
            "",
            "Reasoning configuration updated. Changes take effect immediately.",
            "",
            "Note: The new reasoning profile prompt will be loaded on the next message loop."
        ]
        
        # Get new state to show impact
        if reasoning_type == "internal":
            state = system.get_internal_reasoning_state()
        elif reasoning_type == "interleaved":
            state = system.get_interleaved_reasoning_state()
        else:  # external
            state = system.get_external_reasoning_state()
        
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
