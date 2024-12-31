"""
This module contains url helper functions
"""

from urllib.parse import urlparse

def is_url(url):
    """Check if a string is a valid url"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False
