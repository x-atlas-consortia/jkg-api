// Used by the /codes/<code_id>/concepts endpoint

WITH $code AS code
MATCH (t:Term)<-[r:CODE {codeid:code}]-(c:Concept)
WITH DISTINCT c.id AS conceptid
ORDER BY c.id
WITH {concept:conceptid} AS concept
RETURN COLLECT(DISTINCT concept) AS concepts