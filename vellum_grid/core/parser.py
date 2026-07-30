import re
from typing import List, Dict, Any

class ScriptParser:
    """Core parser for segmenting unstructured script text into structured scene blocks."""
    
    SLUG_PATTERN = re.compile(
        r'^\s*(INT\.|EXT\.|INT\./EXT\.|I/E)\s+(.+?)(?:\s*-\s*(?:DAY|NIGHT|CONTINUOUS|MORNING|EVENING|LATER))?\s*$',
        re.IGNORECASE | re.MULTILINE
    )

    @classmethod
    def parse_script(cls, script_text: str) -> List[Dict[str, Any]]:
        scenes = []
        matches = list(cls.SLUG_PATTERN.finditer(script_text))
        
        for i, match in enumerate(matches):
            start_idx = match.start()
            end_idx = matches[i + 1].start() if i + 1 < len(matches) else len(script_text)
            
            slugline = match.group(0).strip()
            scene_body = script_text[match.end():end_idx].strip()
            
            scenes.append({
                "scene_number": i + 1,
                "slugline": slugline,
                "content": scene_body
            })
            
        return scenes
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
