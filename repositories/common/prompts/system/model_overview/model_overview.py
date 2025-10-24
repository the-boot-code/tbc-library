import json
from typing import Any
from python.helpers.files import VariablesPlugin
from python.helpers import files
from python.helpers.print_style import PrintStyle

class ModelOverview(VariablesPlugin):
    def get_variables(self, file: str, backup_dirs: list[str] | None = None, **kwargs) -> dict[str, Any]:
        # Extract agent config from kwargs (passed from extension)
        chat_model_provider = kwargs.get('chat_model_provider', 'unknown')
        chat_model_name = kwargs.get('chat_model_name', 'unknown')
        
        # Try to load model-specific persona file
        # model_overview_path = f"/a0/prompts/common/model_overview/{chat_model_provider}/{chat_model_name}/{chat_model_name}.md"
        model_overview_path = f"/a0/prompts/system/model_overview/{chat_model_provider}/{chat_model_name}_overview.md"
        
        if files.exists(model_overview_path):
            try:
                model_overview = files.read_file(model_overview_path)
            except Exception as e:
                PrintStyle().error(f"Error loading model persona '{model_overview_path}': {e}")
                model_overview = f"(Error loading model persona file: {model_overview_path})"
        else:
            # Default persona if model-specific file doesn't exist
            model_overview = f"(Model persona file not found: {model_overview_path})"

        
        return {
            "model_overview": model_overview
        }
