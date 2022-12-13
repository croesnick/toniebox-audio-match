#!/bin/bash

# Start the debugger
#ps -el | awk '$14 == "usr/bin/python" {print $4}' > python.pid
python -m debugpy --listen 0.0.0.0:5678 --wait-for-client app.py 
