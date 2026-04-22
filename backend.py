from pydantic import BaseModel

class RequestState(BaseModel):
    model_name: str
    model_provider: str
    System_prompt: str
    messages: list[str]
    allow_search: bool

from fastapi import FastAPI
from ai_agent import get_response

Allowed_model = [
    # Groq models (current)
    "llama-3.3-70b-versatile",       # replaces llama3-70b-8192 & mixtral-8x7b-32768
    "llama-3.1-8b-instant",          # fast, lightweight
    "llama-3.3-70b-versatile",       # best general-purpose Groq model
    "meta-llama/llama-4-scout-17b-16e-instruct",  # multimodal capable
    # OpenAI models
    "gpt-4o-mini",
    "gpt-4o",
]
# Deduplicate while preserving order
Allowed_model = list(dict.fromkeys(Allowed_model))

app = FastAPI(title='chatbot server')

@app.post('/chat')
def chat_endpoint(request: RequestState):
    if request.model_name not in Allowed_model:
        return {"error": f"Invalid model name. Allowed models: {Allowed_model}"}
    llm_id = request.model_name
    query = request.messages
    allow_search = request.allow_search
    system_prompt = request.System_prompt
    provider = request.model_provider
    response = get_response(llm_id, query, allow_search, system_prompt, provider)
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=9999)