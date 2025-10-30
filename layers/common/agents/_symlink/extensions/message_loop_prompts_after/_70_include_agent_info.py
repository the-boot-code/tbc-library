from python.helpers.extension import Extension
from agent import LoopData

class IncludeAgentInfo(Extension):
    """Extension that includes agent configuration info in message loop.
    
    All data extraction logic moved to AgentInfo plugin for clean separation of concerns.
    Plugin handles: agent config, SystemControl queries, feature summaries.
    Extension only: reads prompt and stores result.
    """
    
    async def execute(self, loop_data: LoopData = LoopData(), **kwargs):
        # Read prompt - plugin handles all SystemControl logic and data extraction
        agent_info_prompt = self.agent.read_prompt(
            "agent.extras.agent_info.md",
            agent=self.agent,  # Plugin extracts everything it needs from agent object
        )

        # Add agent info to the prompt
        loop_data.extras_temporary["agent_info"] = agent_info_prompt
