from setuptools import setup, find_packages

setup(
    name="vellum_grid",
    version="1.0.0",
    description="Service-oriented narrative matrix and script analysis engine for writers, directors, and producers.",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.110.0",
        "uvicorn==0.28.0",
        "pydantic==2.6.4",
        "pytest==8.1.1"
    ],
    entry_points={
        "console_scripts": [
            "vellum-grid=vellum_grid.api.main:app",
        ],
    },
)
