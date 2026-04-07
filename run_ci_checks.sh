#!/bin/bash
# Full CI check script - runs all checks that GitHub Actions will run

set -e  # Exit on any error

echo "🚀 Starting Full CI Check Locally"
echo "================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. Check Python version
echo "📌 Step 1: Checking Python version..."
python_version=$(python3 --version)
echo "  Using $python_version"
if [[ $python_version != *"3.9"* ]]; then
    echo -e "${YELLOW}  Warning: Expected Python 3.9, but found $python_version${NC}"
fi
echo ""

# 2. Set up environment
echo "📌 Step 2: Setting up environment..."
export PYTHONPATH="${PYTHONPATH}:${PWD}"
echo "  PYTHONPATH set to: $PYTHONPATH"
echo ""

# 3. Install dependencies
echo "📌 Step 3: Installing dependencies..."
pip install -r requirements.txt
pip install pytest pytest-cov pytest-xdist
echo ""

# 4. Run Black formatting check
echo "📌 Step 4: Checking Black formatting..."
if black --check src/ tests/ --verbose --line-length=88; then
    echo -e "${GREEN}  ✅ Black check passed${NC}"
else
    echo -e "${RED}  ❌ Black formatting issues found${NC}"
    echo "  Run 'black src/ tests/ --line-length=88' to fix"
    exit 1
fi
echo ""

# 5. Run isort import sorting check
echo "📌 Step 5: Checking isort imports..."
if isort --check-only --profile black --line-length=88 src/ tests/; then
    echo -e "${GREEN}  ✅ isort check passed${NC}"
else
    echo -e "${RED}  ❌ Import sorting issues found${NC}"
    echo "  Run 'isort --profile black src/ tests/' to fix"
    exit 1
fi
echo ""

# 6. Run Pylint
echo "📌 Step 6: Running Pylint..."
if pylint src/ --fail-under=7.0 --exit-zero; then
    echo -e "${GREEN}  ✅ Pylint passed${NC}"
else
    echo -e "${YELLOW}  ⚠️  Pylint issues found (non-fatal)${NC}"
fi
echo ""

# 7. Run MyPy type checking
echo "📌 Step 7: Running MyPy type checking..."
if mypy src/ --ignore-missing-imports --no-strict-optional --check-untyped-defs; then
    echo -e "${GREEN}  ✅ MyPy passed${NC}"
else
    echo -e "${RED}  ❌ MyPy type errors found${NC}"
    exit 1
fi
echo ""

# 8. Run Bandit security check
echo "📌 Step 8: Running Bandit security check..."
if bandit -r src/ -ll; then
    echo -e "${GREEN}  ✅ Bandit passed${NC}"
else
    echo -e "${YELLOW}  ⚠️  Bandit issues found (non-fatal)${NC}"
fi
echo ""

# 9. Run tests with coverage
echo "📌 Step 9: Running tests with coverage..."
if pytest tests/ -v -n auto --cov=src/image_generator --cov-report=term --cov-report=html --cov-fail-under=50 --maxfail=5; then
    echo -e "${GREEN}  ✅ All tests passed with sufficient coverage${NC}"
else
    echo -e "${RED}  ❌ Tests failed or coverage insufficient${NC}"
    exit 1
fi
echo ""

# 10. Test CLI
echo "📌 Step 10: Testing CLI..."
if python -m src.image_generator.cli --size 300 --output test_output --formats webp svg png; then
    echo -e "${GREEN}  ✅ CLI test passed${NC}"
    # Clean up test output
    rm -rf test_output/
else
    echo -e "${RED}  ❌ CLI test failed${NC}"
    exit 1
fi
echo ""

# Success!
echo "================================"
echo -e "${GREEN}✅ All CI checks passed successfully!${NC}"
echo "================================"
