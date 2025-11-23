"""SystemControl - Flat, Module-Based System Configuration Management

This module provides a simplified, flat approach to managing system profiles and
prompt-includes/system control tools.

Architecture:
    - ConfigStore: File I/O operations (no caching, always current)
    - ProfileManager: Flat profile operations using prompt_modules section

Design Principles:
    - Flat structure: All profiles use prompt_modules section with module names
    - No external profile loading: Features read from profiles.json by profile loaders
    - No caching: Always reads fresh config
    - No nested keys: Reasoning profiles treated like other module-based profiles
    - Single responsibility: Each class has one clear purpose

Profile Storage:
    - Active profiles: Stored in prompt_modules[module_name]["active_profile"]
    - Available profiles & features: Read from profiles.json in profile module directories
    - Security profile: Special case with no module_name, stored in security section
"""

import json
import os
from typing import Dict, List
from python.helpers import files
from python.helpers.print_style import PrintStyle


CONTROL_FILE = "/a0/tmp/system_control.json"
ADMIN_OVERRIDE_FILE = "/a0/tmp/admin_override.lock"


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
                config = json.loads(content)
                return config
            else:
                PrintStyle().warning(f"⚠️ Config file does not exist: {self.config_path}")
        except Exception as e:
            PrintStyle().error(f"❌ ConfigStore error reading {self.config_path}: {e}")

        PrintStyle().warning(f"⚠️ ConfigStore using defaults - config file not found or unreadable")
        return self._get_default_config()
    
    def save(self, config: dict) -> bool:
        """Save configuration to disk."""
        try:
            content = json.dumps(config, indent=2)
            files.write_file(self.config_path, content)
            return True
        except Exception as e:
            PrintStyle().error(f"❌ ConfigStore write error: {e}")
            return False
    
    def has_admin_override(self) -> bool:
        """Check if admin override file exists."""
        active = files.exists(self.admin_override_path)
        if active:
            PrintStyle().warning(f"🚨 Admin override ACTIVE")
        return active
    
    def _get_default_config(self) -> dict:
        """Get default configuration when file is missing."""
        return {
            "security": {"active_profile": "open"},
            # Security profiles gate prompt-includes at profile level; global prompt-includes are separate
            "security_profiles": {"open": {"prompt_includes": {}}},
            # Global prompt-includes
            "prompt_includes": {
                "godmode": {"enabled": False},
                "plinian_cognitive_matrix": {"enabled": False},
                "model_overview": {"enabled": True}
            },
            # Global System Control tools (including prompt_include_control)
            "system_control_tools": {
                "security_profile_control": {"enabled": True},
                "prompt_include_control": {"enabled": True},
                "workflow_profile_control": {"enabled": True},
                "reasoning_profile_control": {"enabled": True},
                "philosophy_profile_control": {"enabled": True},
                "liminal_thinking_profile_control": {"enabled": True}
            }
        }


# ============================================================================
# PROFILE MANAGEMENT LAYER
# ============================================================================

class ProfileManager:
    """Generic profile management using flat, module-based approach.

    This manager intentionally does not know about concrete profile variants.
    For module-based profiles, the profile_module_name string is treated as the
    prompt_modules key. Security is handled as a special case using the
    "security" and "security_profiles" keys.
    """

    def __init__(self, config_store: ConfigStore):
        self.store = config_store

    def _is_security_module(self, profile_module_name: str) -> bool:
        """Return True if the given profile_module_name refers to the security profile."""
        return profile_module_name == "security"

    def get_active(self, profile_module_name: str) -> str:
        """Get active profile for specified profile module.

        For module-based profiles this reads prompt_modules[profile_module_name].active_profile.
        For security it reads security.active_profile.
        """
        config = self.store.load()

        # Security profile uses dedicated config section
        if self._is_security_module(profile_module_name):
            security_cfg = config.get("security", {})
            if isinstance(security_cfg, dict):
                return security_cfg.get("active_profile", "open")
            return "open"

        # Module-based profiles use prompt_modules[profile_module_name]
        prompt_modules = config.get("prompt_modules", {})
        if isinstance(prompt_modules, dict):
            module_section = prompt_modules.get(profile_module_name, {})
            if isinstance(module_section, dict):
                return module_section.get("active_profile", "default")

        return "default"

    def get_available(self, profile_module_name: str) -> List[str]:
        """Get list of available profiles for the given profile module.

        For security, this is derived from the security_profiles section.
        For module-based profiles, availability is determined by profiles.json
        files in the profile modules and is not tracked in system_control.json,
        so this returns an empty list.
        """
        # Security profiles are defined in the config file
        if self._is_security_module(profile_module_name):
            config = self.store.load()
            security_profiles = config.get("security_profiles", {})
            if isinstance(security_profiles, dict):
                return list(security_profiles.keys())
            return []

        # Module-based profile availability is owned by profiles.json loaders
        return []

    def set_active(self, profile_module_name: str, profile: str) -> dict:
        """Set active profile for specified profile module.

        For security, validates against the configured security_profiles. For
        module-based profiles, this simply records the requested profile name
        under prompt_modules[profile_module_name].active_profile and lets the profile
        loaders validate it against profiles.json.
        """
        config = self.store.load()

        # Security profile: validate against known profiles if available
        if self._is_security_module(profile_module_name):
            available = self.get_available(profile_module_name)
            if available and profile not in available:
                return {
                    "success": False,
                    "error": f"Security profile '{profile}' not found",
                    "available_profiles": available,
                }

        # Get old profile
        old_profile = self.get_active(profile_module_name)
        if old_profile == profile:
            label = "security" if self._is_security_module(profile_module_name) else "profile"
            return {
                "success": True,
                "message": f"Already on {label} '{profile}'",
                "profile": profile,
            }

        # Write new active profile
        if self._is_security_module(profile_module_name):
            security_cfg = config.setdefault("security", {})
            if not isinstance(security_cfg, dict):
                security_cfg = {}
            security_cfg["active_profile"] = profile
            config["security"] = security_cfg
        else:
            prompt_modules = config.setdefault("prompt_modules", {})
            if not isinstance(prompt_modules, dict):
                prompt_modules = {}
            module_section = prompt_modules.get(profile_module_name, {})
            if not isinstance(module_section, dict):
                module_section = {}
            module_section["active_profile"] = profile
            prompt_modules[profile_module_name] = module_section
            config["prompt_modules"] = prompt_modules

        # Save to disk
        if not self.store.save(config):
            return {"success": False, "error": "Failed to write configuration"}

        return {
            "success": True,
            "previous_profile": old_profile,
            "new_profile": profile,
            "message": f"Profile changed from '{old_profile}' to '{profile}'",
        }

    def get_state(self, profile_module_name: str) -> dict:
        """Get complete state for specified profile module.

        Features are loaded from profiles.json files by the profile loaders, so
        this method only returns the active profile name and available profile
        ids (when known).
        """
        profile_name = self.get_active(profile_module_name)
        available = self.get_available(profile_module_name)

        return {
            "active_profile": profile_name,
            "available_profiles": available,
            "features": {},  # Features loaded from profiles.json by profile loaders
        }


# ============================================================================
# MAIN FACADE CLASS
# ============================================================================

class SystemControl:
    """System configuration helper for flat, module-based profile management.
    
    Provides clean, explicit methods for profile and prompt-include management.
    All profile control tools use profile module names (e.g., "workflow_profile").
    """
    
    def __init__(self):
        """Initialize SystemControl with modular components."""
        control_file, admin_override_file = self._resolve_control_paths()
        self.config_store = ConfigStore(control_file, admin_override_file)
        # Initialize managers
        self.profile_manager = ProfileManager(self.config_store)
    
    
    def _resolve_control_paths(self) -> tuple[str, str]:
        """Resolve control and admin override paths from environment or defaults."""
        control_file = os.environ.get("SYSTEM_CONTROL_FILE", CONTROL_FILE)
        admin_override = os.environ.get("SYSTEM_CONTROL_OVERRIDE", ADMIN_OVERRIDE_FILE)
        return control_file, admin_override
    
    # ========================================================================
    # CORE GENERIC METHODS
    # ========================================================================
    
    def get_active_profile(self, profile_module_name: str) -> str:
        """Get active profile for specified profile module."""
        profile = self.profile_manager.get_active(profile_module_name)
        return profile
    
    def set_active_profile(self, profile_module_name: str, profile: str) -> dict:
        """Set active profile for specified profile module."""
        return self.profile_manager.set_active(profile_module_name, profile)
    
    def get_state(self, profile_module_name: str) -> dict:
        """Get complete state for specified profile module."""
        return self.profile_manager.get_state(profile_module_name)
    
    def get_available_profiles(self, profile_module_name: str) -> List[str]:
        """Get available profiles for specified profile module."""
        profiles = self.profile_manager.get_available(profile_module_name)
        return profiles
    
    # Note: Feature-level configuration is owned by profile loaders reading
    # profiles.json in each module; SystemControl does not expose feature
    # enable/disable methods.

    def get_available_profile_modules(self) -> List[str]:
        """Get list of all known profile modules (security + prompt_modules keys)."""
        types: set[str] = set()
        # Always include security
        types.add("security")

        # Add any module-based profiles present in prompt_modules
        config = self.config_store.load()
        prompt_modules = config.get("prompt_modules", {})
        if isinstance(prompt_modules, dict):
            types.update(prompt_modules.keys())

        return sorted(types)
    
    def get_profile_choices(self, profile_module_name: str) -> dict:
        """Get available profiles for a profile module.

        The human-friendly display name for a profile module is supplied by the
        calling tool (profile_module_display_name). SystemControl's
        responsibility here is only to surface the available profile names, when
        known.
        """
        available = self.get_available_profiles(profile_module_name)
        return {
            "success": True,
            "profile_module_name": profile_module_name,
            "display_name": profile_module_name,
            "available_profiles": available,
        }
    
    def run_profile_control(
        self,
        profile_module_name: str,
        profile_module_control_key: str,
        profile_module_display_name: str,
        action: str = "",
        **kwargs,
    ) -> dict:
        """Run a generic profile control action for a given profile module.

        This centralizes the behavior used by profile control tools. It handles:
        - Tool gating via profile_control_key
        - get_state: profile state and prompt-includes
        - get_profile: active profile and available profiles
        - set_profile: change active profile with robust change/no-op handling

        Returns a plain dict with 'message' and 'break_loop' keys, suitable for
        wrapping by Tool/Response in the agents layer.
        """

        # Check if tool/control is enabled
        if not self.is_control_enabled(profile_module_control_key):
            return {
                "message": (
                    f"{profile_module_display_name} control tool is disabled by current security profile. "
                    "Admin override required."
                ),
                "break_loop": False,
            }

        # Route to action handlers
        if action == "get_state":
            state = self.get_state(profile_module_name)

            lines = [
                f"=== {profile_module_display_name} Status (SystemControl) ===",
                f"Active {profile_module_display_name}: {state['active_profile']}",
                f"Available {profile_module_display_name}s: {', '.join(state['available_profiles'])}",
                "",
                "Profile prompt includes:",
            ]

            for feature, config in state.get("features", {}).items():
                enabled = config.get("enabled", False)
                status = "ENABLED" if enabled else "disabled"
                lines.append(f"  - {feature}: {status}")

            if not state.get("features"):
                lines.append("  - (No prompt includes defined for this profile)")

            return {"message": "\n".join(lines), "break_loop": False}

        if action == "get_profile":
            profile_name = self.get_active_profile(profile_module_name)
            choices = self.get_profile_choices(profile_module_name)
            available = choices.get("available_profiles", [])

            lines = [
                f"Active {profile_module_display_name}: {profile_name}",
                f"Available Profiles: {', '.join(available)}",
            ]

            return {"message": "\n".join(lines), "break_loop": False}

        if action == "set_profile":
            profile = kwargs.get("profile", "")

            if not profile:
                choices = self.get_profile_choices(profile_module_name)
                available = choices.get("available_profiles", [])
                return {
                    "message": (
                        "Missing 'profile' parameter. Available profiles: "
                        f"{', '.join(available)}"
                    ),
                    "break_loop": False,
                }

            # Attempt to change profile
            result = self.set_active_profile(profile_module_name, profile)

            if not result.get("success", False):
                error = result.get("error", "Unknown error")
                available = result.get("available_profiles", [])
                msg = f"Failed to change {profile_module_display_name.lower()}: {error}"
                if available:
                    msg += f"\nAvailable profiles: {', '.join(available)}"
                return {"message": msg, "break_loop": False}

            # Success - format detailed response, handling both changed and no-op cases
            previous_profile = result.get("previous_profile")
            new_profile = result.get("new_profile")

            if previous_profile is not None and new_profile is not None:
                # Profile actually changed
                lines = [
                    f"✓ {profile_module_display_name} changed: {previous_profile} → {new_profile}",
                    "",
                    "Profile configuration updated. Changes take effect immediately.",
                    "",
                    (
                        f"Note: The new {profile_module_display_name.lower()} prompt will be "
                        "loaded on the next message loop."
                    ),
                ]
            else:
                # No-op success (e.g. already on this profile)
                active = result.get("profile") or self.get_active_profile(profile_module_name)
                message = result.get(
                    "message",
                    f"Already on {profile_module_display_name.lower()} '{active}'",
                )
                lines = [
                    message,
                    "",
                    f"Active {profile_module_display_name}: {active}",
                    "",
                    (
                        f"Note: The {profile_module_display_name.lower()} prompt will be "
                        "loaded on the next message loop."
                    ),
                ]

            # Get new state to show impact
            state = self.get_state(profile_module_name)
            if state.get("features"):
                lines.append("")
                lines.append("Profile prompt includes:")
                for feature, config in state["features"].items():
                    enabled = config.get("enabled", False)
                    status = "ENABLED" if enabled else "DISABLED"
                    lines.append(f"  - {feature}: {status}")

            return {"message": "\n".join(lines), "break_loop": False}

        # Unknown action
        return {
            "message": (
                f"Unknown action '{action}'. Available: get_state, get_profile, set_profile"
            ),
            "break_loop": False,
        }
    
    def get_all_profiles_state(self) -> Dict[str, dict]:
        """Get state for all known profile modules.

        Security state is provided by get_security_state. Other profile modules
        are inferred from the prompt_modules section using their module names
        as type identifiers.
        """
        states: Dict[str, dict] = {}

        # Always include security profile state
        states["security"] = self.get_security_state()

        # Include any module-based profiles present in prompt_modules
        config = self.config_store.load()
        prompt_modules = config.get("prompt_modules", {})
        if isinstance(prompt_modules, dict):
            for profile_module_name in prompt_modules.keys():
                if profile_module_name == "security":
                    # Avoid clobbering the dedicated security entry
                    continue
                states[profile_module_name] = self.get_state(profile_module_name)

        return states

    def get_all_profiles_extras(self) -> dict:
        """Get concise extras for all profile modules for message loop extensions.

        Returns a mapping of profile module names to their active profile and an
        enabled flag (whether the profile module is currently enabled via
        prompt-includes/system_control_tools/security), e.g.:

            {
                "profiles": {
                    "workflow_profile": {
                        "active_profile": "default",
                        "enabled": True,
                    },
                    ...
                }
            }
        """
        profiles: Dict[str, dict] = {}

        for profile_module_name in self.get_available_profile_modules():
            if profile_module_name == "security":
                continue

            state = self.get_state(profile_module_name)
            enabled, _ = self._get_entry_enabled_and_source(profile_module_name)

            profiles[profile_module_name] = {
                "active_profile": state.get("active_profile", "unknown"),
                "enabled": enabled,
            }

        return {"profiles": profiles}
    
    def get_system_summary(self) -> dict:
        """Get a high-level summary of SystemControl state.

        Returns profiles, enabled/available prompt-includes/controls, and admin
        override flag.
        """
        return {
            "profiles": self.get_all_profiles_state(),
            "enabled_prompt_includes_and_controls": self.get_enabled_prompt_includes_and_controls(),
            "available_prompt_includes_and_controls": self.get_available_prompt_includes_and_controls(),
            "admin_override": self.is_admin_override_active(),
        }

    # ========================================================================
    # SECURITY-SPECIFIC METHODS
    # ========================================================================
    
    def is_admin_override_active(self) -> bool:
        """Check if admin override file exists."""
        return self.config_store.has_admin_override()
    
    def _get_entry_enabled_and_source(self, name: str) -> tuple[bool, str]:
        """Internal helper: resolve prompt-include/control enabled flag and its source.

        Source values:
        - 'prompt_includes'       → top-level prompt_includes section
        - 'system_control_tools'  → top-level system_control_tools section
        - 'security_profile'      → active security profile prompt_includes
        - 'admin_override'        → admin override forcing enabled
        - 'not_found'             → entry not defined anywhere
        """
        config = self.config_store.load()
        admin_override = self.config_store.has_admin_override()

        enabled, source = False, "not_found"

        # Global prompt-includes, then system_control_tools, then security-profile prompt-includes
        prompt_includes = config.get("prompt_includes", {})

        if name in prompt_includes:
            enabled = prompt_includes[name].get("enabled", False)
            source = "prompt_includes"
        elif name in config.get("system_control_tools", {}):
            enabled, source = config["system_control_tools"][name].get("enabled", False), "system_control_tools"
        else:
            profile_name = self.get_active_profile("security")
            if profile_name:
                profile_section = config.get("security_profiles", {}).get(profile_name, {})
                profile_includes = profile_section.get("prompt_includes", {})
                if name in profile_includes:
                    enabled = profile_includes[name].get("enabled", False)
                    source = "security_profile"

        if admin_override and source == "security_profile":
            enabled, source = True, "admin_override"

        return enabled, source

    def is_prompt_include_enabled(self, include: str) -> bool:
        """Check if a prompt-include/control entry is enabled."""
        enabled, _ = self._get_entry_enabled_and_source(include)
        return enabled

    def get_prompt_include_source(self, include: str) -> str:
        """Get the configuration source for a prompt-include/control entry."""
        _, source = self._get_entry_enabled_and_source(include)
        return source

    def get_prompt_include_config(self, include: str) -> dict:
        """Get full prompt-include/control configuration.

        Reads security profile 'prompt_includes', then global 'prompt_includes',
        then falls back to system_control_tools for control-tool style entries.
        """
        config = self.config_store.load()
        profile_name = self.get_active_profile("security")

        security_section = config.get("security_profiles", {}).get(profile_name, {})
        entry_config = security_section.get("prompt_includes", {}).get(include)
        if entry_config is None:
            entry_config = config.get("prompt_includes", {}).get(include)
        if entry_config is None:
            entry_config = config.get("system_control_tools", {}).get(include, {})

        return entry_config or {}

    def get_available_prompt_includes_and_controls(self) -> list[str]:
        """Get list of available prompt-includes and system control tools."""
        config = self.config_store.load()
        entries: set[str] = set()
    
        includes_section = config.get("prompt_includes", {})
        entries.update(includes_section.keys())
        entries.update(config.get("system_control_tools", {}).keys())
        return sorted(entries)
    
    def get_enabled_prompt_includes_and_controls(self) -> list[str]:
        """Get list of enabled prompt-includes and system control tools."""
        config = self.config_store.load()
        enabled: list[str] = []
    
        includes_section = config.get("prompt_includes", {})
        for name, cfg in includes_section.items():
            if cfg.get("enabled", False):
                enabled.append(name)
    
        for name, cfg in config.get("system_control_tools", {}).items():
            if cfg.get("enabled", False):
                enabled.append(name)
    
        profile = self.get_active_profile("security")
        if profile:
            profile_section = config.get("security_profiles", {}).get(profile, {})
            profile_includes = profile_section.get("prompt_includes", {})
            for name, cfg in profile_includes.items():
                if cfg.get("enabled", False):
                    enabled.append(name)
        
        return enabled
    
    def set_prompt_include_option(self, name: str, enabled: bool) -> dict:
        """Set a prompt-include/control entry enabled/disabled.

        This operates over the global `prompt_includes` and `system_control_tools`
        sections, creating a new entry under `prompt_includes` if it does not
        yet exist.
        """
        config = self.config_store.load()

        section = None
        if name in config.get("prompt_includes", {}):
            section = "prompt_includes"
        elif name in config.get("system_control_tools", {}):
            section = "system_control_tools"
        else:
            section = "prompt_includes"
            if "prompt_includes" not in config:
                config["prompt_includes"] = {}
            config["prompt_includes"][name] = {}

        old_value = config[section][name].get("enabled", False)
        if old_value == enabled:
            return {
                "success": True,
                "entry": name,
                "previous_value": old_value,
                "new_value": enabled,
                "message": f"Entry '{name}' already {('enabled' if enabled else 'disabled')}",
            }

        config[section][name]["enabled"] = enabled

        if not self.config_store.save(config):
            return {"success": False, "error": "Failed to write configuration"}

        return {
            "success": True,
            "entry": name,
            "previous_value": old_value,
            "new_value": enabled,
            "message": f"Entry '{name}' {('enabled' if enabled else 'disabled')}",
            "note": "Active security profile may still override this setting",
        }
    
    def is_control_enabled(self, control_name: str) -> bool:
        """Check if a control is enabled in the config.
        
        Args:
            control_name: Name of the control to check (e.g., 'workflow_profile_control')
        
        Returns:
            bool: True if control is enabled, False otherwise
        """
        config = self.config_store.load()
        system_control_tools = config.get("system_control_tools", {})
        control_config = system_control_tools.get(control_name, {})
        return control_config.get("enabled", False)
    
    def get_security_state(self) -> dict:
        """Get full security state for monitoring, including prompt-include/control sources."""
        config = self.config_store.load()
        admin_override = self.config_store.has_admin_override()
        profile_name = self.get_active_profile("security")

        entries: dict[str, dict] = {}
        for name in self.get_available_prompt_includes_and_controls():
            enabled, source = self._get_entry_enabled_and_source(name)
            entries[name] = {"enabled": enabled, "source": source}

        return {
            "active_profile": profile_name,
            "available_profiles": self.get_available_profiles("security"),
            "admin_override": admin_override,
            "entries": entries,
        }
