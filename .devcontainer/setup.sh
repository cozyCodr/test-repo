#!/bin/bash
# .devcontainer/setup.sh

# Install global tools
npm install -g pnpm

# Frontend setup
cd frontend
pnpm install
pnpm dlx shadcn-ui@latest init -y

# Backend setup
cd ../backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# AI service setup
cd ../ai-service
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Return to workspace root
cd ..

echo "Setup complete! Your development environment is ready."