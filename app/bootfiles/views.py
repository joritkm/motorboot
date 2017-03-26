from flask import request, current_app, make_response, jsonify,\
        send_from_directory
from . import bp as bootfiles
from ..models import Host


@bootfiles.route('/query')
def boot_query():
    hostname = request.args.get('hostname')
    host = Host.query.filter_by(hostname=hostname).first_or_404()
    t = host.target.lower() + '.ipxe'
    return send_from_directory('static', filename=t)
