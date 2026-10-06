// Used by the /concepts/{concept_id}/concepts endpoint

// The function that loads this query will replace concept_id with a value
// from path parameter of the call to the endpoint.

WITH $concept_id AS concept_id
MATCH (c:Concept{id:concept_id})<-[r]-(c2:Concept)
WITH
r.sab AS rsab,
type(r) AS typer,
c2.id as c2id,
c2.pref_term AS prefterm
ORDER BY c2.id
WITH
{
concept:c2id,
prefterm:prefterm,
relationship:typer,
sab:rsab
} AS concept
RETURN COLLECT(DISTINCT concept) AS concepts