import json
from typing import Any
from python.helpers.files import VariablesPlugin
from python.helpers import files
from python.helpers.print_style import PrintStyle

class AgentIdentity(VariablesPlugin):
    def get_variables(self, file: str, backup_dirs: list[str] | None = None, **kwargs) -> dict[str, Any]:
        # Extract agent from kwargs and get profile from it
        agent = kwargs.get('agent')
        agent_profile = agent.config.profile if agent and agent.config.profile else 'default'
        
        # Load model-specific persona file using prompt-relative path
        agent_identity_filename = f"{agent_profile}.md"
        agent_identity_dir = "prompts/tbc/agent_identity/identities"
        agent_profile_dir = f"agents/{agent_profile}/prompts"
        agent_identity_dir_msg_found = f"## '{agent_profile}' in The Book of Agent Identities\n\n" # directory '{agent_identity_dir}'.\n\n"
        # agent_identity_dir_msg_not_found = f"Agent profile '{agent_profile}' not found in directory '{agent_identity_dir}'."
        agent_identity_dir_msg_not_found = ""
        agent_profile_dir_msg_found = f"## '{agent_profile}' in agent profile prompts directory\n\n" #  '{agent_profile_dir}'\n\n"
        # agent_profile_dir_msg_not_found = f"Agent profile '{agent_profile}' not found in directory '{agent_profile_dir}'."
        agent_profile_dir_msg_not_found = ""
        agent_identity_found_true = "Agent identity located"
        agent_identity_found_false = "Agent identity not found"

        def load_prompt(directory: str, found_msg: str, missing_msg: str):
            try:
                content = files.read_prompt_file(
                    agent_identity_filename,
                    _directories=[directory],
                    **kwargs
                )
                return content, found_msg, True
            except FileNotFoundError:
                return missing_msg, missing_msg, False
            except Exception as e:
                error_msg = f"Error loading agent profile '{agent_profile}' from '{directory}': {e}"
                PrintStyle().error(error_msg)
                error_prompt = f"(Error loading agent profile: {agent_profile})"
                return error_prompt, error_msg, False

        profile_prompt, profile_status_msg, profile_success = load_prompt(
            agent_profile_dir,
            agent_profile_dir_msg_found,
            agent_profile_dir_msg_not_found,
        )
        identity_prompt, identity_status_msg, identity_success = load_prompt(
            agent_identity_dir,
            agent_identity_dir_msg_found,
            agent_identity_dir_msg_not_found,
        )

        if profile_success:
            agent_identity = profile_prompt
            agent_identity_source = "agent profile"
        elif identity_success:
            agent_identity = identity_prompt
            agent_identity_source = "shared"
        else:
            agent_identity = profile_prompt or identity_prompt
            agent_identity_source = "missing"

        if profile_success and identity_success:
            agent_identity_where = " in both the agent profile prompts directory and The Book of Agent Identities"
        elif profile_success:
            agent_identity_where = "" # "in the agent profile prompts directory"
        elif identity_success:
            agent_identity_where = "" # "in The Book of Agent Identities"
        else:
            agent_identity_where = " in either the agent profile prompts directory or The Book of Agent Identities"

        agent_identity_found_msg = agent_identity_found_true if profile_success or identity_success else agent_identity_found_false
        agent_identity_found_where = agent_identity_found_msg + agent_identity_where

        return {
            # "agent_identity": agent_identity,
            # "agent_identity_source": agent_identity_source,
            "agent_profile_prompt_lf": "\n" if profile_success else "",
            "agent_profile_prompt_status": profile_status_msg,
            "agent_profile_prompt": profile_prompt,
            "agent_identity_prompt_lf": "\n" if identity_success else "",
            "agent_identity_prompt_status": identity_status_msg,
            "agent_identity_prompt": identity_prompt,
            # "agent_identity_found": profile_success or identity_success,
            # "agent_identity_found_msg": agent_identity_found_msg,
            # "agent_identity_where": agent_identity_where,
            "agent_identity_found_where": agent_identity_found_where
        }

