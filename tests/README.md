# Tests

This directory contains pytest unit tests for the Lord of the Skills crawler pipeline.

## Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=crawler --cov-report=term-missing

# Run a specific test file
pytest tests/test_classify.py -v

# Run a specific test
pytest tests/test_classify.py::TestKingdomClassification::test_gondor_coding -v
```

## Test Files

| File | Tests |
|:---|:---|
| `test_classify.py` | LOTR kingdom classification, skill type, title/summary extraction |
| `test_dedup.py` | Title normalization, Jaccard similarity, canonical score |
| `test_crawler.py` | Skill file detection, framework detection, seed list sanity |
| `conftest.py` | Pytest configuration (adds crawler/ to sys.path) |

## Coverage

The CI workflow runs tests on Python 3.10, 3.11, and 3.12. Coverage reports are uploaded to Codecov.

## Adding Tests

When adding new features to the crawler, please add corresponding tests:

1. **New kingdom keyword** -> add a test in `test_classify.py::TestKingdomClassification`
2. **New framework pattern** -> add a test in `test_crawler.py::TestFrameworkDetection`
3. **New skill file pattern** -> add a test in `test_crawler.py::TestSkillFileDetection`
4. **New dedup logic** -> add a test in `test_dedup.py`

See [`CONTRIBUTING.md`](../CONTRIBUTING.md) for more on contributing.
