import json
from typing import Any
from pathlib import Path
from python.helpers.files import VariablesPlugin
from python.helpers import files
from python.helpers.print_style import PrintStyle


class PromptInclude(VariablesPlugin):
    def get_variables(self, file: str, backup_dirs: list[str] | None = None, **kwargs) -> dict[str, Any]:
        prompt_include_name = "model_overview"
        prompt_include_content = ""
        module_dir = Path(__file__).resolve().parent

        # Check if model_overview prompt include is enabled via SystemControl
        try:
            from control_layer.python.helpers.system_control import SystemControl
            system = SystemControl()

            if not system.is_prompt_include_enabled(prompt_include_name):
                PrintStyle().hint(
                    f"{prompt_include_name} prompt include DISABLED - Security profile: {system.get_active_profile('security')}"
                )
                return {"prompt_include_content": ""}

        except ImportError:
            PrintStyle().hint(f"SystemControl not available - {prompt_include_name} disabled by default")
            return {"prompt_include_content": ""}
        except Exception as e:
            PrintStyle().hint(f"Error checking {prompt_include_name} include: {e}")
            return {"prompt_include_content": ""}

        # Extract agent from kwargs and get chat model info from it
        agent = kwargs.get("agent")
        if agent and hasattr(agent, "config"):
            chat_model_provider = agent.config.chat_model.provider
            chat_model_name = agent.config.chat_model.name
        else:
            chat_model_provider = "unknown"
            chat_model_name = "unknown"

        provider_dir = module_dir / chat_model_provider
        prompt_include_path = str(provider_dir / f"{chat_model_name}_overview.md")

        try:
            prompt_include_content = files.read_prompt_file(
                prompt_include_path,
                _directories=[],
                **kwargs,
            )
            PrintStyle().info(
                f"✓ {prompt_include_name} prompt include ENABLED - loaded from {prompt_include_path}"
            )
        except FileNotFoundError:
            PrintStyle().hint(f"{prompt_include_name} content file not found: {prompt_include_path}")
            prompt_include_content = f"({prompt_include_name} content file not found: {prompt_include_path})"
        except Exception as e:
            PrintStyle().error(f"Error loading {prompt_include_name} content '{prompt_include_path}': {e}")
            prompt_include_content = f"(Error loading {prompt_include_name} content: {prompt_include_path})"

        return {
            "prompt_include_content": prompt_include_content
        }
