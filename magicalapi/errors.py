"""
this file contains all of the errors in this package.
"""


class APIServerError(Exception):
    """this exception raise when the API server not respond."""


class APIServerTimedout(Exception):
    """this exception raise when the API server response timed out."""
