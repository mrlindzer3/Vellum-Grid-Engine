import pytest
from fastapi.testclient import TestClient
from vellum_grid.api.main import app
from vellum_grid.core.parser import ScriptParser
from vellum_grid.core.mapper import LexiconMapper
from vellum_grid.core.analyzer import NarrativeAnalyzer

client = TestClient(app)

SAMPLE_SCRIPT = """
EXT. ABANDONED WAREHOUSE - DAY

The rain pours down on the rusted corrugated metal. John stands waiting.

INT. CONTROL ROOM - NIGHT

Monitors flicker with green phosphor light. Sarah reviews the incoming data stream.
"""

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "engine": "active"}

def test_script_parser():
    scenes = ScriptParser.parse_script(SAMPLE_SCRIPT)
    assert len(scenes) == 2
    assert scenes[0]["scene_number"] == 1
    assert "ABANDONED WAREHOUSE" in scenes[0]["slugline"]
    assert scenes[1]["scene_number"] == 2
    assert "CONTROL ROOM" in scenes[1]["slugline"]

def test_lexicon_mapper():
    parsed = ScriptParser.parse_script(SAMPLE_SCRIPT)
    mapped = LexiconMapper.map_scenes(parsed)
    assert len(mapped) == 2
    assert len(mapped[0]["vector_coordinates"]) == 100
    assert "lex_001" in mapped[0]["vector_coordinates"]

def test_narrative_analyzer():
    parsed = ScriptParser.parse_script(SAMPLE_SCRIPT)
    mapped = LexiconMapper.map_scenes(parsed)
    analysis = NarrativeAnalyzer.analyze_script(mapped)
    assert analysis["total_scenes"] == 2
    assert "structural_summary" in analysis
    assert "mean_vector_magnitude" in analysis["structural_summary"]

def test_analyze_endpoint():
    response = client.post(
        "/api/v1/analyze",
        content=SAMPLE_SCRIPT,
        headers={"Content-Type": "text/plain"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["total_scenes"] == 2
    assert len(data["scenes"]) == 2
import pytest
from vellum_grid.core.parser import ScriptParser
from vellum_grid.core.mapper import MatrixMapper
from vellum_grid.core.analyzer import MatrixAnalyzer

SAMPLE_SCRIPT = """
INT. CONTROL ROOM - NIGHT
The neon hums softly against the dark paneling.
A sudden flash outside the window.

EXT. VAPOR PLAZA - CONTINUOUS
Smoke rises from the drainage grid.
"""

SAMPLE_MATRIX = {
    "neon_pulse": [0.1, 0.5, 0.9],
    "shadow_depth": [0.8, 0.2, 0.1]
}

def test_script_parser():
    parser = ScriptParser(SAMPLE_SCRIPT)
    scenes = parser.parse_scenes()
    
    assert len(scenes) == 2
    assert scenes[0].scene_number == 1
    assert scenes[0].slugline == "INT. CONTROL ROOM - NIGHT"
    assert scenes[1].scene_number == 2
    assert scenes[1].slugline == "EXT. VAPOR PLAZA - CONTINUOUS"

def test_matrix_mapper():
    parser = ScriptParser(SAMPLE_SCRIPT)
    scenes = parser.parse_scenes()
    
    mapper = MatrixMapper(SAMPLE_MATRIX)
    mapped_scenes = mapper.map_entire_script(scenes)
    
    assert "neon_pulse" in mapped_scenes[0].vector_coordinates
    assert "shadow_depth" in mapped_scenes[0].vector_coordinates

def test_matrix_analyzer():
    parser = ScriptParser(SAMPLE_SCRIPT)
    scenes = parser.parse_scenes()
    mapper = MatrixMapper(SAMPLE_MATRIX)
    mapped_scenes = mapper.map_entire_script(scenes)
    
    analyzer = MatrixAnalyzer(mapped_scenes)
    summary = analyzer.generate_structural_summary()
    
    assert summary["total_scenes"] == 2
    assert "high_variance_transitions" in summary
