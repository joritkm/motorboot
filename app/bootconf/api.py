from flask import request, jsonify, make_response, redirect, url_for,\
        current_app
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
from ..models import Host, HostSchema
from ..auth import auth
from .. import db
from . import bp as bootconf


hschema = HostSchema()


"""
Set up custom logmessages and api-friendly errorhandling
"""
def log_error(host, action):
    action_msg = '{a} Host: {h} with MAC: {m} and Target: {t}. failed'\
        .format(a = action,
                h = host.hostname,
                m = host.hwaddress,
                t = host.target.all()[0] if host.target else ''
               )
    current_app.logger.warning(action_msg)


@bootconf.errorhandler(404)
def not_found_error(error):
    return make_response(jsonify({"error":"Not found"}), 404)


@bootconf.errorhandler(500)
def internal_error(error):
    return make_response(jsonify({"error":"Internal Server Error"}), 500)


@auth.error_handler
def unauthorized():
    """
    return 403 on unauthorized access, in case this ever
    gets used with a browser-based client.
    """
    return make_response(jsonify({"error":"Forbidden"}), 403)


"""
API Endpoints
"""
@bootconf.before_request
@auth.login_required
def before_request():
    """
    Guard all api endpoints
    """
    pass


@bootconf.route('/<string:hostname>')
def get_host(hostname):
    host_query = Host.query.filter_by(hostname=hostname).first_or_404()
    result = jsonify(hschema.dump(host_query).data)
    return result, 200


@bootconf.route('/list')
def get_hostlist():
    host_query = Host.query.all()
    results = jsonify(hschema.dump(host_query, many=True).data)
    return results, 200


@bootconf.route('/new', methods=['POST'])
def post_host():
    raw_dict = request.get_json(force=True)
    host_dict = raw_dict['data']['attributes']
    try:
        hschema.validate(host_dict)
        host = Host(hostname=host_dict['hostname'],
                    hwaddress=host_dict['hwaddress'],
                    target=host_dict['target']
                   )
        host.add(host)
        current_app.logger.info('Added Host: {h} with MAC: {m} and Target: {t}.'\
                .format(h = host.hostname,
                        m = host.hwaddress,
                        t = host.target
                       ))
        query = Host.query.get(host.id)
        results = hschema.dump(query).data
        return jsonify(results), 201
    except ValidationError as verr:
        log_error(host,'Adding')
        resp = jsonify({"error": verr.messages})
        return resp, 403
    except SQLAlchemyError as e:
        db.session.rollback()
        log_error(host,'Adding')
        resp = jsonify({"error": str(e)})
        return resp, 403


@bootconf.route('/edit/<string:hostname>', methods=['PATCH'])
def patch_host(hostname):
    host = Host.query.filter_by(hostname=hostname).first_or_404()
    raw_dict = request.get_json(force=True)
    host_dict = raw_dict['data']['attributes']
    host_was_msg='Edited Host: {h} with MAC: {m} and Target: {t}.'\
            .format(h = host.hostname,
                    m = host.hwaddress,
                    t = host.target
                   )
    try:
        for key, value in host_dict.items():
            hschema.validate({key:value})
            if key == 'target' and not (host.target == value):
                host.target = value
            elif key == 'hostname' and not (host.hostname == value):
                host.hostname = value
            elif key == 'hwaddress' and not (host.hwaddress == value):
                host.hwaddress == value
            host.update()
            host = Host.query.get(host.id)
        host_is_msg='To Host: {h} with MAC: {m} and Target: {t}.'\
                .format(h = host.hostname,
                        m = host.hwaddress,
                        t = host.target
                       )
        current_app.logger.info(host_was_msg + '\n' + host_is_msg)
        response = make_response()
        return response, 205
    except ValidationError as verr:
        log_error(host,'Editing')
        resp = jsonify({"error": verr.messages})
        return resp, 403
    except SQLAlchemyError as e:
        db.session.rollback()
        log_error(host,'Editing')
        resp = jsonify({"error": str(e)})
        return resp, 403


@bootconf.route('/remove/<string:hostname>', methods=['DELETE'])
def delete_host(hostname):
    host = Host.query.filter_by(hostname=hostname).first_or_404()
    try:
        delete = host.delete(host)
        current_app.logger.info('Deleted Host: {h} with MAC: {m} and Target: {t}.'\
                .format(h = host.hostname,
                        m = host.hwaddress,
                        t = host.target
                       ))
        response = make_response()
        return response, 204
    except SQLAlchemyError as e:
        db.session.rollback()
        log_error(host,'Deleting')
        resp = jsonify({"error": str(e)})
        return resp, 403
