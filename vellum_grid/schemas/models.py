from pydantic import BaseModel
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class SceneMetricsModel(BaseModel):
    scene_number: int
    slugline: str
    vector_coordinates: Dict[str, float] = Field(default_factory=dict)
    variance_score: float = 0.0

class ScriptAnalysisResponseModel(BaseModel):
    total_scenes: int
    scenes: List[SceneMetricsModel]
    high_variance_transitions: List[int] = Field(default_factory=list)
    structural_summary: Optional[Dict[str, float]] = None

