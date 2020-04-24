class User:
    """Represents a single MoodService user."""

    def __init__(self, int_id, username, password):
        self.int_id = int_id
        self.username = username
        self.password = password
