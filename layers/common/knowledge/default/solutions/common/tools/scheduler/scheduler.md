# Scheduler

## Problem

How to use the task schedular subsystem

## solution

### Task Scheduler Subsystem:
The task scheduler is a part of agent-zero enabling the system to execute
arbitrary tasks defined by a "system prompt" and "user prompt".

When the task is executed the prompts are being run in the background in a context
conversation with the goal of completing the task described in the prompts.

Dedicated context means the task will run in it's own chat. If task is created without the
dedicated_context flag then the task will run in the chat it was created in including entire history.

There are manual and automatically executed tasks.
Automatic execution happens by a schedule defined when creating the task.

Tasks are run asynchronously. If you need to wait for a running task's completion or need the result of the last task run, use the scheduler:wait_for_task tool. It will wait for the task completion in case the task is currently running and will provide the result of the last execution.

#### Important instructions
When a task is scheduled or planned, do not manually run it, if you have no more tasks, respond to user.
Be careful not to create recursive prompt, do not send a message that would make the agent schedule more tasks, no need to mention the interval in message, just the objective.
!!! When the user asks you to execute a task, first check if the task already exists and do not create a new task for execution. Execute the existing task instead. If the task in question does not exist ask the user what action to take. Never create tasks if asked to execute a task.

#### Types of scheduler tasks
There are 3 types of scheduler tasks:

##### Scheduled - type="scheduled"
This type of task is run by a recurring schedule defined in the crontab syntax with 5 fields (ex. */5 * * * * means every 5 minutes).
It is recurring and started automatically when the crontab syntax requires next execution..

##### Planned - type="planned"
This type of task is run by a linear schedule defined as discrete datetimes of the upcoming executions.
It is  started automatically when a scheduled time elapses.

##### AdHoc - type="adhoc"
This type of task is run manually and does not follow any schedule. It can be run explicitly by "scheduler:run_task" agent tool or by the user in the UI.

#### Task Scheduler Tools:

Refer to the individual solutions for tool documentation and detailed usage instructions:

reference solution `scheduler:list_tasks`
reference solution `scheduler:find_task_by_name`
reference solution `scheduler:show_task`
reference solution `scheduler:run_task`
reference solution `scheduler:delete_task`
reference solution `scheduler:create_scheduled_task`
reference solution `scheduler:create_adhoc_task`
reference solution `scheduler:create_planned_task`
reference solution `scheduler:wait_for_task`
