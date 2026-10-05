# JEV Budget Enforcement

Budget tracking is not enough. JEV evaluates budget before the next paid action.

Supported limits:

- project monthly limit
- project daily limit
- task limit
- warning threshold
- hard stop or soft warning

When a hard stop would be exceeded, JEV must block the next paid action before calling the model/provider.

The budget service accepts an estimated cost for the next action so it can prevent overspend rather than only reporting it afterwards.
