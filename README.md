<<<<<<< HEAD
# ⚡ AI Chat — Multi-Model Chatbot with Web Search

A full-stack **AI chatbot application** powered by **FastAPI**, **LangChain**, and **Streamlit**. Switch between Groq and OpenAI models, toggle live web search, customize the system prompt, and chat — all from a sleek dark-themed UI.

---

## ✨ Features

- 🤖 **Multi-Model Support** — Choose from Groq (LLaMA) and OpenAI (GPT) models on the fly
- 🌐 **Web Search Toggle** — Enable Tavily-powered live search per session
- 🧠 **Custom System Prompt** — Fully configurable AI persona from the sidebar
- 💬 **Conversation History** — Maintains full chat context across turns
- 🎨 **Stylish Dark UI** — Custom CSS with gradient bubbles, avatars, and monospace fonts
- ⚡ **FastAPI Backend** — Clean REST API with Pydantic request validation
- 🔌 **Provider-Aware Routing** — Automatically routes requests to Groq or OpenAI based on selected model

---

## 🗂️ Project Structure

```
ai-chat/
│
├── ai_agent.py     # LangChain agent — LLM setup, tool binding, response logic
├── backend.py      # FastAPI server — /chat endpoint, request validation
├── frontend.py     # Streamlit UI — chat interface, sidebar controls
├── .env            # API keys (not committed)
└── README.md
```

---

## 🧠 Supported Models

| Model | Provider | Description |
|---|---|---|
| `llama-3.3-70b-versatile` | Groq | Best general-purpose Groq model |
| `llama-3.1-8b-instant` | Groq | Fast & lightweight |
| `meta-llama/llama-4-scout-17b-16e-instruct` | Groq | Multimodal capable |
| `gpt-4o-mini` | OpenAI | Fast & cost-effective GPT |
| `gpt-4o` | OpenAI | Most capable GPT model |

---

## ⚙️ How It Works

```
User (Streamlit UI)
        │
        ▼
FastAPI /chat endpoint  ←─── Pydantic request validation
        │
        ▼
LangChain Agent
  ├── LLM: Groq (LLaMA) or OpenAI (GPT)
  └── Tool: TavilySearchResults (if search enabled)
        │
        ▼
AI Response → Streamlit chat bubble
```

1. **Frontend** collects user input, model config, system prompt, and search toggle
2. **Backend** validates the request and checks the model against the allowlist
3. **Agent** builds a LangChain pipeline with the selected LLM and optional Tavily search tool
4. **Response** is extracted from the last `AIMessage` and returned to the UI

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- API keys for Groq, OpenAI, and Tavily

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/ai-chat.git
cd ai-chat

# Install dependencies
pip install streamlit fastapi uvicorn langchain langchain-groq langchain-openai \
            langchain-community tavily-python python-dotenv pydantic requests
```

### Environment Setup

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key
```

---

## ▶️ Running the App

You need to start **two terminals** — one for the backend and one for the frontend.

### 1. Start the FastAPI Backend

```bash
python backend.py
```

The API will be live at `http://127.0.0.1:9999`

### 2. Start the Streamlit Frontend

```bash
streamlit run frontend.py
```

Open your browser at `http://localhost:8501`

---

## 🔌 API Reference

### `POST /chat`

**Request Body:**

```json
{
  "model_name": "llama-3.3-70b-versatile",
  "model_provider": "Groq",
  "System_prompt": "You are a helpful assistant.",
  "messages": ["Hello, how are you?"],
  "allow_search": false
}
```

**Response:**

```json
"I'm doing great! How can I help you today?"
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | [Streamlit](https://streamlit.io/) |
| **Backend** | [FastAPI](https://fastapi.tiangolo.com/) + [Uvicorn](https://www.uvicorn.org/) |
| **AI Framework** | [LangChain](https://langchain.com/) |
| **LLM Providers** | [Groq](https://groq.com/) · [OpenAI](https://openai.com/) |
| **Web Search** | [Tavily](https://tavily.com/) |
| **Validation** | [Pydantic](https://docs.pydantic.dev/) |

---

## 📌 Notes & Limitations

- Only models listed in `Allowed_model` (in `backend.py`) are accepted — invalid model names return an error
- Conversation context only sends **user messages** to the agent (not assistant replies)
- Web search uses a maximum of 2 results per query via Tavily
- The `.env` file must be present and populated before starting the backend

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
=======
# Role_Based_chatbot
>>>>>>> ceeb1ddcc810e99ef4df25eda065af1a5fe0b1a8
