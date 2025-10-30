from datetime import datetime
from python.helpers.extension import Extension
from agent import Agent, LoopData
from python.helpers import files, memory


class TBCPrompt(Extension):

    async def execute(self, system_prompt: list[str]=[], loop_data: LoopData = LoopData(), **kwargs):
        prompt = read_prompt(self.agent)
        prompt_padded = '\n\n\n' + prompt + '\n\n\n'
        system_prompt.append(prompt_padded) # .insert(0, prompt) #.append(prompt)

def get_prompt_file(agent: Agent):
    return "/a0/prompts/system/system_ready.md"

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
        prompt = prompt + '\n\n' + 'System Ready.' + '\n\n'
        return prompt
