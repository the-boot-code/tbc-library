from python.helpers import files
from python.helpers.extension import Extension
from agent import Agent, LoopData


class TBCPromptExtension(Extension):
    """
    Extension that reads model-specific prompt with agent access.
    Looks for model-specific prompts in /a0/prompts/common/insert_model_init/{provider}/{name}/{name}.md
    Use this from _81_insert_model_init.py instead of reading the .md file.
    """
    
    def get_model_prompt(self) -> str:
        """Get the model-specific prompt content"""
        provider = self.agent.config.chat_model.provider
        name = self.agent.config.chat_model.name
        
        # Build path to model-specific prompt file
        # model_file = f"/a0/prompts/common/insert_model_init/{provider}/{name}/{name}.md"
        model_file = f"/a0/prompts/common/insert_model_init/{provider}/{name}.md"
        
        # Read the model-specific prompt file
        if files.exists(model_file):
            return files.read_file(model_file)
        else:
            return f"(Model-specific prompt file not found: {model_file})"
    
    def get_model_init_content(self) -> str:
        """Get the full model_init.md content with variables substituted"""
        provider = self.agent.config.chat_model.provider
        name = self.agent.config.chat_model.name
        model_prompt = self.get_model_prompt()
        
        # Format the content
        content = ""
        # content += "# insert_model_init.md\n\n"
        # content += "## model info\n"
        # content += f"Chat Model Provider: {provider}\n"
        # content += f"Chat Model Name: {name}\n\n"
        # content += f"prompt: \n\n{model_prompt}"
        content += f"{model_prompt}"
        
        return content
    
    async def execute(self, system_prompt: list[str]=[], loop_data: LoopData = LoopData(), **kwargs):
        """Execute during system prompt building"""
        prompt = '\n\n' + self.get_model_init_content()
        system_prompt.insert(0, prompt)
