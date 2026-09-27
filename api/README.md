# JEV API Contract

The future JEV Platform API is a thin application boundary.

The API:

- authenticates the human user
- builds ActorContext
- validates the request
- maps the endpoint to a ControlCommand
- calls the Control Layer
- returns a stable response
- never bypasses authorization, audit, staging, verification or approval rules

The dashboard must not call GitHub, model providers, Docker or staging infrastructure directly.
