from python.helpers import files
from python.helpers.extension import Extension
from agent import Agent, LoopData
from python.helpers.print_style import PrintStyle

# Graceful import - SystemControl is optional
try:
    from python.helpers.system_control import SystemControl
    SYSTEM_CONTROL_AVAILABLE = True
except ImportError:
    SYSTEM_CONTROL_AVAILABLE = False


class ModelGodMode(Extension):
    """
    Extension that reads model-specific prompt with agent access.
    Looks for model-specific prompts
    Use this instead of reading the .md file.
    """
    
    def get_model_prompt(self) -> str:
        """Get the model-specific prompt content"""
        provider = self.agent.config.chat_model.provider
        name = self.agent.config.chat_model.name
        
        # Build path to model-specific prompt file
        model_file = f"/a0/prompts/system/features/model_godmode/{provider}/{name}_godmode.md"
        
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
        content += f"{model_prompt}"
        # content += f"Agent Framework follows explicit format final answer to user must be in JSON response tool.\n\n"
        # content += f"!GodMode ON\n\n"
        
        return content
    
    async def execute(self, system_prompt: list[str]=[], loop_data: LoopData = LoopData(), **kwargs):
        """Execute during system prompt building"""
        provider = self.agent.config.chat_model.provider
        name = self.agent.config.chat_model.name
        prompt = ""
        
        # Check security control if available
        if not SYSTEM_CONTROL_AVAILABLE:
            # Disabled by default if SystemControl not available
            debug = f"# !GODMODE DISABLED - SystemControl not available ({provider} {name})"
            prompt = ""
            PrintStyle().hint(debug)
        else:
            security = SystemControl()
            if not security.is_feature_enabled("godmode"):
                debug = f"# !GODMODE DISABLED - Security profile: {security.get_active_profile()} ({provider} {name})"
                prompt = ""
                PrintStyle().hint(debug)
            else:
                # Enabled - load the full godmode content
                debug = f"# !GODMODE ENABLED - {provider} {name}"
                prompt = self.get_model_godmode_content()
                PrintStyle().info(debug)
        
        # Insert prompt (either disable message or full content)
        prompt_padded = ('\n\n' + prompt + '\n\n') if prompt else ''
        system_prompt.insert(0, prompt_padded)
        return prompt_padded