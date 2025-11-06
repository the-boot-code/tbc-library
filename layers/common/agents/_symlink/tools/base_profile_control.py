from python.helpers.tool import Tool, Response
from python.helpers.system_control import SystemControl
import json


class BaseProfileControlTool(Tool):
    """
    Base class for profile control tools.
    Provides common functionality for managing different types of profiles.
    """

    # These should be overridden in subclasses
    profile_type = "base"
    available_actions = []

    def __init__(self):
        super().__init__()
        self.system = SystemControl()
        self.action_handlers = {}

    async def execute(self, **kwargs) -> Response:
        """
        Main execution method for the tool.
        Routes to appropriate handler based on action parameter.
        """
        action = kwargs.get("action", "")

        if not action:
            return Response(
                message=f"Missing 'action' parameter. Available actions: {', '.join(self.available_actions)}",
                break_loop=False
            )

        if action not in self.available_actions:
            return Response(
                message=f"Invalid action '{action}'. Available actions: {', '.join(self.available_actions)}",
                break_loop=False
            )

        handler = self.action_handlers.get(action)
        if not handler:
            return Response(
                message=f"No handler found for action '{action}'",
                break_loop=False
            )

        try:
            return await handler(self.system, kwargs)
        except Exception as e:
            return Response(
                message=f"Error executing action '{action}': {str(e)}",
                break_loop=False
            )

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
