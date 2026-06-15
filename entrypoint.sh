#!/bin/bash
set -e

mkdir -p config

if [ -z "$LLM_API_KEY" ]; then
  echo "ERROR: LLM_API_KEY is not set"
  exit 1
fi

cat > config/config.toml <<EOF
[llm]
model = "${LLM_MODEL:-gemini-2.5-flash}"
base_url = "${LLM_BASE_URL:-https://generativelanguage.googleapis.com/v1beta/openai/}"
api_key = "${LLM_API_KEY}"
max_tokens = 8192
temperature = 0.0

[llm.vision]
model = "${LLM_VISION_MODEL:-${LLM_MODEL:-gemini-2.5-flash}}"
base_url = "${LLM_VISION_BASE_URL:-${LLM_BASE_URL:-https://generativelanguage.googleapis.com/v1beta/openai/}}"
api_key = "${LLM_VISION_API_KEY:-${LLM_API_KEY}}"
EOF

exec python server.py
