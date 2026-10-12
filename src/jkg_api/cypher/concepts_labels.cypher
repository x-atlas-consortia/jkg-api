// used by concepts/<concept_id>/semantic_types endpoint

WITH $concept_id AS concept_id
MATCH (c:Concept{id:concept_id})
RETURN DISTINCT labels(c) AS concept_labels