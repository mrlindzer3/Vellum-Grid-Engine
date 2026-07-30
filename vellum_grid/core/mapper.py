import hashlib
from typing import Dict, List, Any

class LexiconMapper:
    """Projects scene content against the 100-element lexicon matrix to compute semantic vector coordinates."""
    
    VECTOR_DIMENSIONS = 100

    @classmethod
    def compute_lexicon_vector(cls, content: str) -> Dict[str, float]:
        """Generates deterministic pseudo-vector coordinates for a scene based on its text."""
        vector = {}
        # Base deterministic generation using content hashing for robust offline reproducibility
        for i in range(1, cls.VECTOR_DIMENSIONS + 1):
            dim_key = f"lex_{i:03d}"
            # Create a localized hash for each dimension
            hash_input = f"{dim_key}:{content}".encode('utf-8')
            digest = hashlib.sha256(hash_input).hexdigest()
            # Normalize hash into a float coordinate between -1.0 and 1.0
            val = (int(digest[:8], 16) / 0xFFFFFFFF) * 2.0 - 1.0
            vector[dim_key] = round(val, 4)
        return vector

    @classmethod
    def map_scenes(cls, parsed_scenes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        mapped_scenes = []
        for scene in parsed_scenes:
            vector_coords = cls.compute_lexicon_vector(scene.get("content", ""))
            mapped_scene = {
                "scene_number": scene["scene_number"],
                "slugline": scene["slugline"],
                "vector_coordinates": vector_coords,
                "variance_score": 0.0  # Placeholder for analyzer step
            }
            mapped_scenes.append(mapped_scene)
        return mapped_scenes
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
