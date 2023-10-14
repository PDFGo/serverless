#!/bin/sh

# Author Sid86
# Start unicorn server
# bash run.sh


uvicorn main:app --host 0.0.0.0 --port 3000