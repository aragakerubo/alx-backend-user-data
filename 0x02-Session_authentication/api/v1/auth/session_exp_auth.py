#!/usr/bin/env python3
"""Session Exp Auth module
"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from os import getenv


class SessionExpAuth(SessionAuth):
    """Session Exp Auth class
    """
    def __init__(self):
        """Constructor
        """
        session_duration = getenv('SESSION_DURATION')
        if session_duration:
            try:
                self.session_duration = int(session_duration)
            except Exception:
                self.session_duration = 0
        else:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Create a new session
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Return a User ID based on a Session ID
        """
        if session_id is None:
            return None
        session_dictionary = self.user_id_by_session_id.get(session_id)
        if session_dictionary is None:
            return None
        user_id = session_dictionary.get("user_id")
        if user_id is None:
            return None
        if self.session_duration <= 0:
            return user_id
        created_at = session_dictionary.get("created_at")
        if created_at is None:
            return None
        if (created_at + timedelta(seconds=self.session_duration) <
                datetime.now()):
            return None
        return user_id
