# JEV Workspace Engine

Every implementation task gets its own isolated workspace.

The intended flow is:

Task -> create isolated workspace -> clone task branch -> install dependencies ->
execute only allowed commands -> run tests -> collect diff -> destroy workspace

Key rules:

- Never work directly on main/master.
- One writable workspace per task execution.
- Commands are allow-listed.
- Production secrets are not mounted in developer workspaces.
- Secrets are cleared when the workspace is destroyed.
- The transport can be Docker or a VM without changing JEV policy.
