from flask import Blueprint, jsonify, current_app, make_response  #, request
from utils.neo4j_logic import codes_code_id_codes_get_logic,codes_code_id_concepts_get_logic
from utils.http_error_string import get_404_error_string, validate_query_parameter_names, \
    validate_parameter_value_in_enum, validate_param_string_chars, validate_code_format
from utils.http_parameter import parameter_as_list

codes_blueprint = Blueprint('codes', __name__, url_prefix='/codes')

# S3 redirect functions
from utils.s3_redirect import redirect_if_large

codes_blueprint = Blueprint('codes', __name__, url_prefix='/codes')

@codes_blueprint.route('/<code_id>/codes', methods=['GET'])
def codes_code_id_codes_get(code_id):
    """Returns a list of code rels that share concept with the specified code_id.
    Optional parameter: sab: list of SABs

    :param code_id: The code identifier
    :type code_id: str
    """

    # Validate code_id parameter.
    err = validate_code_format(param_name='code_id', param_value=code_id)
    if err != 'ok':
        return make_response(err, 400)

    # Validate sab parameter.
    err = validate_query_parameter_names(parameter_name_list=['sab'])
    if err != 'ok':
        return make_response(err, 400)

    # Obtain a list of sab parameter values.
    sab = parameter_as_list(param_name='sab')
    # Validate parameter values against whitelist.
    err = validate_param_string_chars(param_name='sab', param_values=sab)
    if err != 'ok':
        return make_response(err, 400)

    neo4j_instance = current_app.neo4jConnectionHelper.instance()

    result = codes_code_id_codes_get_logic(neo4j_instance, code_id, sab)
    if result is None or result == []:
        # Empty result
        err = get_404_error_string(prompt_string='No CODE rels sharing the Concept linked to the Code specified',
                                   custom_request_path=f"'codeid' = '{code_id}'",
                                   timeout = neo4j_instance.timeout)
        return make_response(err, 404)


    return redirect_if_large(resp=result)

@codes_blueprint.route('/<code_id>/concepts', methods=['GET'])
def codes_code_id_concepts_get(code_id):
    """Returns a list of concepts linked to the specified Code node.

    :param code_id: The code identifier
   """

    # Validate code_id parameter.
    err = validate_code_format(param_name='code_id', param_value=code_id)
    if err != 'ok':
        return make_response(err, 400)

    neo4j_instance = current_app.neo4jConnectionHelper.instance()
    result = codes_code_id_concepts_get_logic(neo4j_instance, code_id)

    if result is None or result == []:
        # Empty result
        err = get_404_error_string(prompt_string='No Concepts linked to the code specified',
                                   custom_request_path=f"'code_id' = '{code_id}'",
                                   timeout = neo4j_instance.timeout)
        return make_response(err, 404)

    return redirect_if_large(resp=result)