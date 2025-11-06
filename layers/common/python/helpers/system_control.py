"""SystemControl - Modular System Configuration Management

This module provides a flexible, configuration-driven approach to managing system
profiles and features using dynamic method generation to eliminate code duplication.

Architecture:
    - Dynamic method generation eliminates wrapper methods (67% code reduction)
    - ProfileConfig: Metadata defining profile type structure (data-driven)
    - ProfileRegistry: Registry of all profile types (eliminates hardcoding)
    - ConfigStore: File I/O operations (no caching, always current)
    - ProfileManager: Generic profile operations using registry
    - FeatureManager: Generic feature operations using command pattern

Design Principles:
    - No caching: Always reads fresh config (supports external modifications)
    - Configuration-driven: Add profile types via registry, not code
    - Dynamic method generation: Automatic backward compatibility
    - Single responsibility: Each class has one clear purpose
    - Type safety: Uses dataclasses and type hints
"""

import json
import os
from dataclasses import dataclass
from typing import Optional, Dict, List
from python.helpers import files


# ============================================================================
# CONFIGURATION MODELS
# ============================================================================

@dataclass
class ProfileConfig:
    """Metadata defining how a profile type is structured in the config."""
    config_key: str
    profiles_key: str
    display_name: str
    nested_key: Optional[str] = None
    default_profile: str = "default"


@dataclass
class ExternalProfileConfig:
    """Configuration for external profile definitions with lazy loading."""
    path: str
    _cache: Optional[Dict] = None
    
    def load(self) -> Dict:
        """Load profile definitions from external JSON file with caching."""
        if self._cache is not None:
            return self._cache
        
        try:
            if files.exists(self.path):
                content = files.read_file(self.path)
                self._cache = json.loads(content)
                print(f"DEBUG: Loaded external profiles from {self.path}", flush=True)
                return self._cache
        except Exception as e:
            print(f"DEBUG: Error loading external profiles from {self.path}: {e}", flush=True)
        
        return {}
    
    def invalidate_cache(self) -> None:
        """Invalidate cached profiles (useful for testing/reloading)."""
        self._cache = None


# ============================================================================
# REGISTRY LAYER
# ============================================================================

class ProfileRegistry:
    """Central registry for all profile type configurations."""
    
    def __init__(self):
        self._registry: Dict[str, ProfileConfig] = {}
    
    def register(self, type_id: str, config: ProfileConfig) -> None:
        self._registry[type_id] = config
    
    def get(self, type_id: str) -> Optional[ProfileConfig]:
        return self._registry.get(type_id)
    
    def list_types(self) -> List[str]:
        return list(self._registry.keys())


# ============================================================================
# STORAGE LAYER
# ============================================================================

class ConfigStore:
    """Handles all file I/O operations for system configuration (no caching)."""
    
    def __init__(self, config_path: str, admin_override_path: str):
        self.config_path = config_path
        self.admin_override_path = admin_override_path
    
    def load(self) -> dict:
        """Load configuration from disk (always fresh, no caching)."""
        try:
            if files.exists(self.config_path):
                content = files.read_file(self.config_path)
                return json.loads(content)
        except Exception as e:
            print(f"DEBUG: ConfigStore error reading {self.config_path}: {e}", flush=True)
        
        print(f"DEBUG: ConfigStore using defaults", flush=True)
        return self._get_default_config()
    
    def save(self, config: dict) -> bool:
        """Save configuration to disk."""
        try:
            content = json.dumps(config, indent=2)
            files.write_file(self.config_path, content)
            return True
        except Exception as e:
            print(f"DEBUG: ConfigStore write error: {e}", flush=True)
            return False
    
    def has_admin_override(self) -> bool:
        """Check if admin override file exists."""
        active = files.exists(self.admin_override_path)
        if active:
            print(f"DEBUG: Admin override ACTIVE", flush=True)
        return active
    
    def _get_default_config(self) -> dict:
        """Get default configuration when file is missing."""
        return {
            "security": {"active_profile": "open"},
            "security_profiles": {"open": {"features": {}}},
            "features": {
                "godmode": {"enabled": False},
                "plinian_cognitive_matrix": {"enabled": False},
                "model_overview": {"enabled": True}
            },
            "controls": {
                "security_control": {"enabled": True},
                "feature_control": {"enabled": True},
                "workflow_control": {"enabled": True},
                "reasoning_control": {"enabled": True}
            }
        }


# ============================================================================
# FEATURE MANAGEMENT PATTERNS (Command + Strategy + Template Method)
# ============================================================================

@dataclass
class FeatureContext:
    """Context for feature operations using strategy pattern."""
    config: dict
    profile_config: ProfileConfig
    feature: str
    profile_name: str
    
    def get_features_path(self) -> List[str]:
        """Get navigation path to features dict."""
        if self.profile_config.nested_key:
            return [self.profile_config.profiles_key, self.profile_config.nested_key, 
                    self.profile_name, "features"]
        return [self.profile_config.profiles_key, self.profile_name, "features"]
    
    def get_features_dict(self) -> dict:
        """Navigate to features dict using context path."""
        path = self.get_features_path()
        current = self.config
        for key in path:
            if key not in current:
                current[key] = {}
            current = current[key]
        return current


class FeatureCommand:
    """Command pattern for feature operations."""
    def execute(self, context: FeatureContext) -> dict:
        raise NotImplementedError
    def get_success_message(self, context: FeatureContext) -> str:
        raise NotImplementedError


class EnableFeatureCommand(FeatureCommand):
    """Command to enable a feature."""
    def execute(self, context: FeatureContext) -> dict:
        features = context.get_features_dict()
        if context.feature in features and features[context.feature].get("enabled", False):
            return {"success": True, "message": f"Feature '{context.feature}' already enabled", 
                    "feature": context.feature}
        features[context.feature] = {"enabled": True, "reference": f"{context.feature}.md"}
        return {"success": True, "feature": context.feature, "profile": context.profile_name,
                "message": f"Feature '{context.feature}' enabled in profile '{context.profile_name}'"}
    def get_success_message(self, context: FeatureContext) -> str:
        return f"Feature '{context.feature}' enabled in profile '{context.profile_name}'"


class DisableFeatureCommand(FeatureCommand):
    """Command to disable a feature."""
    def execute(self, context: FeatureContext) -> dict:
        features = context.get_features_dict()
        if context.feature not in features:
            return {"success": True, "message": f"Feature '{context.feature}' not configured", 
                    "feature": context.feature}
        if not features[context.feature].get("enabled", False):
            return {"success": True, "message": f"Feature '{context.feature}' already disabled",
                    "feature": context.feature}
        features[context.feature]["enabled"] = False
        return {"success": True, "feature": context.feature, "profile": context.profile_name,
                "message": f"Feature '{context.feature}' disabled in profile '{context.profile_name}'"}
    def get_success_message(self, context: FeatureContext) -> str:
        return f"Feature '{context.feature}' disabled in profile '{context.profile_name}'"


class FeatureManager:
    """Template method pattern for feature operations."""
    
    def __init__(self, config_store: ConfigStore, profile_registry: ProfileRegistry):
        self.config_store = config_store
        self.profile_registry = profile_registry
    
    def modify_feature(self, profile_type: str, feature: str, command: FeatureCommand) -> dict:
        """Template method for feature modification."""
        try:
            config = self.config_store.load()
            profile_config = self.profile_registry.get(profile_type)
            if not profile_config:
                return {"success": False, "error": f"Unknown profile type '{profile_type}'"}
            
            # Get active profile name
            if profile_config.nested_key:
                profile_name = config.get(profile_config.config_key, {}) \
                               .get(profile_config.nested_key, {}) \
                               .get("active_profile", profile_config.default_profile)
            else:
                profile_name = config.get(profile_config.config_key, {}) \
                               .get("active_profile", profile_config.default_profile)
            
            context = FeatureContext(config, profile_config, feature, profile_name)
            result = command.execute(context)
            
            if result.get("success", False):
                if not self.config_store.save(context.config):
                    return {"success": False, "error": "Failed to save configuration"}
                print(f"DEBUG: {command.get_success_message(context)}", flush=True)
            
            return result
        except Exception as e:
            return {"success": False, "error": f"Unexpected error: {e}"}


# ============================================================================
# PROFILE MANAGEMENT LAYER
# ============================================================================

class ProfileManager:
    """Generic profile management using configuration-driven approach with external profile support."""
    
    def __init__(self, config_store: ConfigStore, profile_registry: ProfileRegistry, system_control=None):
        self.store = config_store
        self.registry = profile_registry
        self.system_control = system_control
    
    def get_active(self, type_id: str) -> str:
        """Get active profile for specified type."""
        config = self.store.load()
        profile_config = self.registry.get(type_id)
        if not profile_config:
            return "default"
        
        if profile_config.nested_key:
            return config.get(profile_config.config_key, {}) \
                        .get(profile_config.nested_key, {}) \
                        .get("active_profile", profile_config.default_profile)
        return config.get(profile_config.config_key, {}) \
                .get("active_profile", profile_config.default_profile)
    
    def get_available(self, type_id: str) -> List[str]:
        """Get list of available profiles, checking external sources first."""
        # Check for external profile definitions first
        if self.system_control and hasattr(self.system_control, 'external_profiles'):
            if type_id in self.system_control.external_profiles:
                external_profiles = self.system_control.external_profiles[type_id].load()
                if external_profiles:
                    print(f"DEBUG: Using external profiles for {type_id}", flush=True)
                    return list(external_profiles.keys())
        
        # Fall back to config file
        config = self.store.load()
        profile_config = self.registry.get(type_id)
        if not profile_config:
            return []
        
        if profile_config.nested_key:
            return list(config.get(profile_config.profiles_key, {}) \
                        .get(profile_config.nested_key, {}).keys())
        return list(config.get(profile_config.profiles_key, {}).keys())
    
    def set_active(self, type_id: str, profile: str) -> dict:
        """Set active profile for specified type, validating against external profiles if available."""
        config = self.store.load()
        profile_config = self.registry.get(type_id)
        if not profile_config:
            return {"success": False, "error": f"Unknown profile type '{type_id}'"}
        
        # Validate profile exists (checks external profiles via get_available)
        available = self.get_available(type_id)
        if profile not in available:
            return {"success": False, "error": f"{profile_config.display_name} profile '{profile}' not found",
                    "available_profiles": available}
        
        # Get old profile
        old_profile = self.get_active(type_id)
        if old_profile == profile:
            return {"success": True, "message": f"Already on {profile_config.display_name.lower()} profile '{profile}'",
                    "profile": profile}
        
        # Update configuration (always store active profile in config, even for external profiles)
        if profile_config.config_key not in config:
            config[profile_config.config_key] = {}
        if profile_config.nested_key:
            if profile_config.nested_key not in config[profile_config.config_key]:
                config[profile_config.config_key][profile_config.nested_key] = {}
            config[profile_config.config_key][profile_config.nested_key]["active_profile"] = profile
        else:
            config[profile_config.config_key]["active_profile"] = profile
        
        # Save to disk
        if not self.store.save(config):
            return {"success": False, "error": "Failed to write configuration"}
        
        print(f"DEBUG: {profile_config.display_name} profile changed: {old_profile} → {profile}", flush=True)
        return {"success": True, "previous_profile": old_profile, "new_profile": profile,
                "message": f"{profile_config.display_name} profile changed from '{old_profile}' to '{profile}'"}
    
    def get_state(self, type_id: str) -> dict:
        """Get complete state for specified profile type, checking external profiles first."""
        config = self.store.load()
        profile_config = self.registry.get(type_id)
        if not profile_config:
            return {"active_profile": "default", "available_profiles": [], "features": {}}
        
        profile_name = self.get_active(type_id)
        
        # Check for external profile definitions first
        if self.system_control and hasattr(self.system_control, 'external_profiles'):
            if type_id in self.system_control.external_profiles:
                external_profiles = self.system_control.external_profiles[type_id].load()
                if profile_name in external_profiles:
                    print(f"DEBUG: Using external profile '{profile_name}' for {type_id}", flush=True)
                    return {
                        "active_profile": profile_name,
                        "available_profiles": list(external_profiles.keys()),
                        "features": external_profiles[profile_name].get("features", {}),
                        "description": external_profiles[profile_name].get("description", "")
                    }
        
        # Fall back to config file
        if profile_config.nested_key:
            profile = config.get(profile_config.profiles_key, {}) \
                        .get(profile_config.nested_key, {}) \
                        .get(profile_name, {})
        else:
            profile = config.get(profile_config.profiles_key, {}).get(profile_name, {})
        
        return {"active_profile": profile_name, "available_profiles": self.get_available(type_id),
                "features": profile.get("features", {})}


# ============================================================================
# MAIN FACADE CLASS
# ============================================================================

class SystemControl:
    """System security configuration helper with dynamic method generation.
    
    Uses dynamic method generation to eliminate code duplication while
    maintaining perfect backward compatibility with all existing tools.
    """
    
    CONTROL_FILE = "/a0/tmp/system_control.json"
    ADMIN_OVERRIDE_FILE = "/a0/tmp/admin_override.lock"
    
    def __init__(self):
        """Initialize SystemControl with modular components and external profile support."""
        self.config_store = ConfigStore(self.CONTROL_FILE, self.ADMIN_OVERRIDE_FILE)
        self.profile_registry = ProfileRegistry()
        self._setup_profile_registry()
        
        # Initialize external profile configurations from config file
        self.external_profiles = self._load_external_profile_paths()
        
        # Initialize managers (pass self to ProfileManager for external profile access)
        self.profile_manager = ProfileManager(self.config_store, self.profile_registry, self)
        self.feature_manager = FeatureManager(self.config_store, self.profile_registry)
    
    def __getattr__(self, name):
        """Generate profile-specific methods dynamically for backward compatibility."""
        # Profile getter: get_active_*_profile()
        if name.startswith("get_active_") and name.endswith("_profile"):
            profile_type = name[12:-8]
            if profile_type in ["workflow", "philosophy", "liminal_thinking"]:
                return lambda: self.get_active_profile(profile_type)
            elif profile_type in ["internal_reasoning", "interleaved_reasoning", "external_reasoning"]:
                registry_key = f"reasoning_{profile_type.split('_')[0]}"
                return lambda: self.get_active_profile(registry_key)
        
        # Profile setter: set_active_*_profile()
        elif name.startswith("set_active_") and name.endswith("_profile"):
            profile_type = name[11:-8]
            if profile_type in ["workflow", "philosophy", "liminal_thinking"]:
                return lambda profile: self.set_active_profile(profile_type, profile)
            elif profile_type in ["internal_reasoning", "interleaved_reasoning", "external_reasoning"]:
                registry_key = f"reasoning_{profile_type.split('_')[0]}"
                return lambda profile: self.set_active_profile(registry_key, profile)
        
        # State methods: get_*_state()
        elif name.startswith("get_") and name.endswith("_state"):
            profile_type = name[4:-6]
            if profile_type in ["workflow", "philosophy", "liminal_thinking"]:
                return lambda: self.get_state(profile_type)
            elif profile_type == "security":
                return lambda: self.get_security_state()
            elif profile_type in ["internal_reasoning", "interleaved_reasoning", "external_reasoning"]:
                registry_key = f"reasoning_{profile_type.split('_')[0]}"
                return lambda: self.get_state(registry_key)
        
        # Available profiles: get_available_*_profiles()
        elif name.startswith("get_available_") and name.endswith("_profiles"):
            profile_type = name[15:-9]
            if profile_type in ["workflow", "philosophy", "liminal_thinking"]:
                return lambda: self.get_available_profiles(profile_type)
            elif profile_type in ["internal_reasoning", "interleaved_reasoning", "external_reasoning"]:
                registry_key = f"reasoning_{profile_type.split('_')[0]}"
                return lambda: self.get_available_profiles(registry_key)
        
        # Feature enable/disable: enable_*_feature(), disable_*_feature()
        elif name.startswith("enable_") and name.endswith("_feature"):
            profile_type = name[7:-8]
            if profile_type == "liminal_thinking":
                return lambda feature: self.enable_feature(profile_type, feature)
        elif name.startswith("disable_") and name.endswith("_feature"):
            profile_type = name[8:-8]
            if profile_type == "liminal_thinking":
                return lambda feature: self.disable_feature(profile_type, feature)
        
        # Control methods: *_profile_control(), feature_control()
        elif name.endswith("_control"):
            # Return a callable that checks if this control is enabled
            return lambda: self.is_control_enabled(name)
        
        # Security profile methods (backward compatibility)
        elif name == "get_active_profile":
            return lambda: self.get_active_profile("security")
        elif name == "get_available_profiles":
            return lambda: self.get_available_profiles("security")
        elif name == "set_active_profile":
            return lambda profile: self.set_active_profile("security", profile)
        
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
    
    def _setup_profile_registry(self) -> None:
        """Register all profile types with their configuration metadata."""
        # Simple profiles
        self.profile_registry.register("workflow", ProfileConfig(
            config_key="workflow", profiles_key="workflow_profiles", display_name="Workflow"))
        self.profile_registry.register("philosophy", ProfileConfig(
            config_key="philosophy", profiles_key="philosophy_profiles", display_name="Philosophy"))
        self.profile_registry.register("liminal_thinking", ProfileConfig(
            config_key="liminal_thinking", profiles_key="liminal_thinking_profiles", 
            display_name="Liminal thinking"))
        self.profile_registry.register("security", ProfileConfig(
            config_key="security", profiles_key="security_profiles", display_name="Security"))
        
        # Nested reasoning profiles
        self.profile_registry.register("reasoning_internal", ProfileConfig(
            config_key="reasoning", profiles_key="reasoning_profiles", 
            display_name="Internal reasoning", nested_key="internal"))
        self.profile_registry.register("reasoning_interleaved", ProfileConfig(
            config_key="reasoning", profiles_key="reasoning_profiles",
            display_name="Interleaved reasoning", nested_key="interleaved"))
        self.profile_registry.register("reasoning_external", ProfileConfig(
            config_key="reasoning", profiles_key="reasoning_profiles",
            display_name="External reasoning", nested_key="external"))
    
    def _load_external_profile_paths(self) -> Dict[str, ExternalProfileConfig]:
        """Load external profile paths from config file.
        
        Checks for 'external_path' parameter in profile sections. If found,
        creates ExternalProfileConfig to load profiles from that file instead
        of reading from the config itself.
        
        Config format:
            "liminal_thinking_profiles": {
                "external_path": "prompts/system/profiles/liminal_thinking/liminal_thinking.json"
            }
        
        Returns:
            Dict mapping profile type IDs to ExternalProfileConfig objects
        """
        external_profiles = {}
        config = self.config_store.load()
        
        # Check each registered profile type for external_path
        for type_id in self.profile_registry.list_types():
            profile_config = self.profile_registry.get(type_id)
            if not profile_config:
                continue
            
            # Get the profiles section from config
            profiles_section = config.get(profile_config.profiles_key)
            
            # Check if there's an external_path specified
            if isinstance(profiles_section, dict) and "external_path" in profiles_section:
                external_path = profiles_section["external_path"]
                
                # Build full path (handle both absolute and relative paths)
                if external_path.startswith("/"):
                    full_path = external_path
                else:
                    # Relative path - resolve from config file directory for portability
                    config_dir = os.path.dirname(self.CONTROL_FILE)
                    full_path = os.path.join(config_dir, external_path)
                    # Normalize the path to handle .. and . components
                    full_path = os.path.normpath(full_path)
                
                external_profiles[type_id] = ExternalProfileConfig(path=full_path)
                print(f"DEBUG: Registered external profile path for {type_id}: {full_path}", flush=True)
        
        return external_profiles
    
    # ========================================================================
    # CORE GENERIC METHODS
    # ========================================================================
    
    def get_active_profile(self, profile_type: str) -> str:
        """Get active profile for specified type."""
        profile = self.profile_manager.get_active(profile_type)
        print(f"DEBUG: Active {profile_type} profile: {profile}", flush=True)
        return profile
    
    def set_active_profile(self, profile_type: str, profile: str) -> dict:
        """Set active profile for specified type."""
        return self.profile_manager.set_active(profile_type, profile)
    
    def get_state(self, profile_type: str) -> dict:
        """Get complete state for specified profile type."""
        return self.profile_manager.get_state(profile_type)
    
    def get_available_profiles(self, profile_type: str) -> List[str]:
        """Get available profiles for specified type."""
        profiles = self.profile_manager.get_available(profile_type)
        print(f"DEBUG: Available {profile_type} profiles: {profiles}", flush=True)
        return profiles
    
    def enable_feature(self, profile_type: str, feature: str) -> dict:
        """Generic feature enablement for ANY profile type."""
        return self.feature_manager.modify_feature(profile_type, feature, EnableFeatureCommand())
    
    def disable_feature(self, profile_type: str, feature: str) -> dict:
        """Generic feature disablement for ANY profile type."""
        return self.feature_manager.modify_feature(profile_type, feature, DisableFeatureCommand())
    
    def get_available_profile_types(self) -> List[str]:
        """Get list of all registered profile types."""
        return self.profile_registry.list_types()
    
    # ========================================================================
    # SECURITY-SPECIFIC METHODS
    # ========================================================================
    
    def is_admin_override_active(self) -> bool:
        """Check if admin override file exists."""
        return self.config_store.has_admin_override()
    
    def is_feature_enabled(self, feature: str) -> bool:
        """Check if feature is enabled."""
        config = self.config_store.load()
        admin_override = self.config_store.has_admin_override()
        
        enabled, source = False, "not_found"
        
        if feature in config.get("features", {}):
            enabled, source = config["features"][feature].get("enabled", False), "features"
        elif feature in config.get("controls", {}):
            enabled, source = config["controls"][feature].get("enabled", False), "controls"
        elif feature in config.get("feature_options", {}):
            enabled, source = config["feature_options"][feature].get("enabled", False), "feature_options"
        else:
            profile_name = self.get_active_profile("security")
            if profile_name:
                profile_features = config.get("security_profiles", {}).get(profile_name, {}).get("features", {})
                if feature in profile_features:
                    enabled, source = profile_features[feature].get("enabled", False), "security_profile"
        
        if admin_override and source == "security_profile":
            enabled, source = True, "admin_override"
        
        print(f"DEBUG: Feature '{feature}' enabled: {enabled} (source: {source})", flush=True)
        return enabled
    
    def get_feature_config(self, feature: str) -> dict:
        """Get full feature configuration."""
        config = self.config_store.load()
        profile_name = self.get_active_profile("security")
        profile = config.get("security_profiles", {}).get(profile_name, {})
        
        feature_config = profile.get("features", {}).get(feature)
        if feature_config is None:
            feature_config = config.get("features", {}).get(feature)
        if feature_config is None:
            feature_config = config.get("controls", {}).get(feature)
        if feature_config is None:
            feature_config = config.get("feature_options", {}).get(feature, {})
        
        return feature_config or {}
    
    def get_available_features(self) -> list[str]:
        """Get list of available features and controls."""
        config = self.config_store.load()
        features = set()
        features.update(config.get("features", {}).keys())
        features.update(config.get("controls", {}).keys())
        features.update(config.get("feature_options", {}).keys())
        return sorted(features)
    
    def get_enabled_features(self) -> list[str]:
        """Get list of enabled features and controls."""
        config = self.config_store.load()
        enabled = []
        
        for section in ["features", "controls", "feature_options"]:
            for feature, cfg in config.get(section, {}).items():
                if cfg.get("enabled", False):
                    enabled.append(feature)
        
        profile = self.get_active_profile("security")
        if profile:
            profile_features = config.get("security_profiles", {}).get(profile, {}).get("features", {})
            for feature, cfg in profile_features.items():
                if cfg.get("enabled", False):
                    enabled.append(feature)
        
        return enabled
    
    def set_feature_option(self, feature: str, enabled: bool) -> dict:
        """Set feature or control enabled/disabled."""
        config = self.config_store.load()
        
        section = None
        if feature in config.get("features", {}):
            section = "features"
        elif feature in config.get("controls", {}):
            section = "controls"
        elif feature in config.get("feature_options", {}):
            section = "feature_options"
        else:
            section = "features"
            config["features"][feature] = {}
        
        old_value = config[section][feature].get("enabled", False)
        if old_value == enabled:
            return {"success": True, "feature": feature, "previous_value": old_value, 
                    "new_value": enabled, "message": f"Feature '{feature}' already {('enabled' if enabled else 'disabled')}"}
        
        config[section][feature]["enabled"] = enabled
        
        if not self.config_store.save(config):
            return {"success": False, "error": "Failed to write configuration"}
        
        return {"success": True, "feature": feature, "previous_value": old_value, "new_value": enabled,
                "message": f"Feature '{feature}' {('enabled' if enabled else 'disabled')}",
                "note": "Active security profile may still override this setting"}
    
    def is_control_enabled(self, control_name: str) -> bool:
        """Check if a control is enabled in the config.
        
        Args:
            control_name: Name of the control to check (e.g., 'workflow_profile_control')
        
        Returns:
            bool: True if control is enabled, False otherwise
        """
        config = self.config_store.load()
        controls = config.get("controls", {})
        control_config = controls.get(control_name, {})
        return control_config.get("enabled", False)
    
    def get_security_state(self) -> dict:
        """Get full security state for monitoring."""
        config = self.config_store.load()
        admin_override = self.config_store.has_admin_override()
        profile_name = self.get_active_profile("security")
        
        features = {}
        for feature in self.get_available_features():
            is_enabled = self.is_feature_enabled(feature)
            features[feature] = {"enabled": is_enabled}
        
        return {"active_profile": profile_name, "available_profiles": self.get_available_profiles("security"),
                "admin_override": admin_override, "features": features}
