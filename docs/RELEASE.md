# Release Process

This document describes the release process for the AI Agent Framework.

## Overview

The project uses automated release workflows to manage versioning, tagging, and publishing.

## Version Scheme

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR.MINOR.PATCH** (e.g., 0.2.0)
- **MAJOR**: Breaking changes
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, backward compatible

## Release Checklist

Before releasing a new version:

- [ ] All tests passing (`make test`)
- [ ] Code quality checks passing (`make check`)
- [ ] Documentation updated
- [ ] CHANGELOG.md updated with new version section
- [ ] Version numbers bumped in:
  - `setup.py`
  - `src/__version__.py`
- [ ] Git history is clean
- [ ] All commits are pushed

## Release Steps

### 1. Update Changelog

Add a new section to `CHANGELOG.md` at the top with format:

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added

- New feature description

### Changed

- Changed behavior description

### Fixed

- Bug fix description

### Deprecated

- Deprecated functionality

### Removed

- Removed functionality

### Security

- Security fixes
```

### 2. Prepare Release

Update version files:

```bash
# Bump version (creates reminder)
python scripts/release.py bump patch
```

Then manually update the version files or use:

```bash
# Update setup.py
sed -i 's/version="0.1.0"/version="0.2.0"/' setup.py

# Update __version__.py
sed -i 's/__version__ = "0.1.0"/__version__ = "0.2.0"/' src/__version__.py
```

### 3. Commit & Push

```bash
git add setup.py src/__version__.py CHANGELOG.md
git commit -m "chore: bump version to 0.2.0"
git push origin main
```

### 4. Create Release (Automated)

Go to GitHub Actions → Release workflow:

1. Click "Run workflow"
2. Fill in:
   - **Version**: Enter version (e.g., 0.2.0)
   - **Release type**: Select type (major/minor/patch)
   - **Pre-release**: Check if pre-release
3. Click "Run workflow"

The workflow will:

- ✓ Validate version format
- ✓ Verify changelog entry
- ✓ Create and tag commit
- ✓ Generate GitHub release
- ✓ Publish to PyPI (if configured)
- ✓ Push Docker image (if credentials set)

## Manual Release (Alternative)

If automation is unavailable:

```bash
# Create annotated tag
git tag -a v0.2.0 -m "Release v0.2.0"

# Push tag
git push origin v0.2.0

# Create release on GitHub manually
# - Go to Releases
# - Click "Draft a new release"
# - Select tag v0.2.0
# - Add changelog notes
# - Publish
```

## Release Notes Template

For GitHub release notes:

```markdown
# v0.2.0 - December 2, 2025

## 🎉 Highlights

Brief description of major features or changes.

## 📋 Changes

### Added

- Feature 1
- Feature 2

### Fixed

- Bug fix 1
- Bug fix 2

### Changed

- Behavior change 1

## 📦 Installation

### Via pip

\`\`\`bash
pip install --upgrade agent_ai
\`\`\`

### Via Docker

\`\`\`bash
docker pull agent-ai:v0.2.0
docker compose up
\`\`\`

## 🙏 Contributors

Thanks to all contributors for this release!

## 📖 Documentation

- [API Reference](https://github.com/mohamednoorulnaseem/agent_ai-/blob/main/docs/API.md)
- [Deployment Guide](https://github.com/mohamednoorulnaseem/agent_ai-/blob/main/docs/DEPLOYMENT.md)
- [Contributing Guide](https://github.com/mohamednoorulnaseem/agent_ai-/blob/main/docs/CONTRIBUTING.md)
```

## PyPI Publishing

To publish to PyPI:

1. Create account at https://pypi.org
2. Generate API token
3. Add secret to GitHub: `PYPI_API_TOKEN`
4. Run release workflow

The workflow will automatically build and publish the package.

## Docker Image Publishing

To publish Docker images:

1. Create Docker Hub account
2. Generate access token
3. Add secrets to GitHub:
   - `DOCKER_USERNAME`
   - `DOCKER_PASSWORD`
4. Run release workflow

Images will be tagged as:

- `username/agent-ai:vX.Y.Z` (specific version)
- `username/agent-ai:latest` (latest stable)

## Semantic Commit Messages

Use conventional commit format:

```
type(scope): description

type: feat, fix, docs, style, refactor, test, chore, ci, perf
scope: api, cli, core, docs, ci, etc.
description: brief description
```

Examples:

- `feat(api): add webhook support`
- `fix(cli): resolve initialization error`
- `docs: update deployment guide`
- `chore: bump dependencies`

## Continuous Deployment

Releases are deployed:

- **PyPI**: Package repository
- **Docker Hub**: Container images
- **GitHub Releases**: Release notes and artifacts
- **GitHub Pages** (optional): Documentation site

## Troubleshooting

### Release workflow fails

Check:

1. Version format is correct (X.Y.Z)
2. CHANGELOG.md includes version entry
3. Git repository is clean
4. Secrets are configured (if publishing)

### Version mismatch

Ensure consistency across:

- `setup.py`
- `src/__version__.py`
- `CHANGELOG.md`
- Git tag

### PyPI upload fails

Add or check `PYPI_API_TOKEN` secret in GitHub settings.

### Docker push fails

Add or check secrets in GitHub settings:

- `DOCKER_USERNAME`
- `DOCKER_PASSWORD`

## Release Cadence

- **Patches**: As needed for bug fixes
- **Minors**: Monthly for new features
- **Majors**: Quarterly for major changes

## Rollback

If a release needs to be rolled back:

1. Delete the GitHub release
2. Delete the git tag: `git push origin --delete v0.2.0`
3. Reset to previous tag: `git reset --hard v0.1.0`
4. Force push: `git push -f origin main`

---

For questions, see [CONTRIBUTING.md](CONTRIBUTING.md) or [SUPPORT.md](SUPPORT.md).
