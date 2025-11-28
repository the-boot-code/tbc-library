# scheduler:find_task_by_name

## Poroblem

List all tasks whose name is matching partially or fully the provided name parameter.

## Solution

### Arguments:
* name: str - The task name to look for

### Usage:
~~~json
{
    "thoughts": [
        "I must look for tasks with name XYZ"
    ],
    "headline": "Finding tasks by name XYZ",
    "tool_name": "scheduler:find_task_by_name",
    "tool_args": {
        "name": "XYZ"
    }
}
~~~
