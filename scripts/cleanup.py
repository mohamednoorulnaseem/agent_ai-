#!/usr/bin/env python3
"""
Professional Cleanup Script

Removes temporary files and organizes project for production.
"""

import os
import shutil
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def remove_unwanted_files():
    """Remove temporary and unwanted files."""
    unwanted_patterns = [
        "__pycache__",
        "*.pyc",
        ".pytest_cache",
        ".mypy_cache",
        "*.egg-info",
        ".coverage",
        "*.db",
        ".DS_Store",
    ]

    removed_count = 0

    for pattern in unwanted_patterns:
        if "*" in pattern:
            # Handle wildcards
            for file in Path(".").rglob(pattern):
                if file.is_file():
                    try:
                        file.unlink()
                        logger.info(f"Removed: {file}")
                        removed_count += 1
                    except Exception as e:
                        logger.warning(f"Could not remove {file}: {e}")
        else:
            # Handle directory patterns
            for dir_path in Path(".").rglob(pattern):
                if dir_path.is_dir():
                    try:
                        shutil.rmtree(dir_path)
                        logger.info(f"Removed directory: {dir_path}")
                        removed_count += 1
                    except Exception as e:
                        logger.warning(f"Could not remove {dir_path}: {e}")

    logger.info(f"✅ Removed {removed_count} unwanted items")


def organize_documentation():
    """Organize documentation files."""
    docs_dir = Path("docs")
    docs_dir.mkdir(exist_ok=True)

    # Create subdirectories
    (docs_dir / "api").mkdir(exist_ok=True)
    (docs_dir / "guides").mkdir(exist_ok=True)
    (docs_dir / "architecture").mkdir(exist_ok=True)

    logger.info("✅ Documentation organized")


def create_production_files():
    """Create essential production files."""
    files_created = 0

    # Create .gitkeep files for empty directories
    for empty_dir in ["tests/fixtures", "src/models", "src/utils"]:
        gitkeep = Path(empty_dir) / ".gitkeep"
        if not gitkeep.exists():
            gitkeep.touch()
            files_created += 1

    logger.info(f"✅ Created {files_created} production files")


def verify_structure():
    """Verify project structure is correct."""
    required_dirs = [
        "src",
        "src/agent",
        "src/llm",
        "src/repo",
        "tests",
        "docs",
        "infrastructure",
        ".vscode",
        ".github",
    ]

    missing = []
    for dir_path in required_dirs:
        if not Path(dir_path).exists():
            missing.append(dir_path)

    if missing:
        logger.warning(f"⚠️ Missing directories: {missing}")
        return False
    else:
        logger.info("✅ Project structure verified")
        return True


def main():
    """Run cleanup and organization."""
    print("=" * 60)
    print("Agent AI Framework - Professional Cleanup")
    print("=" * 60 + "\n")

    remove_unwanted_files()
    organize_documentation()
    create_production_files()
    is_valid = verify_structure()

    print("\n" + "=" * 60)
    if is_valid:
        print("✅ Project is organized and ready for production!")
    else:
        print("⚠️ Project organization has some issues")
    print("=" * 60)

    return 0 if is_valid else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
