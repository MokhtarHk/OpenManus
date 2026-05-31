#!/bin/bash
set -e

# Create config directory if it doesn't exist
mkdir -p config

# Write config.toml from environment variables
cat > config/config.toml <${LLM_MODEL:-gemini-2.5-flash}"
base_url = "${LLM_BASE_URL:-https://generativelanguage.googleapis.com/v1beta/openai/}"
api_key = "${LLM_API_KEY}"
max_tokens = 8192
temperature = 0.0

[llm.vision]
model = "${VISION_MODEL:-gemini-2.5-flash}"
base_url = "${LLM_BASE_URL:-https://generativelanguage.googleapis.com/v1beta/openai/}"
api_key = "${LLM_API_KEY}"
EOF

# Start the FastAPI server
exec python server.py
