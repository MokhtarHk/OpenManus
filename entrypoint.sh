#!/bin/bash
set -e

mkdir -p config

cat > config/config.toml << 'ENDOFFILE'
[llm]
model = "PLACEHOLDER_MODEL"
base_url = "PLACEHOLDER_URL"
api_key = "PLACEHOLDER_KEY"
max_tokens = 8192
temperature = 0.0

[llm.vision]
model = "PLACEHOLDER_MODEL"
base_url = "PLACEHOLDER_URL"
api_key = "PLACEHOLDER_KEY"
ENDOFFILE

sed -i "s|PLACEHOLDER_MODEL|${LLM_MODEL:-gemini-2.5-flash}|g" config/config.toml
sed -i "s|PLACEHOLDER_URL|${LLM_BASE_URL:-https://generativelanguage.googleapis.com/v1beta/openai/}|g" config/config.toml
sed -i "s|PLACEHOLDER_KEY|${LLM_API_KEY}|g" config/config.toml

exec python server.py
