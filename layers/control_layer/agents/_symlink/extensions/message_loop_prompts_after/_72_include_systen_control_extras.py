from python.helpers.extension import Extension
from agent import LoopData
from control_layer.python.helpers.system_control import SystemControl


# SHOW_SYSTEM_CONTROL_SOURCE = False


class IncludeSystemControlExtras(Extension):

    async def execute(self, loop_data: LoopData = LoopData(), **kwargs):
        system = SystemControl()

        try:
            security_state = system.get_security_state()
            extras = system.get_all_profiles_extras()
            profiles = extras.get("profiles", {})
        except Exception:
            return

        lines: list[str] = []

        lines.append("# System control extras")
        lines.append("")

        security_profile = security_state.get("active_profile", "unknown")
        security_admin_override = (
            "ACTIVE" if security_state.get("admin_override", False) else "inactive"
        )

        lines.append(f"Active security profile: {security_profile}")
        lines.append(f"Admin override: {security_admin_override}")
        lines.append("")

        # Append enabled profile modules in a concise form: profile_module_name:active_profile
        for profile_module_name in sorted(profiles.keys()):
            profile_data = profiles.get(profile_module_name, {})
            if not profile_data.get("enabled", False):
                continue
            active_profile = profile_data.get("active_profile", "unknown")
            lines.append(f"{profile_module_name}:{active_profile}")
            lines.append("")

        loop_data.extras_temporary["system_control_extras"] = "\n".join(lines)
