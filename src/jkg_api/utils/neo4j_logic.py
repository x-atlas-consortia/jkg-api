"""
neo4j_logic
Functions that execute Cypher queries against a neo4j instance of
JKG.

"""
import logging
import re
from typing import List
import os
import json

# For handling configurable timeouts
from werkzeug.exceptions import GatewayTimeout

# For serializing neo4j Path objects
from neo4j.graph import Path

from pathlib import Path

import neo4j

logging.basicConfig(format='[%(asctime)s] %(levelname)s in %(module)s:%(lineno)d: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

#--------------------
# UTILITY ROUTINES
# -------------------

def loadquerystring(filename: str) -> str:
    """
    Loads a query string from a file.

    Keeping query strings separate from the Python code:
    1. Separates business logic from the presentation layer.
    2. Eases the transition from neo4j development to API development--in particular, by elminating the need to
         reformat a query string in Python

    :param filename: filename, without path.

    Assumes that the file is in the cypher subdirectory, which is at the same level as the script path.
    When ubkg-api endpoints are called as passthrough from hs-ontology api, the script path is in hs-ontology-api.


    """

    fpath = Path(__file__).resolve().parent.parent
    fpath = os.path.join(fpath,'cypher',filename)
    f = open(fpath, "r")
    query = f.read()
    f.close()
    return query

def format_list_for_query(listquery: list[str], doublequote: bool = False) -> str:

    """
    Converts a list of string values into a comma-delimited, delimited string for use in a Cypher query clause.
    :param listquery: list of string values
    :param doublequote: flag to set the delimiter.

    The default is a single quote; however, when a query
    is the argument for the apoc.timebox function, the delimiter should be double quote.

    Example:
        listquery: ['SNOMEDCT_US', 'HGNC']
        return:
            doublequote = False: "'SNOMEDCT_US', 'HGNC'"
            doublequote = True: '"SNOMEDCT_US","HGNC"'

    """
    if doublequote:
        return ', '.join('"{0}"'.format(s) for s in listquery)
    else:
        return ', '.join("'{0}'".format(s) for s in listquery)


# --------------------
# codes ENDPOINT ROUTINES
# -------------------

def codes_code_id_codes_get_logic(neo4j_instance, codeid: str, sab: List[str]) -> List[dict]:
    """
    Called by the /codes/<code_id>/codes endpoint.

    Returns the set of CODE relationships that share Concept links with the specified code_id.
    :param neo4j_instance: neo4j connection
    :param code_id: CodeID for the Code node, in format <SAB>:<CODE>
    :param sab: optional list of SABs from which to select codes that share links to the Concept node linked to the
    Code node

    # Assumption: the parameters code_id and sab were validated by the controller.
    """
    result: list[dict] = []

    # Load Cypher query template from file.
    querytxt: str = loadquerystring(filename='codes_codes.cypher')

    # BUILD QUERY PARAMS

    # Required filter on code_id.
    params: dict = {"code": codeid,"sablist": sab}

    # Instantiate the query with the configured timeout.
    query = neo4j.Query(text=querytxt, timeout=neo4j_instance.timeout)

    with (neo4j_instance.driver.session() as session):
        try:
            # Execute the query with neo4j params
            recds: neo4j.Result = session.run(query, **params)

            for record in recds:
                result.append(record.get('codes'))

        except neo4j.exceptions.ClientError as e:
            # If the error is from a timeout, raise a HTTP 408.
            if e.code == 'Neo.ClientError.Transaction.TransactionTimedOutClientConfiguration':
                raise GatewayTimeout

    # Because of the COLLECTS in the Cypher query, the response is a list that contains a list.
    # Return the inner list.
    if len(result)==0:
        return result
    else:
        return result[0]

def codes_code_id_concepts_get_logic(neo4j_instance, code_id: str) -> List[dict]:

    """
    Called by the /codes/<code_id>/concepts endpoint.
    Returns information on the Concept node that links to the specified Code node.
    :param neo4j_instance: neo4j connection
    :param code_id: CodeID for the Code node, in format <SAB>:<CODE>

    # Assumption: the parameter code_id was validated by the controller.

    """
    result = []

    # Load Cypher query template from file.
    querytxt: str = loadquerystring(filename='codes_concepts.cypher')

    # BUILD QUERY PARAMS

    # Required filter on code_id.
    params: dict = {"code": code_id}

    # Instantiate the query with the configured timeout.
    query = neo4j.Query(text=querytxt, timeout=neo4j_instance.timeout)

    with neo4j_instance.driver.session() as session:
        try:

            # Execute the query with neo4j params
            recds: neo4j.Result = session.run(query, **params)

            for record in recds:
                result.append(record.get('concepts'))


        except neo4j.exceptions.ClientError as e:
            # If the error is from a timeout, raise a HTTP 408.
            if e.code == 'Neo.ClientError.Transaction.TransactionTimedOutClientConfiguration':
                raise GatewayTimeout

    # Because of the COLLECTS in the Cypher query, the response is a list that contains a list.
    # Return the inner list.
    if len(result) == 0:
        return result
    else:
        return result[0]