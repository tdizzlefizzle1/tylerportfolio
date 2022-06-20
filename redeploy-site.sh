#!/bin/bash

tmux kill-server
cd ~/tylerportfolio/
git fetch && git reset origin/main --hard
source .venv/bin/activate
pip install -r requirements.txt
#figure out how to get into the virtual environment before we run the server
tmux new-session -d -s 0 'source .venv/bin/activate && flask run --host=0.0.0.0'
