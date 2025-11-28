# scheduler:create_scheduled_task

## Problem

Create a task within the scheduler system with the type "scheduled".
The scheduled type of tasks is being run by a cron schedule that you must provide.

## Solution

### Arguments:
* name: str - The name of the task, will also be displayed when listing tasks
* system_prompt: str - The system prompt to be used when executing the task
* prompt: str - The actual prompt with the task definition
* schedule: dict[str,str] - the dict of all cron schedule values. The keys are descriptive: minute, hour, day, month, weekday. The values are cron syntax fields named by the keys.
* attachments: list[str] - Here you can add message attachments, valid are filesystem paths and internet urls
* dedicated_context: bool - if false, then the task will run in the context it was created in. If true, the task will have it's own context. If unspecified then false is assumed. The tasks run in the context they were created in by default.

### Usage:
~~~json
{
    "thoughts": [
        "I need to create a scheduled task that runs every 20 minutes in a separate chat"
    ],
    "headline": "Creating recurring cron-scheduled email task",
    "tool_name": "scheduler:create_scheduled_task",
    "tool_args": {
        "name": "XXX",
        "system_prompt": "You are a software developer",
        "prompt": "Send the user an email with a greeting using python and smtp. The user's address is: xxx@yyy.zzz",
        "attachments": [],
        "schedule": {
            "minute": "*/20",
            "hour": "*",
            "day": "*",
            "month": "*",
            "weekday": "*",
        },
        "dedicated_context": true
    }
}
~~~
