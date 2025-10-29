import json
from typing import Any
from python.helpers.files import VariablesPlugin
from python.helpers import files
from python.helpers.print_style import PrintStyle

class InternalReasoningProfile(VariablesPlugin):
    def get_variables(self, file: str, backup_dirs: list[str] | None = None, **kwargs) -> dict[str, Any]:
        # Check if reasoning_control feature is enabled via SystemControl
        try:
            from python.helpers.system_control import SystemControl
            system = SystemControl()
            
            if not system.is_feature_enabled("reasoning_profile_control"):
                PrintStyle().hint(f"Reasoning Control DISABLED - Security profile: {system.get_active_profile()}")
                return {
                    "internal_reasoning_profile": "",
                    "internal_reasoning_features": ""
                }
        except ImportError:
            PrintStyle().hint("SystemControl not available - reasoning_control enabled by default")
        except Exception as e:
            PrintStyle().hint(f"Error checking reasoning_control feature: {e}")
        
        # Get active internal reasoning profile from SystemControl
        reasoning_features_summary = "(none)"
        try:
            from python.helpers.system_control import SystemControl
            system = SystemControl()
            active_profile = system.get_active_internal_reasoning_profile()
            
            # Get internal reasoning features
            reasoning_state = system.get_internal_reasoning_state()
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
            PrintStyle().error("SystemControl not available - using default internal reasoning")
            active_profile = "default"
        except Exception as e:
            PrintStyle().error(f"Error getting internal reasoning profile: {e}")
            active_profile = "default"
        
        # Build path to internal reasoning profile markdown
        reasoning_path = f"/a0/prompts/system/profiles/reasoning_profile/internal/profiles/{active_profile}.md"
        
        # Load file with graceful error handling
        if files.exists(reasoning_path):
            try:
                # Use read_prompt_file for templating support (placeholders, includes, nested plugins)
                reasoning_content = files.read_prompt_file(
                    reasoning_path,
                    _directories=[],  # No fallback dirs needed for absolute path
                    **kwargs  # Pass through all kwargs for future templating capabilities
                )
                PrintStyle().info(f"✓ Loaded internal reasoning profile: {active_profile}")
            except Exception as e:
                PrintStyle().error(f"Error loading internal reasoning '{reasoning_path}': {e}")
                reasoning_content = f"** Internal Reasoning Profile Error **\n\n(Error loading profile: {reasoning_path})\n\nException: {e}"
        else:
            PrintStyle().hint(f"Internal reasoning profile file not found: {reasoning_path}")
            reasoning_content = f"** Internal Reasoning Profile Not Found **\n\n(Profile file not found: {reasoning_path})\n\nUsing default behavior."
        
        # Load feature instruction files for enabled features
        enabled_features_content = []
        try:
            from python.helpers.system_control import SystemControl
            system = SystemControl()
            reasoning_state = system.get_internal_reasoning_state()
            reasoning_features = reasoning_state.get('features', {})
            
            for feature, config in reasoning_features.items():
                if config.get('enabled'):
                    # Use reference field or convention: {feature_name}.md
                    ref_file = config.get('reference', f"{feature}.md")
                    feature_path = f"/a0/prompts/system/profiles/reasoning_profile/internal/features/{ref_file}"
                    
                    if files.exists(feature_path):
                        try:
                            # Use read_prompt_file for templating support in feature files
                            feature_content = files.read_prompt_file(
                                feature_path,
                                _directories=[],
                                **kwargs  # Pass through for nested templating
                            )
                            enabled_features_content.append(feature_content)
                            PrintStyle().info(f"  ✓ Loaded internal reasoning feature: {feature}")
                        except Exception as e:
                            PrintStyle().hint(f"  ⚠ Error loading feature '{feature}': {e}")
                    else:
                        PrintStyle().hint(f"  • Feature file not found: {feature_path}")
        except Exception as e:
            PrintStyle().hint(f"Could not load internal reasoning feature files: {e}")
        
        # Combine profile content with enabled feature instructions
        if enabled_features_content:
            full_reasoning_content = reasoning_content + "\n\n".join(enabled_features_content)
        else:
            full_reasoning_content = reasoning_content
        
        # Create declarative status for agent self-awareness
        status_display = f"**{active_profile}**"
        
        return {
            "internal_reasoning_profile": full_reasoning_content,
            "internal_reasoning_features": reasoning_features_summary,
            "internal_reasoning_status": status_display
        }
