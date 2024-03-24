"""User state tracking module."""

# Simple in-memory user state tracking
# will be replaced with django api
user_states = {}


def get_user_state(chat_id):
    """Retrieves the authentication state of a user."""
    if chat_id in user_states:
        return user_states[chat_id]
    return "UNAUTHENTICATED"  # Default for new users


def set_user_state(chat_id, state):
    """Updates the authentication state of a user."""
    user_states[chat_id] = state
