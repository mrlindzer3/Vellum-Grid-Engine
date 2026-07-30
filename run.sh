#!/bin/bash
echo "Starting Vellum Grid Engine..."
uvicorn vellum_grid.api.main:app --host 0.0.0.0 --port 8000 --reload
