from typing import Dict, List, Any
from vellum_grid.core.sorter import LuxurySorterEngine
from vellum_grid.core.lex_classifier import LexicalClassificationOrganiser

class RecursiveVectorSorter:
    """Attaches directly to the luxury sorter, executing a recursive vector pass into the LexClassification organiser to maintain absolute structural hierarchy."""

    @staticmethod
    def process_and_organise(registry: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Sorts entities through the luxury engine and recursively vector-maps them into the LexicalClassificationOrganiser."""
        sorted_entities = LuxurySorterEngine.sort_entities(registry)
        
        # Prepare wrapped registry for classification mapping
        wrapped_registry = []
        for entity in sorted_entities:
            wrapped_registry.append({
                "category": entity.get("category", "Absolute Luxury Core"),
                **entity
            })

        return LexicalClassificationOrganiser.classify_and_organise(wrapped_registry)
