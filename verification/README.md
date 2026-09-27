# JEV Verification Engine

JEV does not accept "the agent says it is done" as verification.

A task can be VERIFIED only when required evidence is present.

Core evidence:

- requirement traceability
- CI result
- unit tests
- integration tests
- E2E tests when applicable
- diff review
- backend verification when backend/API is affected
- frontend verification when UI/frontend is affected
- database verification when schema/data is affected

The verification engine returns VERIFIED or FAILED with explicit failure reasons.

A failed result must return the task to corrective work instead of allowing completion.
