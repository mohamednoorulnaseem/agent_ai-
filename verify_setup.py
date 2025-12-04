#!/usr/bin/env python3
"""
Verify the Agent AI Framework setup is complete and ready to use.
"""

import sys
import importlib
from pathlib import Path


def check_imports():
    """Check that all required packages are installed."""
    required = [
        "fastapi",
        "uvicorn",
        "pydantic",
        "httpx",
        "aiofiles",
        "redis",
        "psycopg2",
        "yaml",
        "dotenv",
    ]

    print("🔍 Checking Python packages...")
    missing = []

    for package in required:
        try:
            importlib.import_module(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package}")
            missing.append(package)

    return missing


def check_project_structure():
    """Check that all required directories exist."""
    print("\n🔍 Checking project structure...")

    required_dirs = [
        "src",
        "src/agent",
        "src/llm",
        "src/repo",
        "k8s",
        "terraform",
        "docs",
        ".vscode",
    ]

    missing = []
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"  ✅ {dir_path}/")
        else:
            print(f"  ❌ {dir_path}/")
            missing.append(dir_path)

    return missing


def check_config_files():
    """Check that all required configuration files exist."""
    print("\n🔍 Checking configuration files...")

    required_files = [
        ".vscode/settings.json",
        ".vscode/launch.json",
        ".vscode/tasks.json",
        ".vscode/extensions.json",
        "requirements.txt",
        "setup.py",
        "README.md",
        "QUICK_START_GUIDE.md",
    ]

    missing = []
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path}")
            missing.append(file_path)

    return missing


def check_python_version():
    """Check Python version."""
    print("\n🔍 Checking Python version...")
    version = sys.version_info
    min_version = (3, 9)

    if version >= min_version:
        print(f"  ✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"  ❌ Python {version.major}.{version.minor} (need 3.9+)")
        return False


def main():
    """Run all checks."""
    print("=" * 60)
    print("Agent AI Framework - Setup Verification")
    print("=" * 60)

    # Run checks
    missing_packages = check_imports()
    missing_dirs = check_project_structure()
    missing_files = check_config_files()
    python_ok = check_python_version()

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    if not missing_packages and not missing_dirs and not missing_files and python_ok:
        print("\n✅ ✅ ✅ ALL CHECKS PASSED! ✅ ✅ ✅")
        print("\nYour Agent AI Framework is ready to use!")
        print("\nNext steps:")
        print("  1. Review QUICK_START_GUIDE.md")
        print("  2. Check PHASE_7_INDEX.md for features")
        print("  3. Run: python -m src.api")
        print("  4. Visit: http://localhost:8000/docs")
        return 0
    else:
        print("\n⚠️  Some checks failed:")
        if missing_packages:
            print(f"  - Missing packages: {', '.join(missing_packages)}")
        if missing_dirs:
            print(f"  - Missing directories: {', '.join(missing_dirs)}")
        if missing_files:
            print(f"  - Missing files: {', '.join(missing_files)}")
        if not python_ok:
            print("  - Python version too old (need 3.9+)")
        return 1


if __name__ == "__main__":
    sys.exit(main())
