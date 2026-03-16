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

# Generate audited waitlist and operator-cost datasets
datasets:
    uv run python scripts/generate_verified_datasets.py

# Generate machine-verifiable results summary
results: datasets
    uv run python scripts/generate_results.py
    uv run python scripts/generate_verified_readme_visuals.py

# Regenerate audited analysis outputs only
build: setup
    uv run jupyter nbconvert --to notebook --execute notebooks/00_data_collection.ipynb --output-dir notebooks/
    uv run jupyter nbconvert --to notebook --execute notebooks/01_wage_policy_analysis.ipynb --output-dir notebooks/
    uv run jupyter nbconvert --to notebook --execute notebooks/03_wage_stagnation.ipynb --output-dir notebooks/
    uv run python scripts/generate_verified_datasets.py
    uv run python scripts/generate_results.py
    uv run python scripts/generate_verified_readme_visuals.py
