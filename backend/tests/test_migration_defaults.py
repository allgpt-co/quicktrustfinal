"""Regression checks for Alembic DDL that must work on PostgreSQL."""

from __future__ import annotations

import ast
from pathlib import Path

MIGRATION_DIR = Path(__file__).resolve().parents[1] / "alembic" / "versions"


def _is_sa_boolean(node: ast.AST) -> bool:
    return (
        isinstance(node, ast.Attribute)
        and node.attr == "Boolean"
        and isinstance(node.value, ast.Name)
        and node.value.id == "sa"
    )


def _literal_string(node: ast.AST) -> str | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    return None


def _numeric_boolean_server_default(node: ast.AST) -> bool:
    literal = _literal_string(node)
    if literal in {"0", "1"}:
        return True

    if isinstance(node, ast.Call):
        func = node.func
        is_sa_text = (
            isinstance(func, ast.Attribute)
            and func.attr == "text"
            and isinstance(func.value, ast.Name)
            and func.value.id == "sa"
        )
        if is_sa_text and node.args:
            return _literal_string(node.args[0]) in {"0", "1"}

    return False


def _find_numeric_boolean_defaults() -> list[str]:
    offenders: list[str] = []
    for migration in sorted(MIGRATION_DIR.glob("*.py")):
        tree = ast.parse(migration.read_text(), filename=str(migration))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            func = node.func
            is_sa_column = (
                isinstance(func, ast.Attribute)
                and func.attr == "Column"
                and isinstance(func.value, ast.Name)
                and func.value.id == "sa"
            )
            if not is_sa_column or not any(_is_sa_boolean(arg) for arg in node.args):
                continue

            column_name = _literal_string(node.args[0]) if node.args else "<unknown>"
            for keyword in node.keywords:
                if keyword.arg == "server_default" and _numeric_boolean_server_default(keyword.value):
                    offenders.append(f"{migration.name}:{column_name}")
    return offenders


def test_migrations_use_postgres_boolean_server_defaults() -> None:
    offenders = _find_numeric_boolean_defaults()
    assert offenders == [], (
        "Boolean columns in PostgreSQL migrations must use true/false server defaults, "
        f"not numeric 0/1 defaults: {', '.join(offenders)}"
    )


if __name__ == "__main__":
    test_migrations_use_postgres_boolean_server_defaults()
