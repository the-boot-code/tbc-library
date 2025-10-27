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
        
        # Get reasoning states
        internal_state = system.get_internal_reasoning_state()
        internal_profile = internal_state.get('active_profile', 'unknown')
        
        interleaved_state = system.get_interleaved_reasoning_state()
        interleaved_profile = interleaved_state.get('active_profile', 'unknown')
        
        external_state = system.get_external_reasoning_state()
        external_profile = external_state.get('active_profile', 'unknown')
        
        # Build reasoning features summaries
        internal_features_list = []
        for feature, config in internal_state.get('features', {}).items():
            enabled = config.get('enabled', False)
            status = 'ENABLED' if enabled else 'disabled'
            internal_features_list.append(f"{feature}={status}")
        internal_features_summary = ', '.join(internal_features_list) if internal_features_list else '(none)'
        
        interleaved_features_list = []
        for feature, config in interleaved_state.get('features', {}).items():
            enabled = config.get('enabled', False)
            status = 'ENABLED' if enabled else 'disabled'
            interleaved_features_list.append(f"{feature}={status}")
        interleaved_features_summary = ', '.join(interleaved_features_list) if interleaved_features_list else '(none)'
        
        external_features_list = []
        for feature, config in external_state.get('features', {}).items():
            enabled = config.get('enabled', False)
            status = 'ENABLED' if enabled else 'disabled'
            external_features_list.append(f"{feature}={status}")
        external_features_summary = ', '.join(external_features_list) if external_features_list else '(none)'
        
        # read prompt with security, workflow, and reasoning variables
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
            internal_reasoning_profile=internal_profile,
            internal_reasoning_features=internal_features_summary,
            interleaved_reasoning_profile=interleaved_profile,
            interleaved_reasoning_features=interleaved_features_summary,
            external_reasoning_profile=external_profile,
            external_reasoning_features=external_features_summary,
        )

        # add agent info to the prompt
        loop_data.extras_temporary["agent_info"] = agent_info_prompt
