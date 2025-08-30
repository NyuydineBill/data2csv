# Automated Deployment Guide

This guide explains how to set up automated deployment to PyPI using GitHub Actions.

## What This Does

When you merge code to the `main` branch, the workflow will automatically:

1. ✅ **Run tests** on Python 3.11 + Django
2. ✅ **Build the package** (source and wheel distributions)
3. ✅ **Validate package metadata** using `twine check`
4. ✅ **Upload to PyPI** using your API token
5. ✅ **Create a GitHub release** with build number

## Version Management

For this workflow, you'll need to manually manage versions in your code before merging:

1. **Update version in `setup.py`**:
   ```python
   version='1.0.3',  # Change this before merging
   ```

2. **Update version in `admin_export/__init__.py`**:
   ```python
   __version__ = '1.0.3'  # Change this before merging
   ```

3. **Commit and push**:
   ```bash
   git add setup.py admin_export/__init__.py
   git commit -m "Bump version to 1.0.1"
   git push origin main
   ```

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
- Get built  
- Get uploaded to PyPI
- Get a new release

## Workflow Files

- **`.github/workflows/simple-release.yml`** - Simple CI/CD pipeline

## How It Works

### On Pull Request
- Runs tests only
- No deployment

### On Main Branch Push
- Runs tests
- If tests pass, builds package
- Uploads to PyPI
- Creates GitHub release

## Manual Version Management

Since this workflow doesn't auto-bump versions, you need to:

1. **Before merging to main**, update versions in:
   - `setup.py`
   - `admin_export/__init__.py`

2. **Use semantic versioning**:
   - **Patch** (1.0.0 → 1.0.1): Bug fixes
   - **Minor** (1.0.0 → 1.1.0): New features
   - **Major** (1.0.0 → 2.0.0): Breaking changes

3. **Example workflow**:
   ```bash
   # Make changes in feature branch
   # Update version to 1.0.4
   git add setup.py admin_export/__init__.py
   git commit -m "Bump version to 1.0.4"
   # Create PR and merge to main
   # GitHub Actions automatically builds and publishes
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
3. **Version conflicts**: Ensure version in `setup.py` is unique
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

## Customization

You can modify the workflow to:

- Add more Python/Django version combinations
- Include additional testing tools
- Add deployment to other package indexes
- Customize release notes format

## Support

If you encounter issues:

1. Check the GitHub Actions logs
2. Verify your PyPI token is valid
3. Ensure all dependencies are in `requirements.txt`
4. Check that tests pass locally first
5. Verify version numbers are updated before merging

## Example Workflow

1. **Make changes** in a feature branch
2. **Update version** in `setup.py` and `__init__.py`
3. **Create PR** to main
4. **Merge PR** to main
5. **GitHub Actions automatically:**
   - Tests everything
   - Builds package
   - Uploads to PyPI
   - Creates release

Your users can then immediately install the latest version with:
```bash
pip install django-admin-data-export
``` 