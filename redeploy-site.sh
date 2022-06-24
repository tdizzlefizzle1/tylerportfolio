#!/bin/bash
#tmux kill-server
cd ~/tylerportfolio/
git fetch && git reset origin/main --hard
source .venv/bin/activate
pip install -r requirements.txt
tmux new -s 0 -d
tmux send-keys -t 0 "flask run --host=0.0.0.0" Enter
