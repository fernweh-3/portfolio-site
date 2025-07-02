#!/bin/bash

# kill existing tmux sessions
tmux kill-server

# fetch the latest git repo
git fetch && git reset origin/main --hard

# install dependencies
source .venv/bin/activate
pip install -r requirements.txt

# start detached tmux session and starts server
tmux new-session -d -s portfolio-site "flask run --host=0.0.0.0 --port=5000"