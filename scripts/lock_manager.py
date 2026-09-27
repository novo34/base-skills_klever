from __future__ import annotations


def acquire_lock(locks: list[dict], resource: str, owner: str, task_id: str, reason: str = "") -> list[dict]:
    for lock in locks:
        if lock.get("resource") == resource and lock.get("status") == "ACTIVE":
            if lock.get("owner") == owner and lock.get("task_id") == task_id:
                return locks
            raise RuntimeError(f"resource already locked: {resource}")

    return locks + [{
        "resource": resource,
        "owner": owner,
        "task_id": task_id,
        "status": "ACTIVE",
        "reason": reason,
    }]


def release_lock(locks: list[dict], resource: str, owner: str, task_id: str) -> list[dict]:
    updated = []
    found = False

    for lock in locks:
        current = dict(lock)
        if (
            current.get("resource") == resource
            and current.get("owner") == owner
            and current.get("task_id") == task_id
            and current.get("status") == "ACTIVE"
        ):
            current["status"] = "RELEASED"
            found = True
        updated.append(current)

    if not found:
        raise RuntimeError(f"active lock not owned by task: {resource}")

    return updated


def assert_write_allowed(locks: list[dict], resource: str, owner: str, task_id: str) -> None:
    for lock in locks:
        if lock.get("resource") == resource and lock.get("status") == "ACTIVE":
            if lock.get("owner") != owner or lock.get("task_id") != task_id:
                raise PermissionError(f"write denied by active lock: {resource}")
