from flask import jsonify


def make_response(data=None, key="message"):
    response = dict()
    if data:
        response[key] = data

    return jsonify(response)


def field_must_be_type(field, type):
    if not isinstance(field, type):
        return f"{field} must be a {type}."


def field_required(field): return f"{field} is required."

def dup_message(value): return f"Duplicate entry for {value}."
