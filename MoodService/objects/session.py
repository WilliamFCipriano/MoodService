class Session:
    """A session describes a users permission to use the application"""

    def __init__(self, user_int_id, session_id, session_token):
        self.user_int_id = user_int_id
        self.session_id = session_id
        self.session_token = session_token

    def __eq__(self, other):
        if self.session_id == other.session_id:
            return True
        return False