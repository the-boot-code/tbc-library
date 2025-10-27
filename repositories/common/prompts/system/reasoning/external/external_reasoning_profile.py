import json
from typing import Any
from python.helpers.files import VariablesPlugin
from python.helpers import files
from python.helpers.print_style import PrintStyle

class ExternalReasoningProfile(VariablesPlugin):
    def get_variables(self, file: str, backup_dirs: list[str] | None = None, **kwargs) -> dict[str, Any]:
        # Get active external reasoning profile from SystemControl
        reasoning_features_summary = "(none)"
        try:
            from python.helpers.system_control import SystemControl
            system = SystemControl()
            active_profile = system.get_active_external_reasoning_profile()
            
            # Get external reasoning features
            reasoning_state = system.get_external_reasoning_state()
            reasoning_features = reasoning_state.get('features', {})
            
            # Build features summary
            if reasoning_features:
                features_list = []
                for feature, config in reasoning_features.items():
                    enabled = config.get('enabled', False)
                    status = 'ENABLED' if enabled else 'disabled'
                    features_list.append(f"{feature}={status}")
                reasoning_features_summary = ', '.join(features_list)
            
        except ImportError:
            PrintStyle().error("SystemControl not available - using default external reasoning")
            active_profile = "default"
        except Exception as e:
            PrintStyle().error(f"Error getting external reasoning profile: {e}")
            active_profile = "default"
        
        # Build path to external reasoning profile markdown
        reasoning_path = f"/a0/prompts/system/reasoning/external/profiles/{active_profile}.md"
        
        # Load file with graceful error handling
        if files.exists(reasoning_path):
            try:
                reasoning_content = files.read_file(reasoning_path)
                PrintStyle().info(f"✓ Loaded external reasoning profile: {active_profile}")
            except Exception as e:
                PrintStyle().error(f"Error loading external reasoning '{reasoning_path}': {e}")
                reasoning_content = f"** External Reasoning Profile Error **\n\n(Error loading profile: {reasoning_path})\n\nException: {e}"
        else:
            PrintStyle().hint(f"External reasoning profile file not found: {reasoning_path}")
            reasoning_content = f"** External Reasoning Profile Not Found **\n\n(Profile file not found: {reasoning_path})\n\nUsing default behavior."
        
        # Load feature instruction files for enabled features
        enabled_features_content = []
        try:
            from python.helpers.system_control import SystemControl
            system = SystemControl()
            reasoning_state = system.get_external_reasoning_state()
            reasoning_features = reasoning_state.get('features', {})
            
            for feature, config in reasoning_features.items():
                if config.get('enabled'):
                    # Use reference field or convention: {feature_name}.md
                    ref_file = config.get('reference', f"{feature}.md")
                    feature_path = f"/a0/prompts/system/reasoning/external/features/{ref_file}"
                    
                    if files.exists(feature_path):
                        try:
                            feature_content = files.read_file(feature_path)
                            enabled_features_content.append(feature_content)
                            PrintStyle().info(f"  ✓ Loaded external reasoning feature: {feature}")
                        except Exception as e:
                            PrintStyle().hint(f"  ⚠ Error loading feature '{feature}': {e}")
                    else:
                        PrintStyle().hint(f"  • Feature file not found: {feature_path}")
        except Exception as e:
            PrintStyle().hint(f"Could not load external reasoning feature files: {e}")
        
        # Combine profile content with enabled feature instructions
        if enabled_features_content:
            full_reasoning_content = reasoning_content + "\n\n".join(enabled_features_content)
        else:
            full_reasoning_content = reasoning_content
        
        return {
            "external_reasoning_profile": full_reasoning_content,
            "external_reasoning_features": reasoning_features_summary
        }
