from datetime import datetime
from python.helpers.extension import Extension
from agent import Agent, LoopData
from python.helpers import files, memory
from python.helpers.print_style import PrintStyle

# Don't import at module level - do it inside execute() to avoid framework discovering it
import sys
sys.path.insert(0, '/a0/prompts/system/features/model_godmode')


class InsertModelGodMode(Extension):
    """
    Extension that inserts model-specific initialization prompt.
    Uses ModelGodMode from /a0/prompts/system/model_godmode/model_godmode.py
    """

    async def execute(self, system_prompt: list[str]=[], loop_data: LoopData = LoopData(), **kwargs):
        # PrintStyle().info("=== InsertModelGodMode.execute() called ===")
        
        try:
            # Import inside execute() to avoid framework discovering the class
            from model_godmode import ModelGodMode
            # print("DEBUG: BEFORE ModelGodMode.execute()", flush=True)
            
            # Use the ModelGodMode extension and call its execute method
            result = await ModelGodMode(agent=self.agent).execute(system_prompt=system_prompt, loop_data=loop_data, **kwargs)
            
            # print(f"DEBUG: AFTER ModelGodMode.execute() - result type: {type(result)}", flush=True)
            # print(f"DEBUG: result value: {result}", flush=True)
            # print(f"DEBUG: system_prompt has {len(system_prompt)} items", flush=True)
        except ImportError as e:
            PrintStyle().error(f"Failed to import ModelGodMode: {e}")
            return
        except Exception as e:
            print(f"DEBUG: EXCEPTION CAUGHT: {type(e).__name__}: {e}", flush=True)
            import traceback
            traceback.print_exc()
            raise
