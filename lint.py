#!/usr/bin/env python3
"""Linter for enforcing layer architecture in src/."""

import ast
import os
import sys
from pathlib import Path


# Layer definitions: layer -> list of layers it may import from
LAYERS = {
    "types": ["types"],
    "config": ["types", "config"],
    "utils": ["utils"],
    "providers": ["types", "config", "utils", "providers"],
    "repo": ["types", "config", "repo"],
    "service": ["types", "config", "repo", "providers", "service"],
    "runtime": ["types", "config", "repo", "service", "providers", "runtime"],
    "ui": ["types", "config", "service", "runtime", "providers", "ui"],
}

VALID_LAYERS = set(LAYERS.keys())
MAX_LINES = 300

REPO_ROOT = Path(__file__).parent
SRC_DIR = REPO_ROOT / "src"


def get_layer_from_path(file_path: Path) -> str | None:
    """Extract layer name from file path relative to src/."""
    try:
        rel_path = file_path.relative_to(SRC_DIR)
        parts = rel_path.parts
        if len(parts) > 0:
            layer = parts[0]
            if layer in VALID_LAYERS:
                return layer
    except ValueError:
        pass
    return None


def get_imports(file_path: Path) -> list[str]:
    """Extract import module names from a Python file."""
    imports = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=str(file_path))

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)
                elif node.level == 0 and node.module is None:
                    # Handle 'from . import' cases
                    pass
    except SyntaxError:
        pass

    return imports


def check_line_count(file_path: Path) -> list[tuple[int, str]]:
    """Check if file exceeds MAX_LINES."""
    violations = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            if len(lines) > MAX_LINES:
                violations.append((len(lines), f"File exceeds {MAX_LINES} lines ({len(lines)} lines)"))
    except Exception:
        pass
    return violations


def check_imports(file_path: Path, layer: str) -> list[tuple[int, str]]:
    """Check that imports respect layer dependencies."""
    violations = []
    allowed_imports = LAYERS[layer]

    imports = get_imports(file_path)
    for imp in imports:
        # Check if import is from src/ (internal import)
        if imp.startswith("src."):
            # Extract the layer from the import
            parts = imp.split(".")
            if len(parts) > 1:
                imported_layer = parts[1]
                if imported_layer not in allowed_imports:
                    violations.append((1, f"Cannot import from layer '{imported_layer}' - layer '{layer}' may only import from: {', '.join(allowed_imports)}"))

    return violations


def lint_file(file_path: Path) -> list[tuple[int, str, str]]:
    """Lint a single file. Returns list of (line, message, file_path) violations."""
    violations = []

    # Check line count
    line_violations = check_line_count(file_path)
    for line_num, msg in line_violations:
        violations.append((line_num, msg, str(file_path)))

    # Get layer and check imports
    layer = get_layer_from_path(file_path)
    if layer:
        import_violations = check_imports(file_path, layer)
        for line_num, msg in import_violations:
            violations.append((line_num, msg, str(file_path)))

    return violations


def main() -> int:
    """Run the linter on all Python files under src/."""
    all_violations = []

    # Find all .py files under src/
    for root, _, files in os.walk(SRC_DIR):
        for file in files:
            if file.endswith(".py"):
                file_path = Path(root) / file
                violations = lint_file(file_path)
                all_violations.extend(violations)

    if not all_violations:
        print("✓ All files pass linting.")
        return 0

    # Sort violations by file, then line number
    all_violations.sort(key=lambda x: (x[2], x[0]))

    print("✗ Linting failed with the following violations:\n")
    for line, msg, filepath in all_violations:
        print(f"{filepath}:{line}: {msg}")

    return 1


if __name__ == "__main__":
    sys.exit(main())
