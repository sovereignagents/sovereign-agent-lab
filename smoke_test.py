"""
Smoke Test — run this before starting any exercise.
Expected output:  ✅  API connection OK — model replied: READY

Troubleshooting:
  "NEBIUS_KEY not set"   → open .env and paste your key (no quotes)
  "Connection refused"   → check your internet connection
  "401 Unauthorized"     → your API key is wrong or expired
  "ModuleNotFoundError"  → run `uv sync` first

Model note (2026-04-13):
  This uses Llama-3.3-70B-Instruct (the Base variant, not `_fast`).
  Only the `_fast` variant was removed in the Nebius deprecation round;
  the Base variant is still actively supported. If you see connection
  errors mentioning the model string, confirm you have pulled the latest
  main — the earlier scaffold may have referenced the wrong variant.
"""

import os
import sys
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("NEBIUS_KEY", "")
if not key or key == "sk-your-key-here":
    print("❌  NEBIUS_KEY not set. Copy .env.example → .env and paste your key.")
    sys.exit(1)

print("Connecting to Nebius API...")

try:
    client = OpenAI(
        base_url="https://api.tokenfactory.nebius.com/v1/",
        api_key=key,
    )
    resp = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct",
        messages=[{"role": "user", "content": "Reply with exactly one word: READY"}],
        max_tokens=10,
        temperature=0,
    )
    answer = resp.choices[0].message.content.strip()
    if "READY" in answer.upper():
        print(f"✅  API connection OK — model replied: {answer}")
        print(f"    Model : meta-llama/Llama-3.3-70B-Instruct  (Base variant)")
        print(f"    Tokens: {resp.usage.total_tokens}")
        print("\nYou're ready. Start with:")
        print("    uv run python week1/exercise1_context.py")
    else:
        print(f"⚠️   Unexpected reply: '{answer}'")
        print("    Connection works but model behaved unexpectedly. Try again.")
except Exception as e:
    print(f"❌  Connection failed: {e}")
    sys.exit(1)