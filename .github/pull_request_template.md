## JEV change

JEV-RISK: R1

### Summary

Describe the change and why it is needed.

### Risk declaration

Select the declared risk above using Foundation policy (R0-R4).

CI derives risk from the authoritative PR file list and fails if the declared
value is lower than the derived minimum.

For R4 or changes to the review/security mechanism itself, add this exact line
only after you have inspected the impact:

JEV-INDEPENDENT-REVIEW: acknowledged

### Verification

- [ ] Relevant tests pass
- [ ] No protected-path or rename bypass
- [ ] `validate` passes
- [ ] `independent-review` passes
- [ ] For R4/self-protection changes, the explicit acknowledgement is present
