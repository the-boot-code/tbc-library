from datetime import datetime
from python.helpers.extension import Extension
from agent import Agent, LoopData
from python.helpers import files, memory
from python.helpers.print_style import PrintStyle

# Graceful import - SystemControl is optional
try:
    from python.helpers.system_control import SystemControl
    SYSTEM_CONTROL_AVAILABLE = True
except ImportError:
    SYSTEM_CONTROL_AVAILABLE = False


class SystemWorkflowControlPrompt(Extension):
    """
    Extension that inserts system workflow control prompt.
    Loads workflow profile-specific instructions.
    """
    
    async def execute(self, system_prompt: list[str]=[], loop_data: LoopData = LoopData(), **kwargs):
        # Check workflow control if available
        prompt = ""
        
        if not SYSTEM_CONTROL_AVAILABLE:
            # Disabled by default if SystemControl not available
            prompt = "# !WORKFLOW CONTROL DISABLED - SystemControl not available"
            PrintStyle().hint(prompt)
        else:
            system = SystemControl()
            if not system.is_feature_enabled("workflow_control"):
                prompt = f"# !WORKFLOW CONTROL DISABLED - Security profile: {system.get_active_profile()}"
                PrintStyle().hint("!WORKFLOW CONTROL DISABLED - Using default behavior")
            else:
                # Enabled - load the workflow profile
                prompt = read_prompt(self.agent)
                active_profile = system.get_active_workflow_profile()
                PrintStyle().info(f"✓ !WORKFLOW CONTROL ENABLED - Profile: {active_profile}")
        
        # Insert prompt (either disable message or full content)
        prompt_padded = '\n\n\n' + prompt + '\n\n\n'
        system_prompt.insert(0, prompt_padded)

def get_prompt_file(agent: Agent):
    return "/a0/prompts/system/workflow_profile/workflow_profile.md"

def read_prompt(agent: Agent):
    prompt_file = get_prompt_file(agent)
    if files.exists(prompt_file):
        # Pass agent config as kwargs so they're available to workflow_profile.md template
        prompt = agent.read_prompt(
            prompt_file,
            # Agent identity
            agent_number=agent.number,
            agent_name=agent.agent_name,
            agent_profile=agent.config.profile or "default",
            # Chat model config
            chat_model_provider=agent.config.chat_model.provider,
            chat_model_name=agent.config.chat_model.name,
            chat_model_ctx_length=agent.config.chat_model.ctx_length,
            chat_model_vision=agent.config.chat_model.vision,
            # Utility model config
            utility_model_provider=agent.config.utility_model.provider,
            utility_model_name=agent.config.utility_model.name,
            # Memory and knowledge config
            memory_subdir=agent.config.memory_subdir,
            knowledge_subdirs=", ".join(agent.config.knowledge_subdirs),
        )
        return prompt
    else:
        prompt = '# File Skipped: ' + prompt_file
        prompt = prompt + '\n\n(placeholder)'
        return prompt
