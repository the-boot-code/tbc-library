from datetime import datetime
from python.helpers.extension import Extension
from agent import Agent, LoopData
from python.helpers import files, memory

# this is a symbolic link to symlink/agents/symlink/extensions/system_prompt/
# ln -s ../../../../../symlink/agents/symlink/extensions/system_prompt/_11_insert_system_pre_system_manual.py

class InsertPrompt(Extension):

    async def execute(self, system_prompt: list[str]=[], loop_data: LoopData = LoopData(), **kwargs):
        prompt = read_prompt(self.agent)
        prompt_padded = '\n\n' + prompt + '\n\n' if prompt else ''
        system_prompt.insert(0, prompt_padded)

def get_prompt_file(agent: Agent):
    agent_profile=agent.config.profile or "default"
    return "/a0/agents/" + agent_profile + "/prompts/pre_system_manual.md"

def read_prompt(agent: Agent):
    prompt_file = get_prompt_file(agent)
    if files.exists(prompt_file):
        # Pass agent object for plugin/template access
        prompt = agent.read_prompt(
            prompt_file,
            agent=agent,  # Plugins extract what they need from agent object
        )
        return prompt
    else:
        prompt = '# File Skipped: ' + prompt_file
        prompt = prompt + '\n\n(placeholder)'
        return prompt
