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
