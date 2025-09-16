#!/bin/bash

# Start FastAPI backend
source .venv/bin/activate && python main.py  &

# Start Next.js frontend
cd ./frontend
yarn build
yarn start --port 3001

# Wait for both processes to finish
wait
