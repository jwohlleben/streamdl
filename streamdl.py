#!/usr/bin/python3

"""
streamdl downloads streams from m3u8 files
"""

import subprocess
import requests
import logging
import random
import m3u8
import time
import sys
import os

from alive_progress import alive_bar

# Setup logger
logger = logging.getLogger(__name__)
logging.basicConfig()

# Ensure, that all modules can be found
sys.path.insert(0, os.path.dirname(__file__))

from modules.myargparser import parse_args
from modules.headers import headers
from modules.url import is_url

args = parse_args(headers)

# Change verbosity level based on args
if args.verbosity == 0:
    logger.setLevel(logging.WARNING)
elif args.verbosity == 1:
    logger.setLevel(logging.INFO)
else:
    logger.setLevel(logging.DEBUG)


def main_loop():
    """This is the main proram"""
    logger.info('Downloading playlist...')
    logger.info(f'GET {args.stream_url}')
    try:
        response = requests.get(args.stream_url, headers=headers)
    except requests.ConnectionError:
        logger.error(f'Could not connect to {args.stream_url}')
        sys.exit(1)

    if response.status_code != 200:
        logger.error('Could not get playlist')
        sys.exit(1)

    playlist = m3u8.loads(response.text)
    max_segments = len(playlist.segments)

    # Initialize random generator
    random.seed()

    logger.info('Downloading segments...')

    with open(args.output, 'wb') as file:
        with alive_bar(len(playlist.segments), calibrate=50) as bar:
            for i, segment in enumerate(playlist.segments):
                if is_url(segment.uri):
                    segment_url = segment.uri
                else:
                    segment_url = args.base_url + segment.uri

                # Sleep, if specified
                sleep_min, sleep_max = args.sleep
                sleep_sec = random.uniform(sleep_min, sleep_max)
                logger.debug(f'Sleep {sleep_sec:.2} sec')
                time.sleep(sleep_sec)

                logger.info(f'GET {segment_url}')

                try:
                    response = requests.get(segment_url, headers=headers)
                except requests.ConnectionError:
                    logger.info(f'Could not connect to {segment_url}')
                    sys.exit(1)

                if response.status_code != 200:
                    logger.info(f'Aborting. Could not find "{segment_url}"')
                    sys.exit(1)

                file.write(response.content)
                bar()

    logger.info('Done downloading')

    # Convert file, if requested
    if args.convert_format != '':
        logger.info('Converting file...')

        if args.convert_format == 'mp3':
            command = [
                'ffmpeg',
                '-i', args.output,
                '-vn',
                '-ar', '44100',
                '-ac', '2',
                '-b:a', '192k',
                args.output + '.mp3'
            ]
        elif args.convert_format == 'mp4':
            command = [
                'ffmpeg',
                '-i', args.output,
                '-c:v', 'libx264',
                '-c:a', 'aac',
                args.output + '.mp4'
            ]

        try:
            subprocess.run(command)
            logger.info('Done converting')
        except:
            logger.error('Could not convert file. Is ffmpeg installed?')

if __name__ == '__main__':
    try:
        main_loop()
    except KeyboardInterrupt:
        print('Bye')
        sys.exit(0)
