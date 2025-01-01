#!/usr/bin/python3

"""
streamdl downloads streams from m3u8 files
"""

import requests
import logging
import ffmpeg
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


def download_playlist(playlist_url, headers):
    """Returns the downloaded playlist from a url"""

    logger.info(f'GET {playlist_url}')

    try:
        response = requests.get(playlist_url, headers=headers)
    except requests.ConnectionError:
        logger.error(f'Could not connect to {playlist_url}')
        sys.exit(1)

    if response.status_code != 200:
        logger.error('Could not get playlist')
        sys.exit(1)

    return m3u8.loads(response.text)


def download_segment(segment_url, headers):
    """Returns the downloaded segment content"""

    logger.info(f'GET {segment_url}')

    try:
        response = requests.get(segment_url, headers=headers)
    except requests.ConnectionError:
        logger.info(f'Could not connect to {segment_url}')
        sys.exit(1)

    if response.status_code != 200:
        logger.info(f'Aborting. Could not find "{segment_url}"')
        sys.exit(1)

    return response.content


def main_loop():
    """This is the main program"""

    logger.info('Downloading playlist...')
    playlist = download_playlist(args.stream_url, headers)
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

                # Download segment and write to file
                segment_content = download_segment(segment_url, headers)
                file.write(segment_content)

                bar()

    logger.info('Done downloading')

    # Convert file, if requested
    if args.convert_format != '':
        logger.info('Converting file...')

        if args.convert_format == 'mp3':
            ffmpeg.input(args.output).output(args.output + '.mp3', vn=None, ar=44100, ac=2, **{'b:a': '192k'}).run()
        elif args.convert_format == 'mp4':
            ffmpeg.input(args.output).output(args.output + '.mp4', vcodec='libx264', acodec='aac').run()

        logger.info('Done converting')


if __name__ == '__main__':
    try:
        main_loop()
    except KeyboardInterrupt:
        print('Bye')
        sys.exit(0)
