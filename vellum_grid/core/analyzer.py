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
