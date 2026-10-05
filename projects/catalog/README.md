# Project catalog

Project files in this directory are configuration records consumed by JEV.

A project may be registered in `SETUP` before its infrastructure is ready.

Before changing a project to `ACTIVE`, configure and verify:

- production repository and `main`
- permanent `staging` branch
- online staging URL
- separate staging database
- deployment/hosting connection
- allowed models and budget policy

JEV refuses to execute work for projects that are not ACTIVE.
