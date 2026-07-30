import math
from typing import Dict, List, Any

class NarrativeAnalyzer:
    """Calculates vector variances, structural summaries, and high-variance transition points across scenes."""

    @staticmethod
    def euclidean_distance(v1: Dict[str, float], v2: Dict[str, float]) -> float:
        """Computes Euclidean distance between two semantic vector dictionaries."""
        common_keys = set(v1.keys()).intersection(set(v2.keys()))
        if not common_keys:
            return 0.0
        sum_sq = sum((v1[k] - v2[k]) ** 2 for k in common_keys)
        return round(math.sqrt(sum_sq), 4)

    @classmethod
    def analyze_script(cls, mapped_scenes: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not mapped_scenes:
            return {
                "total_scenes": 0,
                "scenes": [],
                "high_variance_transitions": [],
                "structural_summary": {}
            }

        analyzed_scenes = []
        transitions = []
        vector_magnitudes = []

        for i, scene in enumerate(mapped_scenes):
            current_vector = scene["vector_coordinates"]
            
            # Compute magnitude (Euclidean norm from origin) as a baseline metric
            mag = round(math.sqrt(sum(v ** 2 for v in current_vector.values())), 4)
            vector_magnitudes.append(mag)

            variance_score = 0.0
            if i > 0:
                prev_vector = mapped_scenes[i - 1]["vector_coordinates"]
                variance_score = cls.euclidean_distance(prev_vector, current_vector)
                
                # Flag high-variance transitions (threshold set dynamically based on typical distribution)
                if variance_score > 15.0:
                    transitions.append(scene["scene_number"])

            updated_scene = scene.copy()
            updated_scene["variance_score"] = variance_score
            analyzed_scenes.append(updated_scene)

        avg_magnitude = sum(vector_magnitudes) / len(vector_magnitudes) if vector_magnitudes else 0.0

        structural_summary = {
            "mean_vector_magnitude": round(avg_magnitude, 4),
            "max_variance_jump": max((s["variance_score"] for s in analyzed_scenes), default=0.0),
            "pacing_index": round(sum(s["variance_score"] for s in analyzed_scenes) / len(analyzed_scenes), 4)
        }

        return {
            "total_scenes": len(analyzed_scenes),
            "scenes": analyzed_scenes,
            "high_variance_transitions": transitions,
            "structural_summary": structural_summary
        }
# vellum_grid/core/analyzer.py
from typing import List, Dict, Any
from vellum_grid.core.parser import SceneBlock

class MatrixAnalyzer:
    def __init__(self, scenes: List[SceneBlock]):
        self.scenes = scenes

    def calculate_tonal_drift(self) -> List[Dict[str, Any]]:
        """Evaluates variance and drift across scene vector coordinates to flag pacing or thematic anomalies."""
        drift_report = []
        
        for i in range(1, len(self.scenes)):
            prev_scene = self.scenes[i - 1]
            curr_scene = self.scenes[i]
            
            # Calculate Euclidean distance or delta between consecutive scene vectors
            delta_score = 0.0
            all_keys = set(prev_scene.vector_coordinates.keys()).union(curr_scene.vector_coordinates.keys())
            
            for key in all_keys:
                val_prev = prev_scene.vector_coordinates.get(key, 0.0)
                val_curr = curr_scene.vector_coordinates.get(key, 0.0)
                delta_score += abs(val_curr - val_prev)
            
            drift_report.append({
                "transition": f"Scene {prev_scene.scene_number} -> Scene {curr_scene.scene_number}",
                "slugline_from": prev_scene.slugline,
                "slugline_to": curr_scene.slugline,
                "variance_score": round(delta_score, 4)
            })
            
        return drift_report

    def generate_structural_summary(self) -> Dict[str, Any]:
        """Summarizes the entire script's traversal across the 100-element matrix."""
        total_scenes = len(self.scenes)
        drift_data = self.calculate_tonal_drift()
        
        peak_shifts = sorted(drift_data, key=lambda x: x['variance_score'], reverse=True)[:3]

        return {
            "total_scenes": total_scenes,
            "high_variance_transitions": peak_shifts,
            "status": "Matrix convergence complete"
        }
