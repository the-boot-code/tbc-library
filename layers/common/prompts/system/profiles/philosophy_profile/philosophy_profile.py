import json
from typing import Any
from python.helpers.files import VariablesPlugin
from python.helpers import files
from python.helpers.print_style import PrintStyle

class PhilosophyProfile(VariablesPlugin):
    def get_variables(self, file: str, backup_dirs: list[str] | None = None, **kwargs) -> dict[str, Any]:
        # Check if philosophy_control feature is enabled via SystemControl
        try:
            from python.helpers.system_control import SystemControl
            system = SystemControl()
            
            if not system.is_feature_enabled("philosophy_control"):
                PrintStyle().hint(f"Philosophy Control DISABLED - Security profile: {system.get_active_profile()}")
                return {
                    "philosophy_profile": "",
                    "philosophy_features": ""
                }
        except ImportError:
            PrintStyle().hint("SystemControl not available - philosophy_control enabled by default")
        except Exception as e:
            PrintStyle().hint(f"Error checking philosophy_control feature: {e}")
        
        # Get active philosophy profile from SystemControl
        philosophy_features_summary = "(none)"
        try:
            from python.helpers.system_control import SystemControl
            system = SystemControl()
            active_profile = system.get_active_philosophy_profile()
            
            # Get philosophy features
            philosophy_state = system.get_philosophy_state()
            philosophy_features = philosophy_state.get('features', {})
            
            # Build features summary
            if philosophy_features:
                features_list = []
                for feature, config in philosophy_features.items():
                    enabled = config.get('enabled', False)
                    status = 'ENABLED' if enabled else 'disabled'
                    features_list.append(f"{feature}={status}")
                philosophy_features_summary = ', '.join(features_list)
            
        except ImportError:
            PrintStyle().error("SystemControl not available - using default philosophy")
            active_profile = "default"
        except Exception as e:
            PrintStyle().error(f"Error getting philosophy profile: {e}")
            active_profile = "default"
        
        # Build path to philosophy profile markdown
        philosophy_path = f"/a0/prompts/system/profiles/philosophy_profile/profiles/{active_profile}.md"
        
        # Load file with graceful error handling
        if files.exists(philosophy_path):
            try:
                # Use read_prompt_file for templating support (placeholders, includes, nested plugins)
                philosophy_content = files.read_prompt_file(
                    philosophy_path,
                    _directories=[],  # No fallback dirs needed for absolute path
                    **kwargs  # Pass through all kwargs for future templating capabilities
                )
                PrintStyle().info(f"✓ Loaded philosophy profile: {active_profile}")
            except Exception as e:
                PrintStyle().error(f"Error loading philosophy '{philosophy_path}': {e}")
                philosophy_content = f"** Philosophy Profile Error **\n\n(Error loading philosophy profile: {philosophy_path})\n\nException: {e}"
        else:
            PrintStyle().hint(f"Philosophy profile file not found: {philosophy_path}")
            philosophy_content = f"** Philosophy Profile Not Found **\n\n(Philosophy profile file not found: {philosophy_path})\n\nUsing default behavior."
        
        # Load feature instruction files for enabled features
        enabled_features_content = []
        try:
            from python.helpers.system_control import SystemControl
            system = SystemControl()
            philosophy_state = system.get_philosophy_state()
            philosophy_features = philosophy_state.get('features', {})
            
            for feature, config in philosophy_features.items():
                if config.get('enabled'):
                    # Use reference field or convention: {feature_name}.md
                    ref_file = config.get('reference', f"{feature}.md")
                    feature_path = f"/a0/prompts/system/profiles/philosophy_profile/features/{ref_file}"
                    
                    if files.exists(feature_path):
                        try:
                            # Use read_prompt_file for templating support in feature files
                            feature_content = files.read_prompt_file(
                                feature_path,
                                _directories=[],
                                **kwargs  # Pass through for nested templating
                            )
                            enabled_features_content.append(feature_content)
                            PrintStyle().info(f"  ✓ Loaded philosophy feature: {feature}")
                        except Exception as e:
                            PrintStyle().hint(f"  ⚠ Error loading feature '{feature}': {e}")
                    else:
                        PrintStyle().hint(f"  • Feature file not found: {feature_path}")
        except Exception as e:
            PrintStyle().hint(f"Could not load philosophy feature files: {e}")
        
        # Combine profile content with enabled feature instructions
        if enabled_features_content:
            full_philosophy_content = philosophy_content + "\n\n" + "\n\n".join(enabled_features_content)
        else:
            full_philosophy_content = philosophy_content
        
        # Create declarative status for agent self-awareness
        status_display = f"**{active_profile}**"
        
        return {
            "philosophy_profile": full_philosophy_content,
            "philosophy_features": philosophy_features_summary,
            "philosophy_status": status_display
        }
