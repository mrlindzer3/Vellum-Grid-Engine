from fastapi import APIRouter, HTTPException, Body
from vellum_grid.core.parser import ScriptParser
from vellum_grid.core.mapper import LexiconMapper
from vellum_grid.core.analyzer import NarrativeAnalyzer
from vellum_grid.schemas.models import ScriptAnalysisResponseModel

router = APIRouter(prefix="/api/v1", tags=["Analysis"])

@router.post("/analyze", response_model=ScriptAnalysisResponseModel)
def analyze_script_endpoint(script_text: str = Body(..., media_type="text/plain")):
    """Parses raw script text, maps scenes against the lexicon matrix, and runs full narrative analysis."""
    if not script_text.strip():
        raise HTTPException(status_code=400, detail="Script text payload cannot be empty.")
    
    parsed_scenes = ScriptParser.parse_script(script_text)
    if not parsed_scenes:
        raise HTTPException(status_code=422, detail="No valid scenes or sluglines detected in script text.")
    
    mapped_scenes = LexiconMapper.map_scenes(parsed_scenes)
    analysis_results = NarrativeAnalyzer.analyze_script(mapped_scenes)
    
    return analysis_results
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from vellum_grid.api.main import ScriptPayload
from vellum_grid.core.parser import ScriptParser
from vellum_grid.core.mapper import MatrixMapper
from vellum_grid.core.analyzer import MatrixAnalyzer

router = APIRouter(prefix="/matrix", tags=["Matrix Operations"])

@router.post("/process", response_model=Dict[str, Any])
def process_matrix_payload(payload: ScriptPayload):
    """Executes full parsing, mapping, and analytical drift report for external producer pipelines."""
    try:
        parser = ScriptParser(payload.raw_script)
        scenes = parser.parse_scenes()
        
        if not scenes:
            raise HTTPException(status_code=400, detail="Invalid scene structures detected during routing.")

        mapper = MatrixMapper(payload.lexicon_matrix)
        mapped_scenes = mapper.map_entire_script(scenes)

        analyzer = MatrixAnalyzer(mapped_scenes)
        return {
            "routing_status": "success",
            "summary": analyzer.generate_structural_summary(),
            "drift": analyzer.calculate_tonal_drift()
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
