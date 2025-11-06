import json
from typing import Any, Dict, List, Optional
from python.helpers.files import VariablesPlugin
from python.helpers import files
from python.helpers.print_style import PrintStyle

class ProfileLoader:
    """Helper class for loading and managing profile data."""
    
    def __init__(self):
        self.system = None
        self.active_profile = "default"
        self.features = {}
        self.features_list = []
        self.profile_content = ""
    
    def _initialize_system_control(self) -> bool:
        """Initialize SystemControl and check if feature is enabled."""
        try:
            from python.helpers.system_control import SystemControl
            self.system = SystemControl()
            
            if not self.system.is_feature_enabled("reasoning_profile_control"):
                disabled_msg = f"⚠️ Internal Reasoning Control is currently disabled (Security profile: {self.system.get_active_profile()})"
                PrintStyle().hint(disabled_msg)
                self.profile_content = f"# Internal Reasoning Profile\n\n{disabled_msg}\n\nPlease contact your system administrator to enable this feature."
                return False
            return True
            
        except ImportError as e:
            error_msg = f"❌ System Error: Could not load SystemControl module: {e}"
            PrintStyle().error(error_msg)
            self.profile_content = f"# Internal Reasoning Profile\n\n{error_msg}\n\nPlease ensure the SystemControl module is properly installed and configured."
            return False
    
    def _load_profile_data(self) -> None:
        """Load the active profile and its features."""
        if not self.system:
            return
            
        try:
            self.active_profile = self.system.get_active_internal_reasoning_profile()
            reasoning_state = self.system.get_internal_reasoning_state()
            self.features = reasoning_state.get('features', {})
            self.features_list = [f for f, cfg in self.features.items() if cfg.get('enabled')]
            PrintStyle().info(f"✓ Loaded internal reasoning profile: {self.active_profile}")
            
        except Exception as e:
            PrintStyle().warning(f"⚠️ Could not load profile settings: {e}")
    
    def _load_profile_content(self, **kwargs) -> None:
        """Load the content of the active profile."""
        profile_path = f"/a0/prompts/system/profiles/reasoning_profile/internal/profiles/{self.active_profile}.md"
        
        try:
            if not files.exists(profile_path):
                raise FileNotFoundError(f"Profile file not found: {profile_path}")
                
            self.profile_content = files.read_prompt_file(profile_path, _directories=[], **kwargs)
            
        except Exception as e:
            error_msg = f"⚠️ Could not load profile '{self.active_profile}': {e}"
            PrintStyle().warning(error_msg)
            
            if self.active_profile != "default":
                try:
                    self.active_profile = "default"
                    default_path = "/a0/prompts/system/profiles/reasoning_profile/internal/profiles/default.md"
                    if files.exists(default_path):
                        self.profile_content = files.read_prompt_file(default_path, _directories=[], **kwargs)
                        PrintStyle().info("✓ Fallback to default profile successful")
                        return
                    raise FileNotFoundError("Default profile not found")
                except Exception as default_error:
                    error_msg += f"\n\nFailed to load default profile: {default_error}"
            
            self.profile_content = f"# Internal Reasoning Profile\n\n{error_msg}"
    
    def _load_feature_content(self, **kwargs) -> str:
        """Load content for all enabled features."""
        if not self.features_list:
            return ""
            
        features_content = []
        
        for feature in self.features_list:
            try:
                ref_file = self.features[feature].get('reference', f"{feature}.md")
                feature_path = f"/a0/prompts/system/profiles/reasoning_profile/internal/features/{ref_file}"
                
                if files.exists(feature_path):
                    content = files.read_prompt_file(feature_path, _directories=[], **kwargs)
                    features_content.append(content)
                    PrintStyle().info(f"  ✓ Loaded feature: {feature}")
                else:
                    PrintStyle().warning(f"  • Feature file not found: {feature_path}")
            except Exception as e:
                PrintStyle().warning(f"  • Could not load feature '{feature}': {e}")
        
        if not features_content:
            return ""
            
        return "\n\n## Active Features\n\n" + "\n\n".join(features_content)
    
    def build_response(self) -> Dict[str, str]:
        """Build the final response dictionary."""
        features_display = ", ".join(self.features_list) if self.features_list else "(no features enabled)"
        
        # Determine status display
        if not self.features_list:
            status = f"{self.active_profile.upper()} (no additional features)"
        else:
            status = f"{self.active_profile.upper()}"
        
        # Add features to content if any
        if self.features_list:
            self.profile_content += f"\n\n**Additional Features:** {features_display}"
        
        return {
            "internal_reasoning_profile": self.profile_content,
            "internal_reasoning_features": features_display,
            "internal_reasoning_status": status
        }


class InternalReasoningProfile(VariablesPlugin):
    """Handles loading and managing the Internal Reasoning profile and its features."""
    
    def get_variables(self, file: str, backup_dirs: Optional[List[str]] = None, **kwargs) -> Dict[str, str]:
        """Main entry point for the profile loader."""
        loader = ProfileLoader()
        
        # Initialize and check system control
        if not loader._initialize_system_control():
            return {
                "internal_reasoning_profile": loader.profile_content,
                "internal_reasoning_features": "(feature disabled)",
                "internal_reasoning_status": "⛔ DISABLED"
            }
        
        # Load profile data and content
        loader._load_profile_data()
        loader._load_profile_content(**kwargs)
        
        # Load and append feature content if needed
        if loader.features_list:
            feature_content = loader._load_feature_content(**kwargs)
            if feature_content:
                loader.profile_content += feature_content
        
        return loader.build_response()
