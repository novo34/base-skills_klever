# JEV Management Read Model

The management layer prepares stable data for the future dashboard.

It summarizes:

- project counts and states
- active/blocked/completed work orders
- pending human approvals
- changes requested
- staging state
- monthly project and platform cost

The UI should consume these read models instead of recalculating operational state itself.

This keeps the future dashboard as a control surface over JEV, not as the source of truth.
