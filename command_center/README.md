# JEV Command Center

The Command Center converts natural-language instructions into explicit structured intent.

Natural language never executes infrastructure directly.

Flow:

human text -> intent -> project/target resolution -> confirmation when required -> ControlCommand -> authorization -> audit -> execution

Examples:

- Pause Espacore
- Resume Nuvurent
- Audit TASK-423
- Do not spend more than CHF 20 on Espacore

Ambiguous or unsupported commands remain unresolved and must not execute.
