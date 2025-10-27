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


class TBCPrompt(Extension):

    async def execute(self, system_prompt: list[str]=[], loop_data: LoopData = LoopData(), **kwargs):
        # Check security control if available
        prompt = ""
        
        if not SYSTEM_CONTROL_AVAILABLE:
            # Disabled by default if SystemControl not available
            prompt = "# !OMNI DISABLED - SystemControl not available"
            PrintStyle().hint(prompt)
        else:
            security = SystemControl()
            if not security.is_feature_enabled("omni"):
                prompt = f"# !OMNI DISABLED - Security profile: {security.get_active_profile()}"
                PrintStyle().hint("!OMNI DISABLED - Plinian Cognitive Matrix skipped")
            else:
                # Enabled - load the full prompt
                prompt = read_prompt(self.agent)
                PrintStyle().info("✓ !OMNI ENABLED - Plinian Cognitive Matrix loaded")
        
        # Insert prompt (either disable message or full content)
        prompt_padded = '\n\n\n' + prompt + '\n\n\n'
        system_prompt.insert(0, prompt_padded)

def get_prompt_file(agent: Agent):
    return "/a0/prompts/system/cognitive_core/pliny/plinian_cognitive_matrix.md"

def read_prompt(agent: Agent):
    prompt_file = get_prompt_file(agent)
    if files.exists(prompt_file):
        # Pass agent config and info as kwargs so they're available to model_persona.md template
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
            # chat_model_max_tokens=agent.config.chat_model.max_tokens,
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
