# scheduler:run_task

## Problem

Execute a task manually which is not in "running" state
This can be used to trigger tasks manually.
Normally you should only "run" tasks manually if they are in the "idle" state.
It is also advised to only run "adhoc" tasks manually but every task type can be triggered by this tool.
You can pass input data in text form as the "context" argument. The context will then be prepended to the task prompt when executed. This way you can pass for example result of one task as the input of another task or provide additional information specific to this one task run.

## Solution

### Arguments:
* uuid: string - The uuid of the task to run. Can be retrieved for example from "scheduler:tasks_list"
* context: (Optional) string - The context that will be prepended to the actual task prompt as contextual information.

### Usage (execute task with uuid "xyz-123"):
~~~json
{
    "thoughts": [
        "I must run task xyz-123",
    ],
    "headline": "Manually executing scheduled task",
    "tool_name": "scheduler:run_task",
    "tool_args": {
        "uuid": "xyz-123",
        "context": "This text is useful to execute the task more precisely"
    }
}
~~~
