from python.helpers.tool import Tool, Response
from python.helpers.system_control import SystemControl


class FeatureControlTool(Tool):
    """
    Tool for managing feature options.
    Allows agent to view and toggle individual feature settings.
    """
    
    async def execute(self, action: str = "", **kwargs):
        """
        Execute feature control action.
        
        Actions:
        - get_feature: View specific feature status (optional: feature="name")
        - set_feature: Enable/disable a feature option (requires: feature="name", enabled=true/false)
        """
        
        system = SystemControl()
        
        # Check if tool itself is enabled
        if not system.is_feature_enabled("feature_control"):
            return Response(
                message="Feature control tool is disabled by current security profile. Admin override required.",
                break_loop=False
            )
        
        # Route to action handlers
        if action == "get_feature":
            return await self._get_feature(system, kwargs)
        elif action == "set_feature":
            return await self._set_feature(system, kwargs)
        else:
            return Response(
                message=f"Unknown action '{action}'. Available: get_feature, set_feature",
                break_loop=False
            )
    
    async def _get_feature(self, system: SystemControl, kwargs: dict) -> Response:
        """Get status of a specific feature"""
        feature = kwargs.get("feature", "")
        
        if not feature:
            # Show all features
            state = system.get_security_state()
            lines = ["Features:"]
            for feat, info in state['features'].items():
                status = "ENABLED" if info['enabled'] else "disabled"
                source = info['source']
                lines.append(f"  - {feat}: {status} (via {source})")
            return Response(message="\n".join(lines), break_loop=False)
        
        # Show specific feature
        available = system.get_available_features()
        if feature not in available:
            return Response(
                message=f"Feature '{feature}' not found. Available: {', '.join(available)}",
                break_loop=False
            )
        
        is_enabled = system.is_feature_enabled(feature)
        config = system.get_feature_config(feature)
        
        # Determine source
        state = system.get_security_state()
        source = state['features'][feature]['source']
        
        lines = [
            f"Feature: {feature}",
            f"Status: {'ENABLED' if is_enabled else 'disabled'}",
            f"Source: {source}",
            f"Config: {config}"
        ]
        
        return Response(
            message="\n".join(lines),
            break_loop=False
        )
    
    async def _set_feature(self, system: SystemControl, kwargs: dict) -> Response:
        """Enable/disable a feature option"""
        feature = kwargs.get("feature", "")
        enabled_str = kwargs.get("enabled", "")
        
        if not feature:
            available = system.get_available_features()
            return Response(
                message=f"Missing 'feature' parameter. Available features: {', '.join(available)}",
                break_loop=False
            )
        
        if enabled_str == "":
            return Response(
                message="Missing 'enabled' parameter. Use: enabled=true or enabled=false",
                break_loop=False
            )
        
        # Parse boolean
        if isinstance(enabled_str, bool):
            enabled = enabled_str
        elif enabled_str.lower() in ["true", "1", "yes"]:
            enabled = True
        elif enabled_str.lower() in ["false", "0", "no"]:
            enabled = False
        else:
            return Response(
                message=f"Invalid 'enabled' value: {enabled_str}. Use: true or false",
                break_loop=False
            )
        
        # Attempt to change feature
        result = system.set_feature_option(feature, enabled)
        
        if not result["success"]:
            error = result.get("error", "Unknown error")
            available = result.get("available_features", [])
            msg = f"Failed to change feature: {error}"
            if available:
                msg += f"\nAvailable features: {', '.join(available)}"
            return Response(message=msg, break_loop=False)
        
        # Success
        status = "enabled" if result["new_value"] else "disabled"
        lines = [
            f"✓ Feature '{feature}' {status}",
            ""
        ]
        
        # Add note if present
        if "note" in result:
            lines.append(f"Note: {result['note']}")
            lines.append("")
        
        # Show current effective state
        is_actually_enabled = system.is_feature_enabled(feature)
        if is_actually_enabled != enabled:
            lines.append(f"⚠ Feature is currently {'ENABLED' if is_actually_enabled else 'DISABLED'} due to active security profile override")
        else:
            lines.append(f"Feature is now {'ENABLED' if is_actually_enabled else 'DISABLED'}")
        
        return Response(
            message="\n".join(lines),
            break_loop=False
        )
