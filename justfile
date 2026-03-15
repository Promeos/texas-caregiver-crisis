# Texas Caregiver Crisis — task runner
# Install: brew install just (macOS) or cargo install just

# Install dependencies and package in dev mode
setup:
    uv sync
    uv pip install -e ".[dev]"

# Run all tests
test:
    uv run pytest tests/ -v

# Lint with ruff
lint:
    uv run ruff check .

# Run linting + tests
check: lint test

# Regenerate all analysis outputs from scratch
build: setup
    uv run jupyter nbconvert --to notebook --execute notebooks/00_data_collection.ipynb --output-dir notebooks/
    uv run jupyter nbconvert --to notebook --execute notebooks/03_wage_policy_analysis.ipynb --output-dir notebooks/
    uv run jupyter nbconvert --to notebook --execute notebooks/04_waitlist_access.ipynb --output-dir notebooks/
    uv run jupyter nbconvert --to notebook --execute notebooks/05_wage_stagnation.ipynb --output-dir notebooks/
    uv run jupyter nbconvert --to notebook --execute notebooks/06_policy_brief.ipynb --output-dir notebooks/
