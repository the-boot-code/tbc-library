from typing import Any
from python.helpers.files import VariablesPlugin
from python.helpers import files
from python.helpers.print_style import PrintStyle

class AgentInfo(VariablesPlugin):
    def get_variables(self, file: str, backup_dirs: list[str] | None = None, **kwargs) -> dict[str, Any]:
        """
        Plugin that extracts all agent info including security, workflow, and reasoning states.
        Moves logic from extension layer to plugin layer where it belongs.
        """
        # Extract agent from kwargs
        agent = kwargs.get('agent')
        if not agent:
            PrintStyle().warning("AgentInfo plugin: No agent object provided in kwargs")
            return self._get_empty_variables()
        
        try:
            from python.helpers.system_control import SystemControl
            system = SystemControl()
            
            # Get security state
            security_state = system.get_security_state()
            active_security_profile = security_state.get('active_profile', 'unknown')
            security_admin_override = 'ACTIVE' if security_state.get('admin_override', False) else 'inactive'
            security_features = self._build_features_summary(security_state.get('features', {}), include_source=True)
            
            # Get workflow state
            workflow_state = system.get_workflow_state()
            workflow_profile = workflow_state.get('active_profile', 'unknown')
            workflow_features = self._build_features_summary(workflow_state.get('features', {}))
            
            # Get reasoning states
            internal_state = system.get_internal_reasoning_state()
            internal_profile = internal_state.get('active_profile', 'unknown')
            internal_features = self._build_features_summary(internal_state.get('features', {}))
            
            interleaved_state = system.get_interleaved_reasoning_state()
            interleaved_profile = interleaved_state.get('active_profile', 'unknown')
            interleaved_features = self._build_features_summary(interleaved_state.get('features', {}))
            
            external_state = system.get_external_reasoning_state()
            external_profile = external_state.get('active_profile', 'unknown')
            external_features = self._build_features_summary(external_state.get('features', {}))
            
            # Get philosophy state
            philosophy_state = system.get_philosophy_state()
            philosophy_profile = philosophy_state.get('active_profile', 'unknown')
            philosophy_features_summary = self._build_features_summary(philosophy_state.get('features', {}))
            
            # Get liminal thinking state
            liminal_state = system.get_liminal_thinking_state()
            liminal_profile = liminal_state.get('active_profile', 'unknown')
            liminal_features_summary = self._build_features_summary(liminal_state.get('features', {}))
            
        except ImportError:
            PrintStyle().hint("SystemControl not available - using default agent info")
            return self._get_default_variables(agent)
        except Exception as e:
            PrintStyle().error(f"Error getting agent info: {e}")
            return self._get_default_variables(agent)
        
        # Return all variables for template
        return {
            # Basic agent info
            "number": agent.number,
            "profile": agent.config.profile or "default",
            "memory_subdir": agent.config.memory_subdir,
            "knowledge_subdirs": ", ".join(agent.config.knowledge_subdirs),
            "chat_model_provider": agent.config.chat_model.provider,
            "chat_model_name": agent.config.chat_model.name,
            # Security info
            "security_profile": active_security_profile,
            "security_admin_override": security_admin_override,
            "security_features": security_features,
            # Workflow info
            "workflow_profile": workflow_profile,
            "workflow_features": workflow_features,
            # Reasoning info
            "internal_reasoning_profile": internal_profile,
            "internal_reasoning_features": internal_features,
            "interleaved_reasoning_profile": interleaved_profile,
            "interleaved_reasoning_features": interleaved_features,
            "external_reasoning_profile": external_profile,
            "external_reasoning_features": external_features,
            # Philosophy info
            "philosophy_profile": philosophy_profile,
            "philosophy_features": philosophy_features_summary,
            # Liminal thinking info
            "liminal_thinking_profile": liminal_profile,
            "liminal_thinking_features": liminal_features_summary,
        }
    
    def _build_features_summary(self, features: dict, include_source: bool = False) -> str:
        """Helper to build feature summary string"""
        if not features:
            return '(none)'
        
        features_list = []
        for feature, config in features.items():
            enabled = config.get('enabled', False)
            status = 'ENABLED' if enabled else 'disabled'
            
            if include_source:
                source = config.get('source', 'unknown')
                features_list.append(f"{feature}={status}({source})")
            else:
                features_list.append(f"{feature}={status}")
        
        return ', '.join(features_list) if features_list else '(none)'
    
    def _get_empty_variables(self) -> dict[str, Any]:
        """Return empty/placeholder variables"""
        return {
            "number": "?",
            "profile": "unknown",
            "memory_subdir": "unknown",
            "knowledge_subdirs": "unknown",
            "chat_model_provider": "unknown",
            "chat_model_name": "unknown",
            "security_profile": "unknown",
            "security_admin_override": "unknown",
            "security_features": "(none)",
            "workflow_profile": "unknown",
            "workflow_features": "(none)",
            "internal_reasoning_profile": "unknown",
            "internal_reasoning_features": "(none)",
            "interleaved_reasoning_profile": "unknown",
            "interleaved_reasoning_features": "(none)",
            "external_reasoning_profile": "unknown",
            "external_reasoning_features": "(none)",
            "philosophy_profile": "unknown",
            "philosophy_features": "(none)",
            "liminal_thinking_profile": "unknown",
            "liminal_thinking_features": "(none)",
        }
    
    def _get_default_variables(self, agent) -> dict[str, Any]:
        """Return basic agent info without SystemControl"""
        return {
            "number": agent.number,
            "profile": agent.config.profile or "default",
            "memory_subdir": agent.config.memory_subdir,
            "knowledge_subdirs": ", ".join(agent.config.knowledge_subdirs),
            "chat_model_provider": agent.config.chat_model.provider,
            "chat_model_name": agent.config.chat_model.name,
            "security_profile": "(SystemControl unavailable)",
            "security_admin_override": "unknown",
            "security_features": "(none)",
            "workflow_profile": "(SystemControl unavailable)",
            "workflow_features": "(none)",
            "internal_reasoning_profile": "(SystemControl unavailable)",
            "internal_reasoning_features": "(none)",
            "interleaved_reasoning_profile": "(SystemControl unavailable)",
            "interleaved_reasoning_features": "(none)",
            "external_reasoning_profile": "(SystemControl unavailable)",
            "external_reasoning_features": "(none)",
            "philosophy_profile": "(SystemControl unavailable)",
            "philosophy_features": "(none)",
            "liminal_thinking_profile": "(SystemControl unavailable)",
            "liminal_thinking_features": "(none)",
        }
