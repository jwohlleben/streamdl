# streamdl
A simple but feature-rich python script for downloading M3U8 streams.

## Prerequisites
In order to use streamdl, please install
- python3
- python3-pip
- python3-venv

## Setup
In the streamdl folder run `./setup_venv.sh` to setup the virtual environment.

## Usage
```
usage: streamdl.py [-h] [-b base_url] [-o outfile] [-c format] [-a header:value] [-r header]
                   [-s sec|minsec-maxsec] [-v] [--version]
                   m3u8_stream

positional arguments:
  m3u8_stream           url to a stream file, e.g.
                        https://somewebsite.com/epicstream/stream.m3u8

options:
  -h, --help            show this help message and exit
  -b base_url, --base-url base_url
                        overwrites the default URL for downloading, e.g.
                        https://somewebsite.com/epicstream/
  -o outfile, --output outfile
                        downloads to the given outfile
  -c format, --convert format
                        converts the stream to a given format (mp3, mp4) using ffmpeg
  -a header:value, --add-header header:value
                        adds or overwrites an existing header based on the headers.py file
  -r header, --remove-header header
                        removes an existing header based on the headers.py file
  -s sec|minsec-maxsec, --sleep sec|minsec-maxsec
                        sleeps a fixed time sec or sleeps random in [minsec;maxsec] between
                        requests
  -v, --verbose         shows progress, use -vv for maximum verbosity
  --version             show program's version number and exit

```

## Examples
Download a stream:<br>
`./run.sh "https://somewebsite.com/epicstream/stream.m3u8"`

Download a stream, wait 2.5 - 4.5 seconds between requests and save the stream as "myepicstream.ts":<br>
`./run.sh -s 2.5-4.5 -o "myepicstream.ts"`

Download a stream and add a custom header:<br>
`./run.sh -a "My-Header:Awesome" "https://somewebsite.com/epicstream/stream.m3u8"`

## Misc
- You can edit the file `modules/headers.py` to use custom standard headers
- Use `ffmpeg -i inputfile.ts -vn -ar 44100 -ac 2 -b:a 192k outputfile.mp3` to convert the stream to mp3
- Use `ffmpeg -i outputfile.ts -c:v libx264 -c:a aac outputfile.mp4` to convert the stream to mp4
