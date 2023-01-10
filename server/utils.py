from flask import jsonify,json

def make_response(data=None, key="message"):
    response = dict()
    if data:
        response[key] = data
    try:
        return jsonify(response)
    except:
        return json.dumps(response, default=str)

def field_must_be_type(field, type):
    if not isinstance(field, type):
        return f"{field} must be a {type}."


def field_required(field): return f"{field} is required."
