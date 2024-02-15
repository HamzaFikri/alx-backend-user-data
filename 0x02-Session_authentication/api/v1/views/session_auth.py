#!/usr/bin/env python3
"""Module for Session Auth routes
"""
import os
from api.v1.views import app_views
from api.v1.views import User
from flask import abort, jsonify, request
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """ login route"""
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None or email == "":
        return jsonify({"error": "email missing"}), 400
    if password is None or password == "":
        return jsonify({"error": "password missing"}), 400
    rst = User().search({"email": email})
    if len(rst) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    user: User = rst[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    sessin_id = auth.create_session(user.id)
    logger.info(sessin_id)
    out = jsonify(user.to_json())
    out.set_cookie(os.getenv('SESSION_NAME'), sessin_id)
    return out


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def Logout():
    """ logout """
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)