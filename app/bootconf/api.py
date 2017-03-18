from flask import request, jsonify, make_response, redirect, url_for,\
        current_app
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
from ..models import Host, Boottarget, HostSchema
from .. import db
from . import bp as bootconf


hschema = HostSchema()


def log_error(host, action):
    action_msg = '{a} Host: {h} with MAC: {m} and Target: {t}. failed'\
        .format(a = action,
                h = host.hostname,
                m = host.hwaddress,
                t = host.target.all()[0] if host.target else ''
               )
    current_app.logger.warning(action_msg)


@bootconf.route('/<string:hostname>')
def get_host(hostname):
    host_query = Host.query.filter_by(hostname=hostname).first_or_404()
    result = hschema.dump(host_query).data
    return jsonify(result)


@bootconf.route('/list')
def get_hostlist():
    host_query = Host.query.all()
    results = hschema.dump(host_query, many=True).data
    return jsonify(results)


@bootconf.route('/new', methods=['POST'])
def post_host():
    raw_dict = request.get_json(force=True)
    host_dict = raw_dict['data']['attributes']
    try:
        hschema.validate(host_dict)
        host = Host(host_dict['hostname'],host_dict['hwaddress'])
        if host_dict['target']:
            try:
                t = Boottarget.query.\
                        filter_by(name==host_dict['target']).\
                        first_or_404()
                host.target.append(t)
            except SQLAlchemyError as e:
                db.session.rollback()
                resp = jsonify({"error": str(e)})
                return resp, 403
        host.add(host)
        current_app.logger.info('Added Host: {h} with MAC: {m} and Target: {t}.'\
                .format(h = host.hostname,
                        m = host.hwaddress,
                        t = host.target.all()[0] if host.target else ''
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
                    t = host.target.all()[0] if host.target else ''
                   )
    try:
        for key, value in host_dict.items():
            hschema.validate({key:value})
            if key == 'target' and value:
                try:
                    t = Boottarget.query.\
                            filter_by(name==value).\
                            first_or_404()
                    host.target.append(t)
                except SQLAlchemyError as e:
                    db.session.rollback()
                    log_error(host,'Editing')
                    resp = jsonify({"error": str(e)})
                    return resp, 403
            elif key == 'hostname' and not (host.hostname == value):
                host.hostname = value
            elif key == 'hwaddress' and not (host.hwaddress == value):
                host.hwaddress == value
            host.update()
            host = Host.query.get(host.id)
        host_is_msg='To Host: {h} with MAC: {m} and Target: {t}.'\
                .format(h = host.hostname,
                        m = host.hwaddress,
                        t = host.target.all()[0] if host.target else ''
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
                        t = host.target.all()[0] if host.target else ''
                       ))
        response = make_response()
        return response, 204
    except SQLAlchemyError as e:
        db.session.rollback()
        log_error(host,'Deleting')
        resp = jsonify({"error": str(e)})
        return resp, 403
