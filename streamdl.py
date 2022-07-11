#!/usr/bin/python3

"""
streamdl downloads streams from m3u8 files
"""

import random
import time
import sys
import os

# Ensure, that all modules can be found
sys.path.insert(0, os.path.dirname(__file__))

import modules.mylog as log
from modules.myargparser import parse_args
from modules.headers import headers

try:
    import requests
    import m3u8
except ModuleNotFoundError as e:
    print(f'{e}. Please install the module (e.g. using pip)')
    sys.exit(1)

args = parse_args(headers)
log.verbosity = args.verbosity

def main_loop():
    """This is the main proram"""
    log.v('Downloading playlist...')
    log.vv('GET', args.stream_url)
    try:
        response = requests.get(args.stream_url, headers=headers)
    except requests.ConnectionError:
        log.error(f'Could not connect to {args.stream_url}')
        sys.exit(1)

    if response.status_code != 200:
        log.error('Could not get playlist')
        sys.exit(1)

    playlist = m3u8.loads(response.text)
    max_segments = len(playlist.segments)

    # Initialize random generator
    random.seed()

    log.v('Downloading segments...')

    old_ts = time.time()
    new_ts = time.time()

    with open(args.output, 'wb') as file:
        for i, segment in enumerate(playlist.segments):
            new_ts = time.time()
            segment_url = args.base_url + segment.uri

            # Print progress every 10 sec
            if abs(new_ts - old_ts) > 10.0:
                progress = int((i / max_segments) * 100)
                log.v(f'Progress: {progress} %')
                old_ts = new_ts

            # Sleep, if specified
            sleep_min, sleep_max = args.sleep
            sleep_sec = random.uniform(sleep_min, sleep_max)
            log.vv(f'Sleep {sleep_sec:.2} sec')
            time.sleep(sleep_sec)

            log.vv('GET', segment_url)

            try:
                response = requests.get(segment_url, headers=headers)
            except requests.ConnectionError:
                log.error(f'Could not connect to {segment_url}')
                sys.exit(1)

            if response.status_code != 200:
                log.error(f'Aborting. Could not find "{segment_url}"')
                sys.exit(1)

            file.write(response.content)

    log.v('Done :)')

if __name__ == '__main__':
    try:
        main_loop()
    except KeyboardInterrupt:
        log.v('Bye')
        sys.exit(0)
