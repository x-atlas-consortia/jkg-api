// used by concepts/<concept_id>/semantic_types endpoint

WITH $label_id AS label_id
MATCH (n:Node_Label{node_label:label_id})
RETURN {
node_label:n.node_label,
definition:n.def,
id:n.id,
sab:n.sab} AS semantic_type