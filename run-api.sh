#!/bin/bash

. /opt/miniconda/bin/activate
conda activate restapi
#python opt/Video360_WebUI/main.py --port 33334 > /logs/log-main.txt &
#python opt/Video360_WebUI/restapi.py --port 33333 > /logs/log-rest.txt &

python opt/Video360_WebUI/main.py --port 33334 &
python opt/Video360_WebUI/restapi.py --port 33333 &