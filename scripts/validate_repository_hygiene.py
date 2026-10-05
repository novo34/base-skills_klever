from __future__ import annotations

import hashlib
import json
import pathlib
import re
import sys
from datetime import date

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
ALLOWLIST = ROOT / "policies" / "repository-hygiene-allowlist.yaml"

SCAN_ROOTS = (
    ROOT / "agents_runtime",
    ROOT / "scripts",
    ROOT / "skills",
    ROOT / "models",
    ROOT / "schemas",
)
SKIP_DIR_NAMES = {".git", "__pycache__", "node_modules", "vendor", ".venv", "venv"}
TEMP_PATTERNS = (
    re.compile(r"(^|[._-])(tmp|temp|backup|bak|old|copy|debug)([._-]|$)", re.I),
    re.compile(r"\.(tmp|temp|bak|backup|old|orig|log)$", re.I),
)
DUP_EXTENSIONS = {".py", ".php", ".js", ".ts", ".tsx", ".jsx"}
MIN_DUPLICATE_BYTES = 240


def rel(path: pathlib.Path) -> str:
    return path.relative_to(ROOT).as_posix()


def load_allowlist() -> dict[str, dict]:
    data = yaml.safe_load(ALLOWLIST.read_text(encoding="utf-8")) or {}
    entries = data.get("entries") or []
    result: dict[str, dict] = {}
    for item in entries:
        key = item.get("key")
        reason = item.get("reason")
        expires = item.get("expires")
        if not key or not reason or not expires:
            raise ValueError("allowlist entries require key, reason and expires")
        try:
            expiry = date.fromisoformat(str(expires))
        except ValueError as exc:
            raise ValueError(f"invalid allowlist expiry for {key}") from exc
        if expiry < date.today():
            raise ValueError(f"expired allowlist entry: {key}")
        if key in result:
            raise ValueError(f"duplicate allowlist key: {key}")
        result[key] = item
    return result


def iter_files():
    for root in SCAN_ROOTS:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            if any(part in SKIP_DIR_NAMES for part in path.parts):
                continue
            yield path


def main() -> None:
    try:
        allow = load_allowlist()
    except ValueError as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, indent=2))
        sys.exit(1)

    findings: list[dict] = []
    files = tuple(iter_files())

    for path in files:
        name = path.name
        if any(pattern.search(name) for pattern in TEMP_PATTERNS):
            key = f"temporary:{rel(path)}"
            if key not in allow:
                findings.append({
                    "type": "temporary_artifact",
                    "path": rel(path),
                    "key": key,
                })

    hashes: dict[tuple[str, str], list[str]] = {}
    for path in files:
        if path.suffix.lower() not in DUP_EXTENSIONS:
            continue
        content = path.read_bytes()
        if len(content) < MIN_DUPLICATE_BYTES:
            continue
        normalized = b"\n".join(
            line.strip() for line in content.splitlines() if line.strip()
        )
        digest = hashlib.sha256(normalized).hexdigest()
        hashes.setdefault((path.suffix.lower(), digest), []).append(rel(path))

    for (_, digest), paths in sorted(hashes.items()):
        if len(paths) < 2:
            continue
        key = "duplicate:" + digest
        if key not in allow:
            findings.append({
                "type": "exact_duplicate_code",
                "paths": sorted(paths),
                "key": key,
            })

    payload = {
        "status": "PASS" if not findings else "FAIL",
        "findings": findings,
        "allowlist_entries": len(allow),
        "notes": [
            "This gate never deletes files automatically.",
            "Unused dependency checks are delegated to stack-specific tooling when available.",
            "Potential dynamic/reflection-driven dead code requires human/verifier classification.",
        ],
    }
    print(json.dumps(payload, indent=2))

    if findings:
        sys.exit(1)


if __name__ == "__main__":
    main()
