# JEV Development Control Gate / NEXT_TASK

## Purpose

Prevent roadmap drift, silent task skipping and ad-hoc implementation.

The canonical machine-readable backlog is `backlog/jev-master-tasks.yaml`.
For PLATFORM work, **declaration order is execution order**. Dependencies remain
mandatory, but a later task cannot run merely because its own dependencies are
satisfied while an earlier non-terminal task still exists.

## Core rule

At any moment there is exactly one canonical cursor:

```
first PLATFORM task in declaration order
whose status is not DONE or DEFERRED
```

That task is the only candidate that can become NEXT_TASK.

Possible decisions:

- `NEXT_TASK`: first incomplete task is TODO, dependencies are DONE and explicit
  operator authorization is still required.
- `ACTIVE_TASK`: that exact first task is READY, IN_PROGRESS or VERIFYING.
- `BLOCKED`: the first task itself is BLOCKED or one of its dependencies is not DONE.
- `COMPLETE`: every controlled task is terminal.
- `INVALID`: a later/multiple task is active or another invariant is broken.

## No jumping

A request to start PLT-020 while PLT-002 is the current cursor must fail with
`task_jump_forbidden`.

A later task does not become eligible just because it could technically execute
in the dependency DAG.

## New work discovered during development

New work is never implemented immediately.

It must be:

1. captured as a backlog task;
2. analyzed for requirement/roadmap/spec impact;
3. inserted at the correct declaration-order location;
4. linked to dependencies;
5. recorded through the PlanRevision/decision process;
6. validated by CI.

If inserted before the current cursor, it becomes the new NEXT_TASK. This is a
controlled replan, not a silent priority jump.

## Start authorization

Even when the resolver returns NEXT_TASK, work must not start until the operator
authorizes that **exact task id**.

Reference command:

```bash
python scripts/next_task.py --scope PLATFORM
python scripts/next_task.py --scope PLATFORM --authorize-task PLT-002
```

The second command fails if PLT-002 is not the exact canonical NEXT_TASK.

## One active task

At most one PLATFORM task may be:

- READY
- IN_PROGRESS
- VERIFYING

A later task in any of these states while an earlier non-terminal task exists is
invalid and blocks CI.

## DONE is evidence-backed

Starting after the control epoch (`PLT-001`), a PLATFORM task may be marked
DONE only when:

- each acceptance criterion has completion evidence;
- `verified_by` identifies independent verification;
- CI/backlog validators pass.

Example:

```yaml
completion_evidence:
  - "CI run ..."
  - "API evidence ..."
verified_by: "verifier:<id>"
```

The evidence format can evolve in Platform, but absence of evidence may not be
treated as completion.

## Relationship to dependencies

Only `DONE` satisfies a dependency. `DEFERRED` is terminal for cursor
progression but does **not** satisfy another task's dependency.

Therefore deferring required work cannot silently unlock dependent work.

## Relationship to parallel work

Strict sequential control is the default during controlled Platform build-out.
Parallel execution may only be introduced later through an explicit approved
PlanRevision that changes the control policy and proves conflict/evidence safety.
It must not emerge implicitly from the scheduler.

## CI enforcement

CI runs:

- backlog structural validation;
- Development Control Gate validation;
- NEXT_TASK state validation;
- negative unit tests for jumps, blocked tasks, missing authorization and
  incomplete DONE evidence.

This turns the roadmap from guidance into an executable control surface.
