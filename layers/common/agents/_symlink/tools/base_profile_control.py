import json
from python.helpers.system_control import SystemControl


class BaseProfileControlTool:
    """
    Base class for profile control tools.
    Provides common functionality for managing different types of profiles.
    """

    # These should be overridden in subclasses
    profile_type = "base"
    available_actions = []

    def __init__(self):
        self.action_handlers = {}

    async def execute(self, **kwargs):
        """
        Main execution method for the tool.
        Routes to appropriate handler based on action parameter.
        """
        action = kwargs.get("action", "")

        if not action:
            return {
                "message": f"Missing 'action' parameter. Available actions: {', '.join(self.available_actions)}",
                "break_loop": False
            }

        if action not in self.available_actions:
            return {
                "message": f"Invalid action '{action}'. Available actions: {', '.join(self.available_actions)}",
                "break_loop": False
            }

        handler = self.action_handlers.get(action)
        if not handler:
            return {
                "message": f"No handler found for action '{action}'",
                "break_loop": False
            }

        try:
            # Instantiate SystemControl and pass to handler
            system = SystemControl()
            result = await handler(system, kwargs)
            return result
        except Exception as e:
            return {
                "message": f"Error executing action '{action}': {str(e)}",
                "break_loop": False
            }

    def _get_available_profiles(self) -> list[str]:
        """
        Get available profiles for this profile type.
        Should be overridden in subclasses.
        """
        return []

    def _validate_json(self, json_str: str) -> dict:
        """Validate and parse JSON string"""
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e}")
