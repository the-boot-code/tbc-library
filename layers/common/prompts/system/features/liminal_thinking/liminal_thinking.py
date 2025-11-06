import json
from typing import Any
from python.helpers.files import VariablesPlugin
from python.helpers import files
from python.helpers.print_style import PrintStyle

class Feature(VariablesPlugin):
    def get_variables(self, file: str, backup_dirs: list[str] | None = None, **kwargs) -> dict[str, Any]:
        # Check if feature is enabled via SystemControl
        feature_name = "liminal_thinking"
        feature_content = ""
        try:
            from python.helpers.system_control import SystemControl
            system = SystemControl()
            
            if not system.is_feature_enabled(feature_name):
                PrintStyle().hint(f"{feature_name} Feature DISABLED - Security profile: {system.get_active_profile()}")
                return {"feature_content": ""}
                
        except ImportError:
            PrintStyle().hint("SystemControl not available - {feature_name} disabled by default")
            return {"feature_content": ""}
        except Exception as e:
            PrintStyle().hint(f"Error checking omni feature: {e}")
            return {"feature_content": ""}
        
        # Feature is enabled - load
        feature_path = f"/a0/prompts/system/features/liminal_thinking/liminal_thinking_codex.md"
        
        if files.exists(feature_path):
            try:
                # Use read_prompt_file for templating support (placeholders, includes, nested plugins)
                feature_content = files.read_prompt_file(
                    feature_path,
                    _directories=[],  # No fallback dirs needed for absolute path
                    **kwargs  # Pass through all kwargs for future templating capabilities
                )
                PrintStyle().info(f"✓ {feature_name} Feature ENABLED - Liminal Thinking loaded")
            except Exception as e:
                PrintStyle().error(f"Error loading {feature_name} content '{feature_path}': {e}")
                feature_content = f"(Error loading {feature_name} content: {feature_path})"
        else:
            PrintStyle().hint(f"{feature_name} content file not found: {feature_path}")
            feature_content = f"({feature_name} content file not found: {feature_path})"

        
        return {
            "feature_content": feature_content
        }
