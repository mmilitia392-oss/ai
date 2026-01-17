from fastapi import FastAPI, Request
from pydantic import BaseModel
import subprocess
import os
from typing import List, Dict
from uuid import uuid4

app = FastAPI()

# --------------------
# LLM Function
# --------------------
OLLAMA_MODEL = "tinyllama"

def ask_llm(prompt: str) -> str:
    try:
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"

        result = subprocess.run(
            ["ollama", "run", OLLAMA_MODEL, prompt],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
            timeout=300,
            env=env
        )

        if result.returncode != 0:
            print("Ollama error:", result.stderr)
            return f"LLM failed to respond. ({result.stderr.strip()})"

        return result.stdout.strip()

    except subprocess.TimeoutExpired:
        return "The AI is thinking too long (low resources). Try again."
    except FileNotFoundError:
        return "Ollama is not installed or not added to PATH."
    except Exception as e:
        return f"Unexpected error: {str(e)}"


# --------------------
# Request Schema
# --------------------
class ChatRequest(BaseModel):
    message: str
    session_id: str = None  # optional: user can provide a session_id to continue chat


# --------------------
# In-Memory Session Store
# --------------------
# Stores conversation history per session_id
sessions: Dict[str, List[Dict[str, str]]] = {}


# --------------------
# FastAPI Endpoint
# --------------------
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    user_message = request.message.strip()

    if not user_message:
        return {"response": "Please provide a message."}

    # Generate a new session_id if none provided
    session_id = request.session_id or str(uuid4())

    # Initialize conversation history if new session
    if session_id not in sessions:
        sessions[session_id] = []

    # Append user's message to session history
    sessions[session_id].append({"role": "user", "message": user_message})

    # Build the prompt with conversation history
    prompt = ""
    for entry in sessions[session_id]:
        role = entry["role"]
        msg = entry["message"]
        if role == "user":
            prompt += f"User: {msg}\n"
        else:
            prompt += f"AI: {msg}\n"

    # Ask Ollama
    ai_response = ask_llm(prompt)

    # Append AI response to session history
    sessions[session_id].append({"role": "ai", "message": ai_response})

    # Return AI response + session_id (so user can continue conversation)
    return {"response": ai_response, "session_id": session_id}
