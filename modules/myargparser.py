"""
This file contains the argument parser with all arguments
"""

import sys
import argparse
from datetime import datetime

parser = argparse.ArgumentParser()

timestamp = int(datetime.timestamp(datetime.now()))
DEFAULT_OUTFILE = 'download' + str(timestamp) + '.ts'

parser.add_argument(
    help='url to a stream file, e.g. https://somewebsite.com/epicstream/stream.m3u8',
    metavar='m3u8_stream',
    dest='stream_url',
)

parser.add_argument(
    '-b',
    '--base-url',
    help='overwrites the default URL for downloading, e.g. https://somewebsite.com/epicstream/',
    metavar='base_url',
    dest='base_url',
)

parser.add_argument(
    '-o',
    '--output',
    default=DEFAULT_OUTFILE,
    help='downloads to the given outfile',
    metavar='outfile',
    dest='output',
)

parser.add_argument(
    '-a',
    '--add-header',
    action='append',
    default=[],
    help='adds or overwrites an existing header based on the headers.py file',
    metavar='header:value',
    dest='add_headers',
)

parser.add_argument(
    '-r',
    '--remove-header',
    action='append',
    default=[],
    help='removes an existing header based on the headers.py file',
    metavar='header',
    dest='remove_headers',
)

parser.add_argument(
    '-s',
    '--sleep',
    default=(0,0),
    help='sleeps a fixed time sec or sleeps random in [minsec;maxsec] between requests',
    metavar='sec|minsec-maxsec',
    dest='sleep',
)

parser.add_argument(
    '-v',
    '--verbose',
    action='count',
    default=0,
    help='shows progress, use -vv for maximum verbosity',
    dest='verbosity',
)

parser.add_argument(
    '--version',
    action='version',
    version='%(prog)s 1.0'
)

def parse_args(headers):
    """Parses and prepares the args and headers"""
    args = parser.parse_args()

    # Set base_url if no --base-url is specified
    if args.base_url is None:
        parts = args.stream_url.rsplit('/', 1)
        if len(parts) != 2:
            print('Malformed base url')
            sys.exit(1)
        args.base_url = parts[0] + '/'

    # Handle --add-headers
    for header in args.add_headers:
        parts = header.split(':', 1)
        if len(parts) != 2:
            print(f'Malformed header "{header}"')
            sys.exit(1)
        headers[parts[0]] = parts[1]

    # Handle --remove-headers
    for header in args.remove_headers:
        try:
            del headers[header]
        except KeyError:
            print(f'Could not remove non existing header "{header}"')
            sys.exit(1)

    # Handle --sleep
    if args.sleep != (0,0):
        sleep_min = 0
        sleep_max = 0
        try:
            sleep_sec = int(args.sleep)
            sleep_min = sleep_sec
            sleep_max = sleep_sec
        except ValueError:
            parts = args.sleep.split('-')
            if len(parts) != 2:
                print('Malformed sleep interval')
                sys.exit(1)
            try:
                sleep_min = float(parts[0])
                sleep_max = float(parts[1])
            except ValueError:
                print('Malformed sleep interval')
                sys.exit(1)

        if sleep_min < 0 or sleep_max < 0:
            print('Invalid sleep interval (< 0)')
            sys.exit(1)
        if sleep_min > sleep_max:
            print('Invalid sleep interval (minsec > maxsec)')
            sys.exit(1)

        args.sleep = (sleep_min, sleep_max)

    return args
