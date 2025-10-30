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
        
        # Load model-specific persona file using relative path
        # agent_identity_path = f"tbc/agent_identity/identities/{agent_profile}.md"
        agent_identity_path = f"./identities/{agent_profile}.md"
        
        try:
            # Use read_prompt_file for full templating support:
            # - Placeholder replacement with {{variable}} syntax
            # - Include statement processing {{include 'file.md'}}
            # - Nested plugin variable loading
            # - Code fence removal
            agent_identity = files.read_prompt_file(
                agent_identity_path,
                _directories=[],  # Search in default prompt directories
                **kwargs  # Pass through all kwargs for nested templating
            )
        except Exception as e:
            PrintStyle().error(f"Error loading agent profile '{agent_identity_path}': {e}")
            agent_identity = f"(Error loading agent profile: {agent_profile})"
        else:
            # Default persona if model-specific file doesn't exist
            agent_identity = f"(Agent profile prompt file not found: {agent_identity_path})"
        
        return {
            "agent_identity_path": agent_identity_path,
            "agent_identity": agent_identity
        }
