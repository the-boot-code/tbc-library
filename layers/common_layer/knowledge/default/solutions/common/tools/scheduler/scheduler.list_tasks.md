# scheduler:list_tasks

## Problem

List all tasks present in the system with their 'uuid', 'name', 'type', 'state', 'schedule' and 'next_run'.
All runnable tasks can be listed and filtered here. The arguments are filter fields.

## Solution

### Arguments:
* state: list(str) (Optional) - The state filter, one of "idle", "running", "disabled", "error". To only show tasks in given state.
* type: list(str) (Optional) - The task type filter, one of "adhoc", "planned", "scheduled"
* next_run_within: int (Optional) - The next run of the task must be within this many minutes
* next_run_after: int (Optional) - The next run of the task must be after not less than this many minutes

### Usage:
~~~json
{
    "thoughts": [
        "I must look for planned runnable tasks with name ... and state idle or error",
        "The tasks should run within next 20 minutes"
    ],
    "headline": "Searching for planned runnable tasks to execute soon",
    "tool_name": "scheduler:list_tasks",
    "tool_args": {
        "state": ["idle", "error"],
        "type": ["planned"],
        "next_run_within": 20
    }
}
~~~
