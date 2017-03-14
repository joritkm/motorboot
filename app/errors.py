from flask import jsonify
from flask import current_app as app

@app.errorhandler(404)
def not_found(message):
    response = jsonify({'error': 'not found', 'message': message})
    response.status_code = 404
    return response

@app.errorhandler(400)
def bad_request(message):
    response = jsonify({'error': 'bad request', 'message': message})
    response.status_code = 400
    return response

@app.errorhandler(401)
def unauthorized(message):
    response = jsonify({'error': 'unauthorized', 'message': message})
    response.status_code = 401
    return response

@app.errorhandler(403)
def forbidden(message):
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response
