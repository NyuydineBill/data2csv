# Automated Deployment Guide

This guide explains how to set up automated deployment to PyPI using GitHub Actions.

## What This Does

When you merge code to the `main` branch, the workflow will automatically:

1. ✅ **Run tests** on multiple Python and Django versions
2. ✅ **Build the package** (source and wheel distributions)
3. ✅ **Validate package metadata** using `twine check`
4. ✅ **Upload to PyPI** using your API token
5. ✅ **Create a GitHub release** with the build number

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
git add .github/
git commit -m "Add automated CI/CD workflow"
git push origin main
```

### 3. Verify Setup

1. Go to your GitHub repository
2. Click **Actions** tab
3. You should see the workflow running after pushing to main

## Workflow Files

- **`.github/workflows/release.yml`** - Main CI/CD pipeline (recommended)
- **`.github/workflows/ci-cd.yml`** - Comprehensive testing matrix
- **`.bumpversion.cfg`** - Version bumping configuration

## How It Works

### On Pull Request
- Runs tests on Python 3.11 + Django
- No deployment

### On Main Branch Push
- Runs tests
- If tests pass, builds package
- Uploads to PyPI
- Creates GitHub release

## Manual Release

If you need to release manually:

```bash
# Update version in setup.py
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