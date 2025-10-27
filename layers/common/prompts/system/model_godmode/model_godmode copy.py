from python.helpers import files
from python.helpers.extension import Extension
from agent import Agent, LoopData
from python.helpers.print_style import PrintStyle
import json


class ModelGodMode(Extension):
    """
    Extension that reads model-specific prompt with agent access.
    Looks for model-specific prompts
    Use this instead of reading the .md file.
    """
    
    def is_godmode_enabled(self) -> bool:
        """Check if godmode is enabled in control.json"""
        control_file = "/a0/tmp/control.json"
        try:
            if files.exists(control_file):
                content = files.read_file(control_file)
                config = json.loads(content)
                return config.get("system_prompt_features", {}).get("godmode", {}).get("enabled", True)
            else:
                # Default to DISABLED if config doesn't exist
                return False
        except Exception as e:
            PrintStyle().error(f"Error reading control.json: {e}")
            # Default to DISABLED on error
            return False
    
    def get_model_prompt(self) -> str:
        """Get the model-specific prompt content"""
        provider = self.agent.config.chat_model.provider
        name = self.agent.config.chat_model.name
        
        # Build path to model-specific prompt file
        # model_file = f"/a0/prompts/common/pliny/model_godmode/{provider}/{name}/{name}.md"
        model_file = f"/a0/prompts/system/model_godmode/{provider}/{name}_godmode.md"
        
        # Read the model-specific prompt file
        if files.exists(model_file):
            return files.read_file(model_file)
        else:
            PrintStyle().warning(f"!GODMODE Unavailable (Model-specific prompt file not found: {model_file})")
        return f"!GODMODE Unavailable (Model-specific prompt file not found: {model_file})"
    
    def get_model_godmode_content(self) -> str:
        """Get the full model_godmode.md content with variables substituted"""
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
        content += f"{model_prompt}\n\n"
        # content += f"Agent Framework follows explicit format final answer to user must be in JSON response tool.\n\n"
        # content += f"!GodMode ON\n\n"
        
        return content
    
    async def execute(self, system_prompt: list[str]=[], loop_data: LoopData = LoopData(), **kwargs):
        """Execute during system prompt building"""
        provider = self.agent.config.chat_model.provider
        name = self.agent.config.chat_model.name
        
        # Check if godmode is enabled
        if not self.is_godmode_enabled():
            PrintStyle().hint(f"!GODMODE DISABLED {provider} {name}")
            return ""
        
        prompt = '\n\n' + self.get_model_godmode_content()
        system_prompt.insert(0, prompt)
        PrintStyle().info(f"✓ !GODMODE ENABLED {provider} {name}")
        return prompt