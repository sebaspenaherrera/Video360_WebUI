#!/bin/bash

# Activate the conda environment for the main screen
. /opt/miniconda/bin/activate
conda activate restapi


# Create a new tmux session for the API and WebUI
tmux new-session -s api -d
tmux new-session -s web -d

# Initialize the API
tmux send-keys -t api ". /opt/miniconda/bin/activate restapi" 'Enter' 
tmux send-keys -t api "python /opt/Video360_WebUI/restapi.py --port 33333" 'Enter'

# Initialize the WebUI
tmux send-keys -t web ". /opt/miniconda/bin/activate restapi" 'Enter' 
tmux send-keys -t web "python /opt/Video360_WebUI/main.py --port 33334" 'Enter'