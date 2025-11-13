# scheduler:show_task

## Problem

Show task details for scheduler task with the given uuid.

## Solution

### Arguments:
* uuid: string - The uuid of the task to display

### Usage (execute task with uuid "xyz-123"):
~~~json
{
    "thoughts": [
        "I need details of task xxx-yyy-zzz",
    ],
    "headline": "Retrieving task details and configuration",
    "tool_name": "scheduler:show_task",
    "tool_args": {
        "uuid": "xxx-yyy-zzz",
    }
}
~~~
