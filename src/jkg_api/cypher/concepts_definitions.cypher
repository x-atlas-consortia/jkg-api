// used by concepts/<concept_id>/definitions endpoint

WITH $concept_id AS concept_id
MATCH (c:Concept{id:concept_id})-[r:CODE]->(t:Term)
WITH DISTINCT r.def AS def, r.sab AS sab
WHERE r.def <>""
WITH {definition:def, sab:sab} AS definition
order by sab, def
RETURN COLLECT(DISTINCT definition) AS definitions