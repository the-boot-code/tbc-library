import json
from typing import Any
from python.helpers.files import VariablesPlugin
from python.helpers import files
from python.helpers.print_style import PrintStyle

class WorkflowProfile(VariablesPlugin):
    def get_variables(self, file: str, backup_dirs: list[str] | None = None, **kwargs) -> dict[str, Any]:
        # Check if workflow_control feature is enabled via SystemControl
        try:
            from python.helpers.system_control import SystemControl
            system = SystemControl()
            
            if not system.is_feature_enabled("workflow_profile_control"):
                PrintStyle().hint(f"Workflow Control DISABLED - Security profile: {system.get_active_profile()}")
                return {
                    "workflow_profile": "",
                    "workflow_features": ""
                }
        except ImportError:
            PrintStyle().hint("SystemControl not available - workflow_control enabled by default")
        except Exception as e:
            PrintStyle().hint(f"Error checking workflow_control feature: {e}")
        
        # Get active workflow profile from SystemControl
        workflow_features_summary = "(none)"
        try:
            from python.helpers.system_control import SystemControl
            system = SystemControl()
            active_profile = system.get_active_workflow_profile()
            
            # Get workflow features
            workflow_state = system.get_workflow_state()
            workflow_features = workflow_state.get('features', {})
            
            # Build features summary
            if workflow_features:
                features_list = []
                for feature, config in workflow_features.items():
                    enabled = config.get('enabled', False)
                    status = 'ENABLED' if enabled else 'disabled'
                    features_list.append(f"{feature}={status}")
                workflow_features_summary = ', '.join(features_list)
            
        except ImportError:
            PrintStyle().error("SystemControl not available - using default workflow")
            active_profile = "default"
        except Exception as e:
            PrintStyle().error(f"Error getting workflow profile: {e}")
            active_profile = "default"
        
        # Build path to workflow profile markdown
        workflow_path = f"/a0/prompts/system/profiles/workflow_profile/profiles/{active_profile}.md"
        
        # Load file with graceful error handling
        if files.exists(workflow_path):
            try:
                # Use read_prompt_file for templating support (placeholders, includes, nested plugins)
                workflow_content = files.read_prompt_file(
                    workflow_path,
                    _directories=[],  # No fallback dirs needed for absolute path
                    **kwargs  # Pass through all kwargs for future templating capabilities
                )
                PrintStyle().info(f"✓ Loaded workflow profile: {active_profile}")
            except Exception as e:
                PrintStyle().error(f"Error loading workflow '{workflow_path}': {e}")
                workflow_content = f"** Workflow Profile Error **\n\n(Error loading workflow profile: {workflow_path})\n\nException: {e}"
        else:
            PrintStyle().hint(f"Workflow profile file not found: {workflow_path}")
            workflow_content = f"** Workflow Profile Not Found **\n\n(Workflow profile file not found: {workflow_path})\n\nUsing default behavior."
        
        # Load feature instruction files for enabled features
        enabled_features_content = []
        try:
            from python.helpers.system_control import SystemControl
            system = SystemControl()
            workflow_state = system.get_workflow_state()
            workflow_features = workflow_state.get('features', {})
            
            for feature, config in workflow_features.items():
                if config.get('enabled'):
                    # Use reference field or convention: {feature_name}.md
                    ref_file = config.get('reference', f"{feature}.md")
                    feature_path = f"/a0/prompts/system/profiles/workflow_profile/features/{ref_file}"
                    
                    if files.exists(feature_path):
                        try:
                            # Use read_prompt_file for templating support in feature files
                            feature_content = files.read_prompt_file(
                                feature_path,
                                _directories=[],
                                **kwargs  # Pass through for nested templating
                            )
                            enabled_features_content.append(feature_content)
                            PrintStyle().info(f"  ✓ Loaded feature: {feature}")
                        except Exception as e:
                            PrintStyle().hint(f"  ⚠ Error loading feature '{feature}': {e}")
                    else:
                        PrintStyle().hint(f"  • Feature file not found: {feature_path}")
        except Exception as e:
            PrintStyle().hint(f"Could not load feature files: {e}")
        
        # Combine profile content with enabled feature instructions
        if enabled_features_content:
            full_workflow_content = workflow_content + "\n\n".join(enabled_features_content)
        else:
            full_workflow_content = workflow_content
        
        # Create declarative status for agent self-awareness
        status_display = f"**{active_profile}**"
        
        return {
            "workflow_profile": full_workflow_content,
            "workflow_features": workflow_features_summary,
            "workflow_status": status_display
        }
