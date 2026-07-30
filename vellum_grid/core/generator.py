import random
from vellum_grid.data.lexicon_matrix import LEXICON_MATRIX

class VellumGridEngine:
    def __init__(self):
        self.matrix = LEXICON_MATRIX

    def _check_cadence(self, name: str) -> bool:
        """Ensures phonetic balance (2 to 6 vowel sounds per compound name)."""
        vowels = "aeiouy"
        syllables = sum(1 for char in name.lower() if char in vowels)
        return 2 <= syllables <= 6

    def generate_element(self, category: str = None) -> dict:
        """Pulls a structured nomenclature pairing along with its sub-elements."""
        if not category or category not in self.matrix:
            category = random.choice(list(self.matrix.keys()))
            
        elements_dict = self.matrix[category]["elements"]
        base_name = random.choice(list(elements_dict.keys()))
        sub_elements = elements_dict[base_name]
        
        return {
            "category": category,
            "nomenclature": base_name,
            "sub_elements": sub_elements,
            "description": self.matrix[category]["description"]
        }

    def generate_tracklist(self, category: str, count: int = 5) -> list:
        """Generates a sequentially balanced set of names for albums or game chapters."""
        elements_dict = self.matrix[category]["elements"]
        keys = list(elements_dict.keys())
        selected = random.sample(keys, min(count, len(keys)))
        return selected
