import json
from typing import Any
from python.helpers.files import VariablesPlugin
from python.helpers import files
from python.helpers.print_style import PrintStyle

class ExternalResources(VariablesPlugin):
    def get_variables(self, file: str, backup_dirs: list[str] | None = None, **kwargs) -> dict[str, Any]:
        # Extract agent from kwargs
        agent = kwargs.get('agent')
        # agent_profile = agent.config.profile if agent and agent.config.profile else 'default'
        
        resource_filename = f"merged_post_system_manual.md"
        resource_dir = "/common/prompts/merged"

        def load_prompt(directory: str, found_msg: str, missing_msg: str):
            try:
                content = files.read_prompt_file(
                    resource_filename,
                    _directories=[directory],
                    **kwargs
                )
                return content, found_msg, True
            except FileNotFoundError:
                return missing_msg, missing_msg, False
            except Exception as e:
                error_msg = f"Error loading resource '{resource_filename}' from '{directory}': {e}"
                PrintStyle().error(error_msg)
                error_prompt = f"(Error loading resource: {resource_filename})"
                return error_prompt, error_msg, False

        resource_content, resource_status_msg, resource_success = load_prompt(
            resource_dir,
            f"Loaded resource '{resource_dir}/{resource_filename}'",
            f"Resource not found '{resource_dir}/{resource_filename}'",
        )

        return {
            # "agent_profile": agent_profile,
            # "resource_filename": resource_filename,
            # "resource_dir": resource_dir,
            # "resource_loaded": resource_success,
            # "resource_status": resource_status_msg,
            "resource_content": resource_content,
        }

