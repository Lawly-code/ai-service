import json
import os

from dotenv import load_dotenv

load_dotenv("assistant/.env")

PROMPTS = json.load(open("assistant/data/prompts.json", encoding="utf-8"))
DEEPSEEK_TOKEN = os.getenv("deepseek_token")
TEMPERATURE = float(os.getenv("temperature"))
MAX_TOKENS = int(os.getenv("max_tokens"))