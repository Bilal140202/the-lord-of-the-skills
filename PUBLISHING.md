# 📦 Publishing `lotr-skills` to PyPI

> How to publish the `lotr` CLI so anyone can `pip install lotr-skills`

---

## 🔄 One-Time Setup

### 1. Create PyPI accounts

1. **PyPI**: Register at https://pypi.org/account/register/
2. **TestPyPI** (optional, for testing): Register at https://test.pypi.org/account/register/

### 2. Create an API token

1. Go to https://pypi.org/manage/account/token/
2. Click **"Add API token"**
3. Scope: **"Entire account"** (for first publish)
4. Copy the token (starts with `pypi-`)

### 3. Create `~/.pypirc`

```ini
[distutils]
index-servers = pypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = pypi-YOUR_TOKEN_HERE
```

---

## 📦 Build + Publish

### From the repo root:

```bash
# 1. Install build tools (one-time)
pip install build twine

# 2. Clean previous builds
rm -rf dist/ build/ *.egg-info

# 3. Build the package
python -m build
# Creates:
#   dist/lotr_skills-1.0.0-py3-none-any.whl   (wheel — binary)
#   dist/lotr_skills-1.0.0.tar.gz              (sdist — source)

# 4. Test locally (optional but recommended)
pip install dist/lotr_skills-1.0.0-py3-none-any.whl
lotr --version          # should print "lotr 1.0.0"
lotr kingdoms           # should list 10 kingdoms
pip uninstall lotr-skills   # clean up

# 5. Upload to PyPI
twine upload dist/*

# Or test on TestPyPI first:
twine upload --repository testpypi dist/*
```

### After publish:

```bash
# Anyone on earth can now do:
pip install lotr-skills

# And use:
lotr "write unit tests"
lotr kickoff "building a tauri app"
```

---

## 🔁 Updating a New Version

When you make changes and want to publish a new version:

### 1. Bump the version in `pyproject.toml`

```toml
[project]
name = "lotr-skills"
version = "1.1.0"    # ← change this
```

Also update `cli/__init__.py`:
```python
__version__ = "1.1.0"
```

And the CLI version in `cli/lotr.py`:
```python
parser.add_argument("--version", action="version", version="lotr 1.1.0")
```

### 2. Rebuild + upload

```bash
rm -rf dist/ build/
python -m build
twine upload dist/*
```

### 3. Users update with

```bash
pip install --upgrade lotr-skills
```

---

## 📋 Pre-Publish Checklist

Before each publish, verify:

- [ ] Version bumped in `pyproject.toml`, `cli/__init__.py`, and `cli/lotr.py`
- [ ] All tests pass: `pytest tests/ -v`
- [ ] `lotr --version` shows the new version
- [ ] `lotr kingdoms` works
- [ ] `lotr detect` works on a test project
- [ ] `lotr kickoff "building a tauri app"` works end-to-end
- [ ] CHANGELOG.md updated with the new version
- [ ] Git committed and pushed
- [ ] `rm -rf dist/ build/` (clean build)
- [ ] `python -m build` succeeds
- [ ] `pip install dist/*.whl` works locally
- [ ] `twine upload dist/*` succeeds

---

## 🐛 Troubleshooting

### "File already exists" error on upload

PyPI doesn't allow re-uploading the same version. Bump the version number and rebuild.

### "Invalid API token"

Make sure your `~/.pypirc` has `username = __token__` (not your PyPI username) and the password is the full token including the `pypi-` prefix.

### `lotr` command not found after install

The `lotr` script is installed to your Python's `bin/` directory. Make sure it's on your PATH:

```bash
# Linux/Mac
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Or find where it was installed:
python -m pip show lotr-skills | grep Location
```

### Import errors after install

Make sure you're not inside the repo directory when running `lotr` — Python might pick up the local `cli/` directory instead of the installed package. `cd` to a different directory first.

---

## 📊 PyPI Metadata

The package is configured in `pyproject.toml` at the repo root:

| Field | Value |
|:---|:---|
| Name | `lotr-skills` |
| Version | `1.0.0` |
| Python | `>=3.10` |
| License | MIT |
| Entry point | `lotr = "cli.lotr:main"` |
| Dependencies | `requests>=2.31.0` |

The key line is `[project.scripts]` — this tells pip to create a `lotr` terminal command that calls `cli.lotr:main()`.

---

## 🏗 CI/CD Auto-Publish (Optional)

To auto-publish on every git tag, add this to `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install build twine
      - run: python -m build
      - run: twine upload dist/*
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
```

Then every GitHub Release you publish will auto-push to PyPI.

---

<div align="center">

*One `pip install` to rule them all.*

</div>
