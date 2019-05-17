# fireapi/controllers.py

from flask import Blueprint, jsonify
# from flask_restplus import Api
from flask_login import login_required
from hackathon.mod_fireapi.exec_untrusted import exec_untrusted

mod_fireapi = Blueprint('fireapi', __name__, url_prefix='/fireapi')


# http://localhost:5000/fireapi/coderesult/print%28%27hello%27%29
@mod_fireapi.route("/coderesult/<code>", methods=['GET'])
@login_required
def get_response(code):
    response_str = str(exec_untrusted(code))
    return jsonify({'response': 200, 'results': response_str})

