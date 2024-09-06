#!/usr/bin/env python3
""" Session DB Auth
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta
from os import getenv


class SessionDBAuth(SessionExpAuth):
    """ Session DB Auth class
    """
    def create_session(self, user_id=None):
        """ create session
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        UserSession.save_to_file()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ user id for session id
        """
        if session_id is None:
            return None
        user_sessions = UserSession.search({'session_id': session_id})
        if not user_sessions:
            return None
        user_session = user_sessions[0]
        if user_session is None:
            return None
        if user_session.created_at + timedelta(seconds=self.session_duration) \
                < datetime.now():
            return None
        return user_session.user_id

    def destroy_session(self, request=None):
        """ destroy session
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_sessions = UserSession.search({'session_id': session_id})
        if user_sessions:
            for user_session in user_sessions:
                user_session.remove()
                UserSession.save_to_file()
                return True
        return False
