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


def get_url(url, headers):
    """Performs a get request and returns the response"""
    logger.info(f'GET {url}')

    try:
        response = requests.get(url, headers=headers)
    except requests.ConnectionError:
        print(f'Could not connect to {url}')
        sys.exit(1)

    if response.status_code != 200:
        print(f'Aborting. Could not find "{url}"')
        sys.exit(1)

    return response


def choose_url(base_url, uri):
    """Chooses the new url based on the uri"""
    if is_url(uri):
        return uri
    else:
        return base_url + uri


def download_stream_segments(stream, old_ts=None):
    """Download all stream segments or segments, that are newer than old_ts"""
    with open(args.output, 'ab') as file:
            with alive_bar(len(stream.m3u8.segments), calibrate=50) as bar:
                for i, segment in enumerate(stream.m3u8.segments):
                    # Skip old timestamps, if specified
                    if old_ts != None and segment.program_date_time <= old_ts:
                        bar(skipped=True)
                        continue

                    segment_url = choose_url(stream.base, segment.uri)

                    # Sleep, if specified
                    sleep_min, sleep_max = args.sleep
                    sleep_sec = random.uniform(sleep_min, sleep_max)
                    logger.debug(f'Sleep {sleep_sec:.2} sec')
                    time.sleep(sleep_sec)

                    # Download segment and write to file
                    segment_content = get_url(segment_url, headers).content
                    file.write(segment_content)

                    bar()


class MyStream:
    """Wrapper class for streams"""

    def __init__(self, path, is_local=False):
        """Initialize a new stream"""

        self._url = None
        self._base = None
        self._m3u8 = None

        if is_local:
            self._url = ''
            self._base = ''
            self.__init_from_file(path)
        else:
            self.set_url(path)

    @property
    def url(self):
        """Return stream url"""
        return self._url


    @property
    def base(self):
        """Return base url"""
        return self._base


    @property
    def m3u8(self):
        """Returns the stream"""
        return self._m3u8


    def set_url(self, url):
        """Set a new stream url"""
        self._url = url
        self.__update_base_url()
        self._m3u8 = m3u8.loads(get_url(self.url, headers).text)


    def __update_base_url(self):
        """Update the base url"""
        parts = self.url.rsplit('/', 1)
        if len(parts) != 2:
            print('Malformed stream url')
            sys.exit(1)
        self._base = parts[0] + '/'


    def __init_from_file(self, path):
        """Reads the local file"""
        try:
            with open(path, 'r') as f:
                self._m3u8 = m3u8.loads(f.read())
        except:
            print('Could not read local file')
            sys.exit(1)


def main():
    """This is the main program"""

    stream = MyStream(args.stream_url, args.local_mode)

    # Check for other playlists
    while len(stream.m3u8.playlists) != 0:
        print('There are multiple streams available. Please select one to download:')
        for i, p in enumerate(stream.m3u8.playlists):
            print(f'{i}: {p.stream_info}')

        print()

        while True:
            choice = input('Choice: ')
            try:
                choice = int(choice)
                assert choice >= 0
                assert choice < len(stream.m3u8.playlists)
            except:
                print('Please enter a valid number')
                continue
            break

        stream.set_url(choose_url(stream.base, stream.m3u8.playlists[choice].uri))

    # Initialize random generator
    random.seed()

    logger.info('Downloading segments...')

    if args.live_mode:
        print('Entering live mode. Hit STRG + C to exit this mode...')
        print()

        # Initialize timestamp
        last_ts = None

        while True:
            try:
                download_stream_segments(stream, last_ts)
                last_ts = stream.m3u8.segments[-1].program_date_time

                if last_ts == None:
                    print('Stream does not provide a timestamp. Exiting live mode')
                    break

                print('Waiting for changes...')

                # Sleep for 10 seconds before requesting the new playlist
                time.sleep(10)
                stream = MyStream(stream.url)

                # Remove last bar
                print('\033[F\033[K', end='')
                print('\033[F\033[K', end='')

            except KeyboardInterrupt:
                print('Stopped live mode')
                break

    else:
        download_stream_segments(stream)

    logger.info('Done downloading')

    # Convert file, if requested
    if args.convert_format != None:
        print(args.convert_format)
        logger.info('Converting file...')

        if args.convert_format == 'mp3':
            ffmpeg.input(args.output).output(args.output + '.mp3', vn=None, ar=44100, ac=2, **{'b:a': '192k'}).run()
        elif args.convert_format == 'mp4':
            ffmpeg.input(args.output).output(args.output + '.mp4', vcodec='libx264', acodec='aac').run()

        logger.info('Done converting')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Bye')
        sys.exit(0)
