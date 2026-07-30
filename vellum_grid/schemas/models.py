from pydantic import BaseModel
from typing import List, Dict, Any

class SceneMetricsModel(BaseModel):
    scene_number: int
    slugline: str
    vector_coordinates: Dict[str, float]

class ScriptAnalysisResponseModel(BaseModel):
    structural_summary: Dict[str, Any]
    tonal_drift_report: List[Dict[str, Any]]
    scene_count: int
    scenes: List[SceneMetricsModel]
