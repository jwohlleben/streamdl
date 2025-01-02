# streamdl
A simple but feature-rich python script for downloading M3U8 streams.

## Prerequisites
In order to use streamdl, please install
- python3
- python3-pip
- python3-venv

### Install using apt
Run `sudo apt install python3 python3-pip python3-venv`

## Setup
In the streamdl folder run `./setup_venv.sh` to setup the virtual environment.

## Usage
```
usage: streamdl.py [-h] [-f] [-l] [-o outfile] [-c format] [-H header] [-R header]
                   [-s sec|minsec-maxsec] [-t min|h:min] [-v] [--version]
                   m3u8_stream

positional arguments:
  m3u8_stream           url to a stream file, e.g.
                        https://somewebsite.com/epicstream/stream.m3u8

options:
  -h, --help            show this help message and exit
  -f, --file            reads a local file instead
  -l, --live            enables live mode for downloading livestreams
  -o outfile, --output outfile
                        downloads to the given outfile
  -c format, --convert format
                        converts the stream to a given format (mp3, mp4)
  -H header, --header header
                        adds or overwrites an existing header based on the headers.py file
  -R header, --remove-header header
                        removes an existing header based on the headers.py file
  -s sec|minsec-maxsec, --sleep sec|minsec-maxsec
                        sleeps a fixed time sec or sleeps random in [minsec;maxsec] between
                        requests
  -t min|h:min, --timer min|h:min
                        sets a timer for stopping live mode
  -v, --verbose         shows progress, use -vv for maximum verbosity
  --version             show program's version number and exit
```

## Examples
Download a stream:<br>
`./run.sh "https://somewebsite.com/epicstream/stream.m3u8"`

Download a livestream and convert it into a video:<br>
`./run.sh -l -c mp4 "https://somewebsite.com/epicstream/stream.m3u8"`

Download a stream, wait 2.5 - 4.5 seconds between requests and save the stream as "myepicstream.ts":<br>
`./run.sh -s 2.5-4.5 -o "myepicstream.ts" "https://somewebsite.com/epicstream/stream.m3u8"`

Download a stream and add a custom header:<br>
`./run.sh -H "My-Header:Awesome" "https://somewebsite.com/epicstream/stream.m3u8"`

## Misc
- You can edit the file `modules/headers.py` to use custom standard headers
