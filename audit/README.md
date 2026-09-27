# JEV Audit Log

Every sensitive mutation must produce an append-only audit event.

Audit events capture:

- actor and actor type
- action
- project/object/task
- result
- timestamp
- risk
- model/provider
- cost
- approval reference
- rationale
- metadata

Development agents must not be able to edit or delete audit history.

The in-memory store is a contract/reference implementation. JEV Platform will persist the same model in PostgreSQL using append-only access controls.
