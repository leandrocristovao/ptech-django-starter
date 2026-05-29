"""Helpers for loading a local .env file without extra dependencies."""

from __future__ import annotations

import os
from pathlib import Path


def load_env_file(path: Path) -> dict[str, str]:
    """Load KEY=VALUE pairs from *path* into ``os.environ``.

    Existing environment variables win, so shell exports still override the
    local file. Blank lines, comments, and ``export`` prefixes are ignored.
    """

    loaded: dict[str, str] = {}
    if not path.exists():
        return loaded

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        parsed_line = parse_env_line(raw_line)
        if parsed_line is None:
            continue

        key, value = parsed_line
        if key in os.environ:
            continue

        os.environ[key] = value
        loaded[key] = value

    return loaded


def parse_env_line(raw_line: str) -> tuple[str, str] | None:
    """Parse a single .env line.

    Returns ``None`` for blank lines, comments, or malformed entries.
    """

    line = raw_line.strip()
    if not line or line.startswith("#"):
        return None

    if line.startswith("export "):
        line = line[7:].lstrip()

    key, separator, raw_value = line.partition("=")
    if not separator:
        return None

    key = key.strip()
    if not key:
        return None

    return key, parse_env_value(raw_value.strip())


def parse_env_value(raw_value: str) -> str:
    """Parse a .env value, handling quoted strings and inline comments."""

    if not raw_value:
        return ""

    if raw_value[0] in {'"', "'"}:
        return _parse_quoted_value(raw_value)

    return _parse_unquoted_value(raw_value)


def _parse_quoted_value(raw_value: str) -> str:
    quote = raw_value[0]
    parsed: list[str] = []
    escaped = False

    for char in raw_value[1:]:
        if escaped:
            parsed.append(char)
            escaped = False
            continue

        if quote == '"' and char == "\\":
            escaped = True
            continue

        if char == quote:
            return "".join(parsed)

        parsed.append(char)

    return "".join(parsed)


def _parse_unquoted_value(raw_value: str) -> str:
    parsed: list[str] = []

    for index, char in enumerate(raw_value):
        if char == "#" and (index == 0 or raw_value[index - 1].isspace()):
            break
        parsed.append(char)

    return "".join(parsed).strip()
