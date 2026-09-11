// Used by the codes/<code_id>/terms endpoint.

WITH
  $code AS code,
  $term_type AS term_type
MATCH (t:Term)<-[r:CODE {codeid:code}]-(c:Concept)
WHERE CASE WHEN term_type=[] THEN 1=1 ELSE r.tty IN term_type END
WITH DISTINCT
  r.codeid AS code_id,
  t.id AS term_string,
  r.tty AS term_type
WITH code_id, COLLECT({term:term_string,term_type:term_type}) AS code_terms
RETURN {code:code_id,terms:code_terms} AS terms