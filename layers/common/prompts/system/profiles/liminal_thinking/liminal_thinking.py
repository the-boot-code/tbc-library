import json
from typing import Any
from python.helpers.files import VariablesPlugin
from python.helpers import files
from python.helpers.print_style import PrintStyle

class LiminalThinkingProfile(VariablesPlugin):
    def get_variables(self, file: str, backup_dirs: list[str] | None = None, **kwargs) -> dict[str, Any]:
        # Check if liminal_thinking_profile_control feature is enabled via SystemControl
        try:
            from python.helpers.system_control import SystemControl
            system = SystemControl()
            
            if not system.is_feature_enabled("liminal_thinking_profile_control"):
                PrintStyle().hint(f"Liminal Thinking Control DISABLED - Security profile: {system.get_active_profile()}")
                return {
                    "liminal_thinking_profile": "",
                    "liminal_thinking_features": "",
                    "liminal_status": "**disabled**"
                }
        except ImportError:
            PrintStyle().hint("SystemControl not available - liminal_thinking_control enabled by default")
        except Exception as e:
            PrintStyle().hint(f"Error checking liminal_thinking_control feature: {e}")
        
        # Get active liminal thinking profile from SystemControl
        liminal_features_summary = "(none)"
        try:
            from python.helpers.system_control import SystemControl
            system = SystemControl()
            active_profile = system.get_active_liminal_thinking_profile()
            
            # Get liminal thinking features
            liminal_state = system.get_liminal_thinking_state()
            liminal_features = liminal_state.get('features', {})
            
            # Build features summary
            if liminal_features:
                features_list = []
                for feature, config in liminal_features.items():
                    enabled = config.get('enabled', False)
                    status = 'ENABLED' if enabled else 'disabled'
                    features_list.append(f"{feature}={status}")
                liminal_features_summary = ', '.join(features_list)
            
        except ImportError:
            PrintStyle().error("SystemControl not available - using default liminal thinking")
            active_profile = "default"
        except Exception as e:
            PrintStyle().error(f"Error getting liminal thinking profile: {e}")
            active_profile = "default"
        
        # Build path to liminal thinking profile markdown
        liminal_path = f"/a0/prompts/system/profiles/liminal_thinking/profiles/{active_profile}.md"
        
        # Load file with graceful error handling
        if files.exists(liminal_path):
            try:
                # Use read_prompt_file for templating support (placeholders, includes, nested plugins)
                liminal_content = files.read_prompt_file(
                    liminal_path,
                    _directories=[],  # No fallback dirs needed for absolute path
                    **kwargs  # Pass through all kwargs for future templating capabilities
                )
                PrintStyle().info(f"✓ Loaded liminal thinking profile: {active_profile}")
            except Exception as e:
                PrintStyle().error(f"Error loading liminal thinking '{liminal_path}': {e}")
                liminal_content = f"** Liminal Thinking Profile Error **\n\n(Error loading profile: {liminal_path})\n\nException: {e}"
        else:
            PrintStyle().hint(f"Liminal thinking profile file not found: {liminal_path}")
            liminal_content = f"** Liminal Thinking Profile Not Found **\n\n(Profile file not found: {liminal_path})\n\nUsing default behavior."
        
        # Load feature instruction files for enabled features
        enabled_features_content = []
        try:
            from python.helpers.system_control import SystemControl
            system = SystemControl()
            liminal_state = system.get_liminal_thinking_state()
            liminal_features = liminal_state.get('features', {})
            
            for feature, config in liminal_features.items():
                if config.get('enabled'):
                    # Use reference field or convention: {feature_name}.md
                    ref_file = config.get('reference', f"{feature}.md")
                    feature_path = f"/a0/prompts/system/profiles/liminal_thinking/features/{ref_file}"
                    
                    if files.exists(feature_path):
                        try:
                            # Use read_prompt_file for templating support in feature files
                            feature_content = files.read_prompt_file(
                                feature_path,
                                _directories=[],
                                **kwargs  # Pass through for nested templating
                            )
                            enabled_features_content.append(feature_content)
                            PrintStyle().info(f"  ✓ Loaded liminal thinking feature: {feature}")
                        except Exception as e:
                            PrintStyle().hint(f"  ⚠ Error loading feature '{feature}': {e}")
                    else:
                        PrintStyle().hint(f"  • Feature file not found: {feature_path}")
        except Exception as e:
            PrintStyle().hint(f"Could not load liminal thinking feature files: {e}")
        
        # Combine profile content with enabled feature instructions
        if enabled_features_content:
            full_liminal_content = liminal_content + "\n\n" + "\n\n".join(enabled_features_content)
        else:
            full_liminal_content = liminal_content
        
        # Create declarative status for agent self-awareness
        status_display = f"**{active_profile}**"
        
        return {
            "liminal_thinking_profile": full_liminal_content,
            "liminal_thinking_features": liminal_features_summary,
            "liminal_status": status_display
        }
