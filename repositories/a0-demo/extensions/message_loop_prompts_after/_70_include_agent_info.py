from python.helpers.extension import Extension
from agent import LoopData
from python.helpers.system_control import SystemControl

class IncludeAgentInfo(Extension):
    async def execute(self, loop_data: LoopData = LoopData(), **kwargs):
        
        # Get security state
        system = SystemControl()
        security_state = system.get_security_state()
        
        # Extract security variables
        active_profile = security_state.get('active_profile', 'unknown')
        available_profiles = ', '.join(security_state.get('available_profiles', []))
        admin_override = 'ACTIVE' if security_state.get('admin_override', False) else 'inactive'
        
        # Build features summary
        features_list = []
        for feature, info in security_state.get('features', {}).items():
            status = 'ENABLED' if info.get('enabled', False) else 'disabled'
            source = info.get('source', 'unknown')
            features_list.append(f"{feature}={status}({source})")
        features_summary = ', '.join(features_list)
        
        # Get workflow state
        workflow_state = system.get_workflow_state()
        workflow_profile = workflow_state.get('active_profile', 'unknown')
        workflow_profiles_available = ', '.join(workflow_state.get('available_profiles', []))
        
        # Build workflow features summary
        workflow_features_list = []
        for feature, config in workflow_state.get('features', {}).items():
            enabled = config.get('enabled', False)
            status = 'ENABLED' if enabled else 'disabled'
            workflow_features_list.append(f"{feature}={status}")
        workflow_features_summary = ', '.join(workflow_features_list) if workflow_features_list else '(none)'
        
        # read prompt with security and workflow variables
        agent_info_prompt = self.agent.read_prompt(
            "agent.extras.agent_info.md",
            number=self.agent.number,
            profile=self.agent.config.profile or "Default",
            memory_subdir=self.agent.config.memory_subdir,
            knowledge_subdirs=self.agent.config.knowledge_subdirs,
            chat_model_provider=self.agent.config.chat_model.provider,
            chat_model_name=self.agent.config.chat_model.name,
            security_profile=active_profile,
            security_profiles_available=available_profiles,
            security_admin_override=admin_override,
            security_features=features_summary,
            workflow_profile=workflow_profile,
            workflow_profiles_available=workflow_profiles_available,
            workflow_features=workflow_features_summary,
        )

        # add agent info to the prompt
        loop_data.extras_temporary["agent_info"] = agent_info_prompt
