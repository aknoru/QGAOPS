# QGAOPS-QGPU Makefile
# [SOFTWARE] Build automation for the software baseline

PYTHON := python
PIP    := pip
PYTEST := pytest
SRC    := src/qgpu
TESTS  := tests

.PHONY: all install install-dev test test-cov benchmark golden lint clean help

all: install test

## install: Install the package in editable mode
install:
	$(PIP) install -e .

## install-dev: Install with development extras
install-dev:
	$(PIP) install -e ".[dev]"

## test: Run the full pytest suite
test:
	$(PYTEST) $(TESTS)/ -v --tb=short

## test-cov: Run tests with coverage report
test-cov:
	$(PYTEST) $(TESTS)/ -v --tb=short --cov=$(SRC) --cov-report=term-missing

## benchmark: Run all software benchmarks
benchmark:
	$(PYTHON) -m qgpu benchmark

## benchmark-rotor: Run rotor transformation benchmark
benchmark-rotor:
	$(PYTHON) -m qgpu benchmark --workload rotor

## benchmark-pointcloud: Run point-cloud benchmark
benchmark-pointcloud:
	$(PYTHON) -m qgpu benchmark --workload point_cloud

## benchmark-quantum: Run quantum-GA benchmark
benchmark-quantum:
	$(PYTHON) -m qgpu benchmark --quantum

## benchmark-ablation: Run full B0-B9 ablation study
benchmark-ablation:
	$(PYTHON) -m qgpu benchmark --ablation

## golden: Generate all golden test vectors
golden:
	$(PYTHON) -m qgpu generate-golden

## analyze: Run algebra analyzer on current workloads
analyze:
	$(PYTHON) -m qgpu analyze

## clean: Remove generated artifacts
clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	rm -rf .pytest_cache htmlcov .coverage dist build *.egg-info

## help: Show this help message
help:
	@grep -E '^## ' Makefile | sed 's/## /  /'
