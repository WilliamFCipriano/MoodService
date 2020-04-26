class User:
    """Represents a single MoodService user"""

    def __init__(self, int_id, username, password, last_submission, streak_days):
        self.int_id = int_id
        self.username = username
        self.password = password
        self.last_submission = last_submission
        self.streak_days = streak_days

    def __eq__(self, other):
        if self.int_id == other.int_id:
            return True
        return False
