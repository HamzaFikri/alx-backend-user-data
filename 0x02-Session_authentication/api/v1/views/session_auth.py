#!/usr/bin/env python3
"""
Create a new Flask view that handles all routes for the Session authentication.
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from os import getenv
from models.user import User


@app_views.route('/auth_session/login',
                 methods=['POST'], strict_slashes=False)
def login():
    """
    Handles all routes for the Session authentication.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    for user in users:
        if not user.is_valid_password(password):
            return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    """
    WARNING: please import it only where you need it - not on top of the file
    (can generate circular import - and break first tasks of this project)
    """

    user = users[0]

    response = jsonify(user.to_json())
    response.set_cookie(getenv("SESSION_NAME"), auth.create_session(user.id))

    return response


@app_views.route('/api/v1/auth_session/logout',
                 methods=['POST'], strict_slashes=False)
def logout():
    """
    Deletes the user session.
    """
    from api.v1.app import auth

    if not auth.destroy_session(request):
        abort(404)

    return jsonify({}), 200
