#!/usr/bin/env python3
"""
Release helper script for AI Agent Framework.

This script helps manage the release process including version bumping,
changelog generation, and release coordination.

Usage:
    python scripts/release.py check              # Check release readiness
    python scripts/release.py bump patch         # Bump patch version
    python scripts/release.py bump minor         # Bump minor version
    python scripts/release.py bump major         # Bump major version
    python scripts/release.py validate           # Validate release
"""

import re
import sys
import argparse
from pathlib import Path
from typing import Tuple, Optional


def get_current_version() -> str:
    """Get current version from setup.py."""
    setup_file = Path("setup.py")
    if not setup_file.exists():
        raise FileNotFoundError("setup.py not found")

    content = setup_file.read_text()
    match = re.search(r'version="([^"]*)"', content)
    if not match:
        raise ValueError("Could not find version in setup.py")

    return match.group(1)


def parse_version(version: str) -> Tuple[int, int, int]:
    """Parse version string into (major, minor, patch)."""
    match = re.match(r"(\d+)\.(\d+)\.(\d+)", version)
    if not match:
        raise ValueError(f"Invalid version format: {version}")

    return int(match.group(1)), int(match.group(2)), int(match.group(3))


def bump_version(version: str, bump_type: str) -> str:
    """Bump version based on type (major, minor, patch)."""
    major, minor, patch = parse_version(version)

    if bump_type == "major":
        return f"{major + 1}.0.0"
    elif bump_type == "minor":
        return f"{major}.{minor + 1}.0"
    elif bump_type == "patch":
        return f"{major}.{minor}.{patch + 1}"
    else:
        raise ValueError(f"Invalid bump type: {bump_type}")


def update_version_in_files(old_version: str, new_version: str) -> None:
    """Update version in all relevant files."""
    files_to_update = [
        ("setup.py", f'version="{old_version}"', f'version="{new_version}"'),
        ("src/__version__.py", f'__version__ = "{old_version}"', f'__version__ = "{new_version}"'),
    ]

    for filepath, old_text, new_text in files_to_update:
        path = Path(filepath)
        if not path.exists():
            print(f"⚠️  File not found: {filepath}")
            continue

        content = path.read_text()
        if old_text not in content:
            print(f"⚠️  Old version not found in {filepath}")
            continue

        new_content = content.replace(old_text, new_text)
        path.write_text(new_content)
        print(f"✓ Updated {filepath}")


def check_changelog(version: str) -> bool:
    """Check if CHANGELOG has entry for version."""
    changelog_file = Path("CHANGELOG.md")
    if not changelog_file.exists():
        return False

    content = changelog_file.read_text()
    return f"## [{version}]" in content


def validate_release(version: str) -> bool:
    """Validate that release is ready."""
    print(f"\n🔍 Validating release v{version}...\n")

    checks = [
        ("Version format", is_valid_version(version)),
        ("Changelog entry", check_changelog(version)),
        ("Git repo clean", is_git_clean()),
        ("Python syntax", check_python_syntax()),
    ]

    all_passed = True
    for check_name, passed in checks:
        status = "✓" if passed else "✗"
        print(f"  {status} {check_name}")
        if not passed:
            all_passed = False

    return all_passed


def is_valid_version(version: str) -> bool:
    """Check if version string is valid."""
    return bool(re.match(r"^\d+\.\d+\.\d+$", version))


def is_git_clean() -> bool:
    """Check if git repo is clean."""
    import subprocess
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip() == ""
    except Exception:
        return False


def check_python_syntax() -> bool:
    """Check Python syntax in src/."""
    import py_compile
    try:
        for py_file in Path("src").rglob("*.py"):
            py_compile.compile(str(py_file), doraise=True)
        return True
    except Exception:
        return False


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Release helper for AI Agent Framework"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # check command
    subparsers.add_parser("check", help="Check current version")

    # bump command
    bump_parser = subparsers.add_parser("bump", help="Bump version")
    bump_parser.add_argument(
        "type",
        choices=["major", "minor", "patch"],
        help="Type of version bump"
    )

    # validate command
    subparsers.add_parser("validate", help="Validate release readiness")

    args = parser.parse_args()

    try:
        current_version = get_current_version()
        print(f"Current version: {current_version}\n")

        if args.command == "check":
            print("✓ Version check complete")

        elif args.command == "bump":
            new_version = bump_version(current_version, args.type)
            print(f"Bumping {args.type}: {current_version} → {new_version}")
            print("\nNext steps:")
            print(f"  1. Update CHANGELOG.md with version {new_version}")
            print(f"  2. Run: git add -A && git commit -m 'chore: bump version to {new_version}'")
            print(f"  3. Use GitHub Actions to release")

        elif args.command == "validate":
            if validate_release(current_version):
                print(f"\n✅ Release v{current_version} is ready!")
            else:
                print(f"\n❌ Release v{current_version} is not ready")
                sys.exit(1)

        else:
            parser.print_help()

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
