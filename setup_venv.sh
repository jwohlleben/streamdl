#!/bin/bash
python3 -m venv .env
source .env/bin/activate
pip install alive-progress
pip install m3u8
pip install requests
pip install ffmpeg-python
