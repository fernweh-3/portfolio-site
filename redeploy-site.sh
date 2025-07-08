#!/bin/bash

# fetch the latest git repo
git fetch && git reset origin/main --hard

# install dependencies
source .venv/bin/activate
pip install -r requirements.txt

# restart the systemd service
systemctl restart myportfolio