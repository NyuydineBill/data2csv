# Automated Deployment Guide

This guide explains how to set up automated deployment to PyPI using GitHub Actions with smart version management.

## What This Does

When you merge code to the `main` branch, the workflow will automatically:

1. ✅ **Run tests** on Python 3.11 + Django
2. ✅ **Smart version management** - Auto-increment or manual specification
3. ✅ **Build the package** (source and wheel distributions)
4. ✅ **Validate package metadata** using `twine check`
5. ✅ **Upload to PyPI** using your API token
6. ✅ **Create a GitHub release** with proper versioning

## Smart Version Management

### Automatic Version Bumping

The workflow automatically determines version bumps based on commit messages:

- **`[patch]`** - Increments patch version (1.0.0 → 1.0.1)
- **`[minor]`** - Increments minor version (1.0.0 → 1.1.0)  
- **`[major]`** - Increments major version (1.0.0 → 2.0.0)
- **Default** - Automatically bumps patch version

### Manual Version Specification

You can specify exact versions in commit messages:

```
git commit -m "Add new feature version: 2.0.0"
```

This will set the version to exactly 2.0.0 instead of auto-incrementing.

## Setup Steps

### 1. Add PyPI API Token to GitHub Secrets

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `PYPI_API_TOKEN`
5. Value: Your PyPI API token (starts with `pypi-`)

### 2. Push the Workflow Files

The workflow files are already created in `.github/workflows/`. Just commit and push them:

```bash
git add .github/ DEPLOYMENT.md
git commit -m "Add automated CI/CD pipeline"
git push origin main
```

### 3. That's It! 🎉

Now every time you merge to `main`, your package will automatically:
- Get tested
- Get version bumped
- Get built  
- Get uploaded to PyPI
- Get a new release

## Workflow Files

- **`.github/workflows/smart-release.yml`** - **RECOMMENDED** - Smart version management
- **`.github/workflows/release.yml`** - Basic version bumping

## How It Works

### On Pull Request
- Runs tests only
- No deployment

### On Main Branch Push
- Runs tests
- If tests pass, determines version strategy
- Bumps version automatically or uses manual specification
- Builds package
- Uploads to PyPI
- Creates GitHub release with proper versioning

## Version Management Examples

### Automatic Patch Bump (Default)
```bash
git commit -m "Fix bug in export functionality"
# Results in: 1.0.0 → 1.0.1
```

### Automatic Minor Bump
```bash
git commit -m "Add JSON export support [minor]"
# Results in: 1.0.0 → 1.1.0
```

### Automatic Major Bump
```bash
git commit -m "Breaking changes in API [major]"
# Results in: 1.0.0 → 2.0.0
```

### Manual Version
```bash
git commit -m "Release version 2.0.0 version: 2.0.0"
# Results in: Exact version 2.0.0
```

## Manual Release

If you need to release manually:

```bash
# Update version in setup.py and __init__.py
# Then run:
python -m build
twine check dist/*
twine upload dist/*
```

## Troubleshooting

### Common Issues

1. **Tests failing**: Check the Actions tab for error details
2. **PyPI upload failing**: Verify your `PYPI_API_TOKEN` secret
3. **Version conflicts**: The workflow automatically handles version conflicts
4. **Git push failing**: Ensure the workflow has proper permissions

### Debug Mode

Add `--verbose` to see detailed output:

```yaml
- name: Publish to PyPI
  run: |
    twine upload --verbose dist/*
```

## Security Notes

- Never commit your PyPI API token
- The token is stored securely in GitHub Secrets
- Only runs on main branch pushes (not PRs)
- Tests run before any deployment
- Version bumping is automated and secure

## Customization

You can modify the workflow to:

- Add more Python/Django version combinations
- Include additional testing tools
- Add deployment to other package indexes
- Customize release notes format
- Add changelog generation

## Support

If you encounter issues:

1. Check the GitHub Actions logs
2. Verify your PyPI token is valid
3. Ensure all dependencies are in `requirements.txt`
4. Check that tests pass locally first
5. Verify commit message format for version control

## Example Workflow

1. **Make changes** in a feature branch
2. **Create PR** to main
3. **Merge PR** with appropriate version tag:
   - `[patch]` for bug fixes
   - `[minor]` for new features
   - `[major]` for breaking changes
   - `version: X.Y.Z` for exact versions
4. **GitHub Actions automatically:**
   - Tests everything
   - Bumps version appropriately
   - Builds package
   - Uploads to PyPI
   - Creates release

Your users can then immediately install the latest version with:
```bash
pip install django-admin-export-tools
``` 