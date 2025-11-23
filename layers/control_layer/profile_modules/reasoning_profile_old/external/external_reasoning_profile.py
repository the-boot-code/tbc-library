import json
from typing import Any, Dict, List, Optional
from pathlib import Path
from python.helpers.files import VariablesPlugin
from python.helpers import files
from python.helpers.print_style import PrintStyle

class ProfileLoader:
    """Helper class for loading and managing profile data."""
    
    def __init__(self):
        self.system = None
        self.active_profile = "none"
        self.features = {}
        self.features_list = []
        self.profile_content = ""
        self.module_title = "External Reasoning Profile"
        self.module_name = "reasoning_profile"
        self.module_dir = Path(__file__).resolve().parent
        self.debug_enabled = True  # Set to False to disable debug output
        self.feature_info = True  # Set to False to disable feature loading info
        self.profile_info = True  # Set to False to disable profile loading info
    
    def _initialize_system_control(self) -> bool:
        """Initialize SystemControl and check if feature is enabled."""
        try:
            from control_layer.python.helpers.system_control import SystemControl
            self.system = SystemControl()
            # PrintStyle().debug(f"{self.module_name} created: {type(self.system)}") if self.debug_enabled else None
            
            if not self.system.is_control_enabled(f"{self.module_name}_control"):
                disabled_msg = f"⚠️ {self.module_title} Control is currently disabled (Security profile: {self.system.get_active_profile('security')})"
                PrintStyle().hint(disabled_msg)
                self.profile_content = f"# {self.module_title}\n\n{disabled_msg}\n\nPlease contact your system administrator to enable this feature."
                return False
            return True
            
        except ImportError as e:
            error_msg = f"❌ System Error: Could not load SystemControl module: {e}"
            PrintStyle().error(error_msg)
            self.profile_content = f"# {self.module_title}\n\n{error_msg}\n\nPlease ensure the SystemControl module is properly installed and configured."
            return False
    
    def _load_profile_data(self) -> None:
        """Load the active profile and its features."""
        if not self.system:
            return
            
        try:
            self.active_profile = self.system.get_active_profile("reasoning_external")
            state = self.system.get_state("reasoning_external")
            self.features = state.get('features', {})
            self.features_list = [f for f, cfg in self.features.items() if cfg.get('enabled')]
            # PrintStyle().debug(f"{self.module_title} found: {self.active_profile}") if self.profile_info else None
            
        except AttributeError as e:
            if "get_active_profile" in str(e):
                PrintStyle().error(f"❌ {self.module_title} SystemControl method 'get_active_profile' not found. Available methods: {[m for m in dir(self.system) if 'profile' in m.lower()]}")
            raise
        except Exception as e:
            PrintStyle().warning(f"⚠️ {self.module_title} could not load profile settings: {e}")
    
    def _load_profile_content(self, **kwargs) -> None:
        """Load the content of the active profile."""
        profile_path = self.module_dir / "profiles" / f"{self.active_profile}.md"
        
        # print(f"DEBUG: {self.module_title} loading profile: {self.active_profile} from {profile_path}", flush=True) if self.debug_enabled else None
        
        try:
            self.profile_content = files.read_prompt_file(str(profile_path), _directories=[], **kwargs)
            PrintStyle().info(f"{self.module_title} loaded: {self.active_profile}") if self.profile_info else None
            
        except Exception as e:
            error_msg = f"⚠️ {self.module_title} could not load profile '{self.active_profile}': {e}"
            PrintStyle().warning(error_msg)
            self.active_profile = "error"
            self.profile_content = f"# {self.module_title}\n\n{error_msg}"
    
    def _load_feature_content(self, **kwargs) -> str:
        """Load content for all enabled features."""
        if not self.features_list:
            return ""
            
        features_content = []
        
        for feature in self.features_list:
            ref_file = self.features[feature].get('reference', f"{feature}.md")
            feature_path = self.module_dir / "features" / ref_file

            try:
                content = files.read_prompt_file(str(feature_path), _directories=[], **kwargs)
                features_content.append(content)
                if self.feature_info:
                    PrintStyle().standard(f"  Loaded feature: {feature}")
            except FileNotFoundError:
                PrintStyle().warning(f"  Feature file not found: {feature_path}")
            except Exception as e:
                PrintStyle().warning(f"  Could not load feature '{feature}': {e}")
        
        if not features_content:
            return ""
            
        features_display = ", ".join(self.features_list) if self.features_list else "(no features enabled)"
        return f"\n\n## Active Features\n\n**Enabled:** {features_display}\n\n" + "\n\n".join(features_content)
    
    def build_response(self) -> Dict[str, str]:
        """Build the final response dictionary."""
        features_display = ", ".join(self.features_list) if self.features_list else "(no features enabled)"
        
        # Determine status display
        if not self.features_list:
            status = f"{self.active_profile.upper()} (no additional features)"
        else:
            status = f"{self.active_profile.upper()}"
        
        # Features are now added in _load_feature_content
        
        return {
            "profile_content": self.profile_content,
            "features_display": features_display,
            "status": status
        }


class Profile(VariablesPlugin):
    """Handles loading and managing the profile and its features."""
    
    def get_variables(self, file: str, backup_dirs: Optional[List[str]] = None, **kwargs) -> Dict[str, str]:
        """Main entry point for the profile loader."""
        loader = ProfileLoader()
        
        # Initialize and check system control
        if not loader._initialize_system_control():
            return {
                "profile_content": loader.profile_content,
                "features_display": "(feature disabled)",
                "status": "⛔ DISABLED"
            }
        
        # Load profile data and content
        loader._load_profile_data()
        loader._load_profile_content(**kwargs)
        
        # Load and append feature content if needed
        if loader.features_list:
            feature_content = loader._load_feature_content(**kwargs)
            if feature_content:
                loader.profile_content += feature_content
        
        # Return the built response directly since it already has the right variable names
        return loader.build_response()
