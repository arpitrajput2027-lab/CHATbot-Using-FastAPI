from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import re
from typing import List
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Sarvam Chatbot API")

SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")
SARVAM_API_URL = "https://api.sarvam.ai/v1/chat/completions"

SYSTEM_PROMPT = """You are a helpful, intelligent AI assistant powered by Sarvam AI. 
Be concise, friendly, and accurate. 
Reply in the same language the user writes in (Hindi, English, or Hinglish)."""


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]


@app.post("/api/chat")
async def chat(req: ChatRequest):
    print(req)
    if not SARVAM_API_KEY:
        raise HTTPException(status_code=500, detail="SARVAM_API_KEY not set in .env file")

    payload = {
        "model": "sarvam-30b",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            *[{"role": m.role, "content": m.content} for m in req.messages]
        ]
    }

    try:
        response = requests.post(
            SARVAM_API_URL,
            headers={
                "Authorization": f"Bearer {SARVAM_API_KEY}",
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=100
        )
        print(response.json())
        response.raise_for_status()
        data = response.json()
        reply = data["choices"][0]["message"]["content"]
        reply = re.sub(r'<think>.*?</think>', '', reply, flags=re.DOTALL).strip()
        return {"reply": reply}

    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="Sarvam API timed out")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Sarvam API error: {str(e)}")
    except (KeyError, IndexError):
        raise HTTPException(status_code=500, detail="Unexpected API response format")


@app.get("/api/health")
async def health():
    return {"status": "ok", "model": "sarvam-30b"}


# Serve static files (HTML/CSS/JS)
app.mount("/", StaticFiles(directory="static", html=True), name="static")


# import requests
# import os
# from dotenv import load_dotenv

# load_dotenv()

# api_key = os.getenv("SARVAM_API_KEY")

# response = requests.post(
#     "https://api.sarvam.ai/v1/chat/completions",
#     headers={
#         "Authorization": f"Bearer {api_key}",
#         "Content-Type": "application/json"
#     },
#     json={
#         "model": "sarvam-30b",
#         "messages": [
#             {
#                 "role": "user",
#                 "content": "Hello"
#             }
#         ]
#     }
# )

# print(response.status_code)
# print(response.text)