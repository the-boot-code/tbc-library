# scheduler:create_planned_task

## Problem

Create a task within the scheduler system with the type "planned".
The planned type of tasks is being run by a fixed plan, a list of datetimes that you must provide.

## Solution

### Arguments:
* name: str - The name of the task, will also be displayed when listing tasks
* system_prompt: str - The system prompt to be used when executing the task
* prompt: str - The actual prompt with the task definition
* plan: list(iso datetime string) - the list of all execution timestamps. The dates should be in the 24 hour (!) strftime iso format: "%Y-%m-%dT%H:%M:%S"
* attachments: list[str] - Here you can add message attachments, valid are filesystem paths and internet urls
* dedicated_context: bool - if false, then the task will run in the context it was created in. If true, the task will have it's own context. If unspecified then false is assumed. The tasks run in the context they were created in by default.

### Usage:
~~~json
{
    "thoughts": [
        "I need to create a planned task to run tomorrow at 6:25 PM",
        "Today is 2025-04-29 according to system prompt"
    ],
    "headline": "Creating planned task for specific datetime",
    "tool_name": "scheduler:create_planned_task",
    "tool_args": {
        "name": "XXX",
        "system_prompt": "You are a software developer",
        "prompt": "Send the user an email with a greeting using python and smtp. The user's address is: xxx@yyy.zzz",
        "attachments": [],
        "plan": ["2025-04-29T18:25:00"],
        "dedicated_context": false
    }
}
~~~
