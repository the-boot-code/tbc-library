# scheduler:create_adhoc_task

## Problem

Create a task within the scheduler system with the type "adhoc".
The adhoc type of tasks is being run manually by "scheduler:run_task" tool or by the user via ui.

## Solution

### Arguments:
* name: str - The name of the task, will also be displayed when listing tasks
* system_prompt: str - The system prompt to be used when executing the task
* prompt: str - The actual prompt with the task definition
* attachments: list[str] - Here you can add message attachments, valid are filesystem paths and internet urls
* dedicated_context: bool - if false, then the task will run in the context it was created in. If true, the task will have it's own context. If unspecified then false is assumed. The tasks run in the context they were created in by default.

### Usage:
~~~json
{
    "thoughts": [
        "I need to create an adhoc task that can be run manually when needed"
    ],
    "headline": "Creating on-demand email task",
    "tool_name": "scheduler:create_adhoc_task",
    "tool_args": {
        "name": "XXX",
        "system_prompt": "You are a software developer",
        "prompt": "Send the user an email with a greeting using python and smtp. The user's address is: xxx@yyy.zzz",
        "attachments": [],
        "dedicated_context": false
    }
}
~~~
