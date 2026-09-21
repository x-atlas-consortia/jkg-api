// Called by the /concepts/<id>/codes endpoint

WITH
  $concept_id AS concept_id,
  $sablist AS sablist
// filter on concept_id
MATCH(c:Concept{id:concept_id})-[r:CODE]->(t:Term)
WHERE
// filter on SABs of CODE rels by the SAB part of the codeid
  CASE
    WHEN sablist=[] THEN 1=1 ELSE SPLIT(r.codeid,':')[0] IN sablist END
WITH r.codeid AS code
  ORDER BY r.codeid
RETURN DISTINCT code
