# Project and work-order flow

JEV now separates permanent project configuration from individual work orders.

A project stores the stable context:

- repository
- main/staging branches
- production/staging URLs
- staging database requirement
- allowed/default models
- monthly budget
- project status

A work order stores the requested piece of work:

- project
- title and description
- priority
- requirement IDs
- optional task budget
- lifecycle state

This enables commands such as "work on Espacore" to resolve the correct repository and staging configuration without repeating technical project data in every request.
