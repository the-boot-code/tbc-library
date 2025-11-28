# scheduler:delete_task

## Problem

Delete the task defined by the given uuid from the system.

## Solution

### Arguments:
* uuid: string - The uuid of the task to run. Can be retrieved for example from "scheduler:tasks_list"

### Usage (execute task with uuid "xyz-123"):
~~~json
{
    "thoughts": [
        "I must delete task xyz-123",
    ],
    "headline": "Removing task from scheduler",
    "tool_name": "scheduler:delete_task",
    "tool_args": {
        "uuid": "xyz-123",
    }
}
~~~
