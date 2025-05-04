import json
import os

try:
    PROMPTS = json.load(open("assistant/data/prompts.json", encoding="utf-8"))
except Exception:
    PROMPTS = json.load(open("app/assistant/data/prompts.json", encoding="utf-8"))

DEEPSEEK_TOKEN = os.getenv("deepseek_token")
TEMPERATURE = float(os.getenv("temperature"))
MAX_TOKENS = int(os.getenv("max_tokens"))
