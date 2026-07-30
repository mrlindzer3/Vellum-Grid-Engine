from fastapi import FastAPI
from vellum_grid.schemas.models import ScriptAnalysisResponseModel, SceneMetricsModel

app = FastAPI(
    title="Vellum Grid Engine",
    description="Service-oriented narrative matrix and script analysis platform.",
    version="1.0.0"
)

@app.get("/health")
def health_check():
    return {"status": "healthy", "engine": "active"}
