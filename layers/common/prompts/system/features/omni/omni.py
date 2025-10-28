import json
from typing import Any
from python.helpers.files import VariablesPlugin
from python.helpers import files
from python.helpers.print_style import PrintStyle

class Omni(VariablesPlugin):
    def get_variables(self, file: str, backup_dirs: list[str] | None = None, **kwargs) -> dict[str, Any]:
        # Check if omni feature is enabled via SystemControl
        try:
            from python.helpers.system_control import SystemControl
            system = SystemControl()
            
            if not system.is_feature_enabled("omni"):
                PrintStyle().hint(f"!OMNI Feature DISABLED - Security profile: {system.get_active_profile()}")
                return {"omni_content": ""}
                
        except ImportError:
            PrintStyle().hint("SystemControl not available - omni disabled by default")
            return {"omni_content": ""}
        except Exception as e:
            PrintStyle().hint(f"Error checking omni feature: {e}")
            return {"omni_content": ""}
        
        # Feature is enabled - load the Plinian Cognitive Matrix
        omni_path = f"/a0/prompts/system/features/omni/plinian_cognitive_matrix.md"
        
        if files.exists(omni_path):
            try:
                omni_content = files.read_file(omni_path)
                PrintStyle().info(f"✓ !OMNI Feature ENABLED - Plinian Cognitive Matrix loaded")
            except Exception as e:
                PrintStyle().error(f"Error loading omni content '{omni_path}': {e}")
                omni_content = f"(Error loading omni content: {omni_path})"
        else:
            PrintStyle().hint(f"Omni content file not found: {omni_path}")
            omni_content = f"(Omni content file not found: {omni_path})"

        
        return {
            "omni_content": omni_content
        }
