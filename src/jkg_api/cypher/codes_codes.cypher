// Used by the codes/codes endpoint.

WITH
  $code AS code,
  $sablist AS sablist
MATCH
	(t:Term)<-[r:CODE{codeid:code}]-
	(c:Concept)-[r2:CODE]->(t2:Term)
WHERE
	r2.codeid<>r.codeid
	AND CASE WHEN sablist=[] THEN 1=1 ELSE SPLIT(r2.codeid,':')[0] IN sablist END
WITH DISTINCT
	r2.codeid AS codeid,
	r2.sab AS sab,
  c.id AS cui
ORDER BY r2.codeid

WITH {code: codeid, sab:sab, concept:cui} AS code
RETURN COLLECT(DISTINCT code) AS codes