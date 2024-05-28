#!/bin/bash

#. /opt/miniconda/bin/activate
conda activate restapi
#python opt/Video360_WebUI/main.py --port 33334 > /logs/log-main.txt &
#python opt/Video360_WebUI/restapi.py --port 33333 > /logs/log-rest.txt &

tmux new-session -s api -d
tmux new-sessuib -s web -d
tmux send-keys -t api "python /opt/Video360_WebUI/restapi.py --port 33333" 'Enter'
tmux send-keys -t web "python /opt/Video360_WebUI/main.py --port 33334" 'Enter'
#python opt/Video360_WebUI/main.py --port 33334 &
#python opt/Video360_WebUI/restapi.py --port 33333 &