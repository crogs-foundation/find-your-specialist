#!/bin/bash

# Start FastAPI backend
source .venv/bin/activate && export DEBUG=1 && python main.py &

# Start Next.js frontend
cd ./frontend && yarn dev &

# Wait for both processes to finish
wait
