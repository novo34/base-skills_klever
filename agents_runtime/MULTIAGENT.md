# JEV Multiagent Coordination

Multiagent execution is coordinated by JEV, not by the models themselves.

Core rules:

- each role has an explicit assignment
- dependencies are declared
- writable resources may be locked
- conflicting writable locks block parallel assignment
- Developer and Verifier must be distinct roles
- Verifier does not repair the code it reviews
- Integrator evaluates handoffs and gates
- VERIFIED is not enough for production merge
- human approval remains required before READY_TO_MERGE
