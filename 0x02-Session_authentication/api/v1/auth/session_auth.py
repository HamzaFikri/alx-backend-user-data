#!/usr/bin/env python3
"""class session"""
from api.v1.auth.auth import Auth
from uuid import uuid4
from api.v1.views.users import User


class SessionAuth(Auth):
    """inherits Auth"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        creates a Session ID for a user_id:
        Return None if user_id is None
        Return None if user_id is not a string
        Otherwise:
        - Generate a session ID usiing uuid$() like id in Base
        - use theID as key dictioney for user_id_by_session_id,
            the value must be user_id
        - Return session ID
        The same user_id can have multiple Session ID - indeed,
        the user_id is the value in the dictionary user_id_by_session_id
        """
        if user_id is None:
            return None
        elif type(user_id) != str:
            return None
        else:
            session_id = str(uuid4())
            self.user_id_by_session_id[session_id] = user_id
            return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        returns a User ID bases on Session ID:
        Return None if session_id is None
        Return None if session_id is not a string
        Return the value (the User ID) for the key,
         session_id in the dictionary user_id_by_session_id.
        use .get() built-in for accessing in a dictionary,
         a value based on key
        """

        if session_id is None:
            return None
        if type(session_id) != str:
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        returns a User instance based on a cookie value
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """
        deletes the user session/logout
        """
        if request is None:
            return False
        cookie = self.session_cookie(request)
        if cookie is None or\
                self.user_id_for_session_id(cookie) is None:
            return False

        del self.user_id_by_session_id[cookie]
        return True
