# JEV Control Layer

The control layer is the single application-facing entry point for the future dashboard.

The dashboard should send commands to JEV, not directly to GitHub, agents, Docker, staging or model providers.

Examples:

- create a work order
- get project status
- request an audit
- approve/reject/request changes
- retry work
- read dashboard state
- generate a report

This keeps business control centralized and auditable.
