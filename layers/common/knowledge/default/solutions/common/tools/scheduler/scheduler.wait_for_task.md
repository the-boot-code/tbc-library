# scheduler:wait_for_task

## Problem

Wait for the completion of a scheduler task identified by the uuid argument and return the result of last execution of the task.
Attention: You can only wait for tasks running in a different chat context (dedicated). Tasks with dedicated_context=False can not be waited for.

## Solution

### Arguments:
* uuid: string - The uuid of the task to wait for. Can be retrieved for example from "scheduler:tasks_list"

### Usage (wait for task with uuid "xyz-123"):
~~~json
{
    "thoughts": [
        "I need the most current result of the task xyz-123",
    ],
    "headline": "Waiting for task completion and results",
    "tool_name": "scheduler:wait_for_task",
    "tool_args": {
        "uuid": "xyz-123",
    }
}
~~~
