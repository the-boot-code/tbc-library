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
        
        # Try to load model-specific persona file
        agent_identity_path = f"/a0/prompts/tbc/agent_identity/identities/{agent_profile}.md"
        
        if files.exists(agent_identity_path):
            try:
                # Use read_prompt_file for full templating support:
                # - Placeholder replacement with {{variable}} syntax
                # - Include statement processing {{include 'file.md'}}
                # - Nested plugin variable loading
                # - Code fence removal
                agent_identity = files.read_prompt_file(
                    agent_identity_path,
                    _directories=[],  # No fallback dirs needed for absolute path
                    **kwargs  # Pass through all kwargs for nested templating
                )
            except Exception as e:
                PrintStyle().error(f"Error loading model persona '{agent_identity_path}': {e}")
                agent_identity = f"(Error loading agent profile prompt file: {agent_identity_path})"
        else:
            # Default persona if model-specific file doesn't exist
            agent_identity = f"(Agent profile prompt file not found: {agent_identity_path})"
        
        return {
            "agent_identity_path": agent_identity_path,
            "agent_identity": agent_identity
        }
