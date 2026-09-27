# JEV Agent Runtimes

Agent contracts define what a role is allowed to do.

Agent runtimes execute that role under JEV control.

The Developer Agent Runtime:

- receives a structured task
- builds a constrained prompt
- calls the Model Gateway
- executes only commands already allowed by the Workspace Engine
- collects validation results
- collects the diff
- returns READY_FOR_REVIEW or FAILED

It does not merge code, bypass verification, or decide production approval.
