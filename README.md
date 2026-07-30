
# Vellum Grid Engine

The Vellum Grid Engine is a service-oriented narrative matrix and script analysis platform designed for writers, directors, and producers. It bridges raw script text and the 100-element lexicon matrix, offering programmatic scene parsing, tonal drift detection, and automated structural evaluation.

## Architecture

* **Core Parser (`vellum_grid/core/parser.py`)**: Segments unstructured script text into structured scene blocks based on sluglines.
* **Matrix Mapper (`vellum_grid/core/mapper.py`)**: Projects scene content against the 100-element lexicon matrix to compute semantic vector coordinates.
* **Matrix Analyzer (`vellum_grid/core/analyzer.py`)**: Computes Euclidean variance, tonal drift, and structural summaries across acts.
* **API Layer (`vellum_grid/api/main.py` & `router.py`)**: Exposes FastAPI endpoints for external producer pipelines and creative tooling integration.

## Setup & Deployment

### Local Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
