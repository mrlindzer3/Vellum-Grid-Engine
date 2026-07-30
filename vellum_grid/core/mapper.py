# vellum_grid/core/mapper.py
from typing import List, Dict
from vellum_grid.core.parser import SceneBlock

class MatrixMapper:
    def __init__(self, lexicon_matrix: Dict[str, List[float]]):
        # The 100-element lexicon matrix reference
        self.lexicon_matrix = lexicon_matrix

    def map_scene_to_vector(self, scene: SceneBlock) -> Dict[str, float]:
        """Analyzes scene content and calculates vector weights against the lexicon matrix."""
        combined_text = " ".join(scene.content).lower()
        coordinates: Dict[str, float] = {}

        for element_key, baseline_vector in self.lexicon_matrix.items():
            # Simple frequency/keyword heuristic placeholder for matrix alignment
            frequency = sum(combined_text.count(word) for word in element_key.lower().split('_'))
            weight = float(frequency) / max(len(scene.content), 1) * 100.0
            coordinates[element_key] = round(weight, 4)

        scene.vector_coordinates = coordinates
        return coordinates

    def map_entire_script(self, scenes: List[SceneBlock]) -> List[SceneBlock]:
        """Maps all scenes in the script to the 100-element grid."""
        for scene in scenes:
            self.map_scene_to_vector(scene)
        return scenes
