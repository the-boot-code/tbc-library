import json
from python.helpers import files


class SystemControl:
    """System security configuration helper - returns values to extensions and tools"""
    
    CONTROL_FILE = "/a0/tmp/system_control.json"
    ADMIN_OVERRIDE_FILE = "/a0/tmp/admin_override.lock"
    
    def _load_config(self) -> dict:
        """Read system_control.json - simple and direct"""
        try:
            if files.exists(self.CONTROL_FILE):
                content = files.read_file(self.CONTROL_FILE)
                return json.loads(content)
        except Exception as e:
            print(f"DEBUG: SystemControl error reading {self.CONTROL_FILE}: {e}", flush=True)
        
        # Simple defaults if file missing/invalid
        print(f"DEBUG: SystemControl using defaults", flush=True)
        return {
            "security": {"active_profile": "open"},
            "security_profiles": {
                "open": {"features": {}}
            },
            "feature_options": {
                "godmode": {"enabled": False},
                "omni": {"enabled": False}
            }
        }
    
    def is_admin_override_active(self) -> bool:
        """Check if admin override file exists"""
        active = files.exists(self.ADMIN_OVERRIDE_FILE)
        if active:
            print(f"DEBUG: Admin override ACTIVE (file exists)", flush=True)
        return active
    
    def is_feature_enabled(self, feature: str) -> bool:
        """
        Check if feature is enabled.
        Extension decides what to do with result.
        """
        config = self._load_config()
        
        # Admin override bypasses security profile only, not feature config
        admin_override = self.is_admin_override_active()
        
        # If admin override, skip profile and use feature options directly
        if admin_override:
            feature_config = config.get("feature_options", {}).get(feature, {})
            enabled = feature_config.get("enabled", False)
            print(f"DEBUG: Feature '{feature}' ADMIN OVERRIDE (options): {enabled}", flush=True)
            return enabled
        
        # Normal flow: check profile
        profile_name = config.get("security", {}).get("active_profile", "open")
        profile = config.get("security_profiles", {}).get(profile_name, {})
        
        # Check feature in profile
        feature_config = profile.get("features", {}).get(feature)
        if feature_config is not None:
            enabled = feature_config.get("enabled", False)
            print(f"DEBUG: Feature '{feature}' in profile '{profile_name}': {enabled}", flush=True)
            return enabled
        
        # Fall back to feature options
        feature_config = config.get("feature_options", {}).get(feature, {})
        enabled = feature_config.get("enabled", False)
        print(f"DEBUG: Feature '{feature}' using feature options: {enabled}", flush=True)
        return enabled
    
    def get_feature_config(self, feature: str) -> dict:
        """
        Get full feature configuration.
        Extension uses what it needs from the dict.
        """
        config = self._load_config()
        profile_name = config.get("security", {}).get("active_profile", "open")
        profile = config.get("security_profiles", {}).get(profile_name, {})
        
        # Get from profile or feature options
        feature_config = profile.get("features", {}).get(feature)
        if feature_config is None:
            feature_config = config.get("feature_options", {}).get(feature, {})
        
        print(f"DEBUG: Feature '{feature}' config: {feature_config}", flush=True)
        return feature_config or {}
    
    def get_active_profile(self) -> str:
        """Get name of active security profile"""
        config = self._load_config()
        profile = config.get("security", {}).get("active_profile", "open")
        print(f"DEBUG: Active profile: {profile}", flush=True)
        return profile
    
    def get_available_profiles(self) -> list[str]:
        """Get list of available security profiles"""
        config = self._load_config()
        profiles = list(config.get("security_profiles", {}).keys())
        print(f"DEBUG: Available profiles: {profiles}", flush=True)
        return profiles
    
    def get_available_features(self) -> list[str]:
        """Get list of available features"""
        config = self._load_config()
        features = list(config.get("feature_options", {}).keys())
        print(f"DEBUG: Available features: {features}", flush=True)
        return features
    
    def _write_config(self, config: dict) -> bool:
        """Write configuration back to system_control.json"""
        try:
            content = json.dumps(config, indent=2)
            files.write_file(self.CONTROL_FILE, content + "\n")
            print(f"DEBUG: SystemControl wrote to {self.CONTROL_FILE}", flush=True)
            return True
        except Exception as e:
            print(f"DEBUG: SystemControl write error: {e}", flush=True)
            return False
    
    def set_active_profile(self, profile: str) -> dict:
        """
        Change active security profile.
        Returns dict with success status and details.
        """
        config = self._load_config()
        
        # Validate profile exists
        available = config.get("security_profiles", {})
        if profile not in available:
            return {
                "success": False,
                "error": f"Profile '{profile}' not found",
                "available_profiles": list(available.keys())
            }
        
        # Get old profile
        old_profile = config.get("security", {}).get("active_profile", "open")
        
        # No change needed
        if old_profile == profile:
            return {
                "success": True,
                "message": f"Already on profile '{profile}'",
                "profile": profile
            }
        
        # Make change
        config["security"]["active_profile"] = profile
        
        # Write back
        if not self._write_config(config):
            return {
                "success": False,
                "error": "Failed to write configuration"
            }
        
        print(f"DEBUG: Profile changed: {old_profile} → {profile}", flush=True)
        
        return {
            "success": True,
            "previous_profile": old_profile,
            "new_profile": profile,
            "message": f"Profile changed from '{old_profile}' to '{profile}'"
        }
    
    def set_feature_option(self, feature: str, enabled: bool) -> dict:
        """
        Set feature option enabled/disabled.
        Returns dict with success status and details.
        """
        config = self._load_config()
        
        # Validate feature exists
        feature_options = config.get("feature_options", {})
        if feature not in feature_options:
            return {
                "success": False,
                "error": f"Feature '{feature}' not found",
                "available_features": list(feature_options.keys())
            }
        
        # Get old value
        old_value = feature_options[feature].get("enabled", False)
        
        # No change needed
        if old_value == enabled:
            return {
                "success": True,
                "message": f"Feature '{feature}' already {('enabled' if enabled else 'disabled')}",
                "feature": feature,
                "enabled": enabled
            }
        
        # Make change
        config["feature_options"][feature]["enabled"] = enabled
        
        # Write back
        if not self._write_config(config):
            return {
                "success": False,
                "error": "Failed to write configuration"
            }
        
        print(f"DEBUG: Feature '{feature}' changed: {old_value} → {enabled}", flush=True)
        
        return {
            "success": True,
            "feature": feature,
            "previous_value": old_value,
            "new_value": enabled,
            "message": f"Feature '{feature}' {('enabled' if enabled else 'disabled')}",
            "note": "Active security profile may still override this setting"
        }
    
    def get_security_state(self) -> dict:
        """Get full security state for monitoring"""
        config = self._load_config()
        admin_override = self.is_admin_override_active()
        profile_name = self.get_active_profile()
        
        # Get feature states
        features = {}
        for feature in self.get_available_features():
            is_enabled = self.is_feature_enabled(feature)
            
            # Determine source
            profile = config.get("security_profiles", {}).get(profile_name, {})
            if admin_override:
                source = "admin_override"
            elif feature in profile.get("features", {}):
                source = "profile"
            else:
                source = "options"
            
            features[feature] = {
                "enabled": is_enabled,
                "source": source
            }
        
        return {
            "active_profile": profile_name,
            "available_profiles": self.get_available_profiles(),
            "admin_override": admin_override,
            "features": features
        }
    
    # Workflow control methods
    
    def get_active_workflow_profile(self) -> str:
        """Get name of active workflow profile"""
        config = self._load_config()
        profile = config.get("workflow", {}).get("active_profile", "default")
        print(f"DEBUG: Active workflow profile: {profile}", flush=True)
        return profile
    
    def get_available_workflow_profiles(self) -> list[str]:
        """Get list of available workflow profiles"""
        config = self._load_config()
        profiles = list(config.get("workflow_profiles", {}).keys())
        print(f"DEBUG: Available workflow profiles: {profiles}", flush=True)
        return profiles
    
    def set_active_workflow_profile(self, profile: str) -> dict:
        """
        Change active workflow profile.
        Returns dict with success status and details.
        """
        config = self._load_config()
        
        # Validate profile exists
        available = config.get("workflow_profiles", {})
        if profile not in available:
            return {
                "success": False,
                "error": f"Workflow profile '{profile}' not found",
                "available_profiles": list(available.keys())
            }
        
        # Get old profile
        old_profile = config.get("workflow", {}).get("active_profile", "default")
        
        # No change needed
        if old_profile == profile:
            return {
                "success": True,
                "message": f"Already on workflow profile '{profile}'",
                "profile": profile
            }
        
        # Make change
        if "workflow" not in config:
            config["workflow"] = {}
        config["workflow"]["active_profile"] = profile
        
        # Write back
        if not self._write_config(config):
            return {
                "success": False,
                "error": "Failed to write configuration"
            }
        
        print(f"DEBUG: Workflow profile changed: {old_profile} → {profile}", flush=True)
        
        return {
            "success": True,
            "previous_profile": old_profile,
            "new_profile": profile,
            "message": f"Workflow profile changed from '{old_profile}' to '{profile}'"
        }
    
    def get_workflow_state(self) -> dict:
        """Get full workflow state for monitoring"""
        config = self._load_config()
        profile_name = self.get_active_workflow_profile()
        
        # Get workflow profile features
        profile = config.get("workflow_profiles", {}).get(profile_name, {})
        workflow_features = profile.get("features", {})
        
        return {
            "active_profile": profile_name,
            "available_profiles": self.get_available_workflow_profiles(),
            "features": workflow_features
        }
    
    # Reasoning control methods - Internal
    
    def get_active_internal_reasoning_profile(self) -> str:
        """Get name of active internal reasoning profile"""
        config = self._load_config()
        profile = config.get("reasoning", {}).get("internal", {}).get("active_profile", "default")
        print(f"DEBUG: Active internal reasoning profile: {profile}", flush=True)
        return profile
    
    def get_available_internal_reasoning_profiles(self) -> list[str]:
        """Get list of available internal reasoning profiles"""
        config = self._load_config()
        profiles = list(config.get("reasoning_profiles", {}).get("internal", {}).keys())
        print(f"DEBUG: Available internal reasoning profiles: {profiles}", flush=True)
        return profiles
    
    def set_active_internal_reasoning_profile(self, profile: str) -> dict:
        """Change active internal reasoning profile"""
        config = self._load_config()
        
        # Validate profile exists
        available = config.get("reasoning_profiles", {}).get("internal", {})
        if profile not in available:
            return {
                "success": False,
                "error": f"Internal reasoning profile '{profile}' not found",
                "available_profiles": list(available.keys())
            }
        
        # Get old profile
        old_profile = config.get("reasoning", {}).get("internal", {}).get("active_profile", "default")
        
        # No change needed
        if old_profile == profile:
            return {
                "success": True,
                "message": f"Already on internal reasoning profile '{profile}'",
                "profile": profile
            }
        
        # Make change
        if "reasoning" not in config:
            config["reasoning"] = {}
        if "internal" not in config["reasoning"]:
            config["reasoning"]["internal"] = {}
        config["reasoning"]["internal"]["active_profile"] = profile
        
        # Write back
        if not self._write_config(config):
            return {
                "success": False,
                "error": "Failed to write configuration"
            }
        
        print(f"DEBUG: Internal reasoning profile changed: {old_profile} → {profile}", flush=True)
        
        return {
            "success": True,
            "previous_profile": old_profile,
            "new_profile": profile,
            "message": f"Internal reasoning profile changed from '{old_profile}' to '{profile}'"
        }
    
    def get_internal_reasoning_state(self) -> dict:
        """Get full internal reasoning state for monitoring"""
        config = self._load_config()
        profile_name = self.get_active_internal_reasoning_profile()
        
        # Get internal reasoning profile features
        profile = config.get("reasoning_profiles", {}).get("internal", {}).get(profile_name, {})
        reasoning_features = profile.get("features", {})
        
        return {
            "active_profile": profile_name,
            "available_profiles": self.get_available_internal_reasoning_profiles(),
            "features": reasoning_features
        }
    
    # Reasoning control methods - Interleaved
    
    def get_active_interleaved_reasoning_profile(self) -> str:
        """Get name of active interleaved reasoning profile"""
        config = self._load_config()
        profile = config.get("reasoning", {}).get("interleaved", {}).get("active_profile", "default")
        print(f"DEBUG: Active interleaved reasoning profile: {profile}", flush=True)
        return profile
    
    def get_available_interleaved_reasoning_profiles(self) -> list[str]:
        """Get list of available interleaved reasoning profiles"""
        config = self._load_config()
        profiles = list(config.get("reasoning_profiles", {}).get("interleaved", {}).keys())
        print(f"DEBUG: Available interleaved reasoning profiles: {profiles}", flush=True)
        return profiles
    
    def set_active_interleaved_reasoning_profile(self, profile: str) -> dict:
        """Change active interleaved reasoning profile"""
        config = self._load_config()
        
        # Validate profile exists
        available = config.get("reasoning_profiles", {}).get("interleaved", {})
        if profile not in available:
            return {
                "success": False,
                "error": f"Interleaved reasoning profile '{profile}' not found",
                "available_profiles": list(available.keys())
            }
        
        # Get old profile
        old_profile = config.get("reasoning", {}).get("interleaved", {}).get("active_profile", "default")
        
        # No change needed
        if old_profile == profile:
            return {
                "success": True,
                "message": f"Already on interleaved reasoning profile '{profile}'",
                "profile": profile
            }
        
        # Make change
        if "reasoning" not in config:
            config["reasoning"] = {}
        if "interleaved" not in config["reasoning"]:
            config["reasoning"]["interleaved"] = {}
        config["reasoning"]["interleaved"]["active_profile"] = profile
        
        # Write back
        if not self._write_config(config):
            return {
                "success": False,
                "error": "Failed to write configuration"
            }
        
        print(f"DEBUG: Interleaved reasoning profile changed: {old_profile} → {profile}", flush=True)
        
        return {
            "success": True,
            "previous_profile": old_profile,
            "new_profile": profile,
            "message": f"Interleaved reasoning profile changed from '{old_profile}' to '{profile}'"
        }
    
    def get_interleaved_reasoning_state(self) -> dict:
        """Get full interleaved reasoning state for monitoring"""
        config = self._load_config()
        profile_name = self.get_active_interleaved_reasoning_profile()
        
        # Get interleaved reasoning profile features
        profile = config.get("reasoning_profiles", {}).get("interleaved", {}).get(profile_name, {})
        reasoning_features = profile.get("features", {})
        
        return {
            "active_profile": profile_name,
            "available_profiles": self.get_available_interleaved_reasoning_profiles(),
            "features": reasoning_features
        }
    
    # Reasoning control methods - External
    
    def get_active_external_reasoning_profile(self) -> str:
        """Get name of active external reasoning profile"""
        config = self._load_config()
        profile = config.get("reasoning", {}).get("external", {}).get("active_profile", "default")
        print(f"DEBUG: Active external reasoning profile: {profile}", flush=True)
        return profile
    
    def get_available_external_reasoning_profiles(self) -> list[str]:
        """Get list of available external reasoning profiles"""
        config = self._load_config()
        profiles = list(config.get("reasoning_profiles", {}).get("external", {}).keys())
        print(f"DEBUG: Available external reasoning profiles: {profiles}", flush=True)
        return profiles
    
    def set_active_external_reasoning_profile(self, profile: str) -> dict:
        """Change active external reasoning profile"""
        config = self._load_config()
        
        # Validate profile exists
        available = config.get("reasoning_profiles", {}).get("external", {})
        if profile not in available:
            return {
                "success": False,
                "error": f"External reasoning profile '{profile}' not found",
                "available_profiles": list(available.keys())
            }
        
        # Get old profile
        old_profile = config.get("reasoning", {}).get("external", {}).get("active_profile", "default")
        
        # No change needed
        if old_profile == profile:
            return {
                "success": True,
                "message": f"Already on external reasoning profile '{profile}'",
                "profile": profile
            }
        
        # Make change
        if "reasoning" not in config:
            config["reasoning"] = {}
        if "external" not in config["reasoning"]:
            config["reasoning"]["external"] = {}
        config["reasoning"]["external"]["active_profile"] = profile
        
        # Write back
        if not self._write_config(config):
            return {
                "success": False,
                "error": "Failed to write configuration"
            }
        
        print(f"DEBUG: External reasoning profile changed: {old_profile} → {profile}", flush=True)
        
        return {
            "success": True,
            "previous_profile": old_profile,
            "new_profile": profile,
            "message": f"External reasoning profile changed from '{old_profile}' to '{profile}'"
        }
    
    def get_external_reasoning_state(self) -> dict:
        """Get full external reasoning state for monitoring"""
        config = self._load_config()
        profile_name = self.get_active_external_reasoning_profile()
        
        # Get external reasoning profile features
        profile = config.get("reasoning_profiles", {}).get("external", {}).get(profile_name, {})
        reasoning_features = profile.get("features", {})
        
        return {
            "active_profile": profile_name,
            "available_profiles": self.get_available_external_reasoning_profiles(),
            "features": reasoning_features
        }


# FUTURE ENHANCEMENTS (commented placeholders):
#
# def get_lockdown_level(self) -> int:
#     """Get numeric lockdown level (0-100)"""
#     pass
#
# def check_admin_override(self) -> dict:
#     """Get admin override details with expiration, reason, etc"""
#     pass
#
# def clear_cache(self):
#     """Manual cache clear for testing"""
#     pass
#
# Cache implementation, validation, metrics, audit logging...
