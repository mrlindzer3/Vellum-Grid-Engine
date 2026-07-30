# vellum_grid/core/parser.py
import re
from typing import List, Dict, Any

class SceneBlock:
    def __init__(self, scene_number: int, slugline: str, content: List[str]):
        self.scene_number = scene_number
        self.slugline = slugline
        self.content = content
        self.vector_coordinates: Dict[str, float] = {}

class ScriptParser:
    def __init__(self, raw_script: str):
        self.raw_script = raw_script
        self.scenes: List[SceneBlock] = []

    def parse_scenes(self) -> List[SceneBlock]:
        """Segments raw script text into structured scene blocks based on sluglines."""
        slugline_pattern = re.compile(r'^(INT\.|EXT\.|EST\.|INT\./EXT\.)\s+.+', re.IGNORECASE)
        
        lines = self.raw_script.split('\n')
        current_slugline = "UNKNOWN_SLUGLINE"
        current_content: List[str] = []
        scene_count = 1

        for line in lines:
            if slugline_pattern.match(line.strip()):
                if current_content:
                    self.scenes.append(SceneBlock(scene_count, current_slugline, current_content))
                    scene_count += 1
                    current_content = []
                current_slugline = line.strip()
            else:
                current_content.append(line)
        
        if current_content:
            self.scenes.append(SceneBlock(scene_count, current_slugline, current_content))
            
        return self.scenes
