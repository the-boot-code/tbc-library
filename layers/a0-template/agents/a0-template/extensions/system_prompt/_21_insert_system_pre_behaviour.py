from datetime import datetime
from python.helpers.extension import Extension
from agent import Agent, LoopData
from python.helpers import files, memory


class InsertPrompt(Extension):

    async def execute(self, system_prompt: list[str]=[], loop_data: LoopData = LoopData(), **kwargs):
        prompt = read_prompt(self.agent)
        prompt_padded = '\n\n' + prompt + '\n\n' if prompt else ''
        system_prompt.insert(0, prompt_padded)

def get_prompt_file(agent: Agent):
    agent_profile=agent.config.profile or "default"
    return "/a0/agents/" + agent_profile + "/prompts/pre_behaviour.md"

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
