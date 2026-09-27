# JEV Preview / Staging Engine

JEV uses one permanent staging environment per project.

## Branch model

- `main` = production
- `staging` = permanent online validation environment
- `feat/TASK-...` = task-specific development branches

A task is tested on its own branch first. When technically ready, that task is integrated into staging for online validation.

Human approval remains task-specific. JEV must never promote the entire staging branch to main simply because one task was approved.

## Data model

Staging uses its own persistent staging database.

- production database stays isolated
- staging database is persistent
- migrations are tested in staging first
- production data is not automatically copied into staging
- test users/data remain in staging

## Promotion flow

Task branch -> automated checks -> staging -> online/manual test -> human approval -> task-specific production PR -> main

The staging environment itself is not destroyed after every task.
