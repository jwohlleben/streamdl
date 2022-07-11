"""
This module contains the log for logging
"""

import sys
from datetime import datetime

verbosity = 0
v_level = 1
vv_level = 2

def get_prefix():
    """Returns a prefix for the log functions using an info_char"""
    current_dt = datetime.now()
    return '[' + current_dt.strftime('%Y-%m-%d %H:%M:%S') + ']'

def should_print(level):
    """Returns true if the log level is high enough for printing"""
    return verbosity >= level

def v(*args, prefix=True, **kwargs):
    """Function for verbose printing"""
    if not should_print(v_level):
        return
    if prefix:
        print(get_prefix() + ' ', end='')
    print(*args, **kwargs)

def vv(*args, prefix=True, **kwargs):
    """Function for very verbose printing"""
    if not should_print(vv_level):
        return
    if prefix:
        print(get_prefix() + ' ', end='')
    print(*args, **kwargs)

def error(*args, prefix=True, **kwargs):
    """Function for error printing"""
    if prefix:
        print(get_prefix() + ' ', file=sys.stderr, end='')
    print(*args, file=sys.stderr, **kwargs)
