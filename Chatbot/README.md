# 🤖 LangGraph Chatbot

A conversational AI chatbot built with **LangGraph** and **Streamlit**, powered by **Groq's Llama 3.3-70B** model. Supports persistent multi-turn conversations using SQLite-backed memory via LangGraph's checkpointing system.

---

## ✨ Features

- 🧠 **Persistent memory** — conversation history survives page reloads via LangGraph's SQLite checkpointer
- ⚡ **Streaming responses** — tokens are streamed in real-time as the model generates them
- 💬 **Multi-turn chat** — full context window maintained across turns
- 🖥️ **Streamlit UI** — clean, browser-based chat interface
- 🖱️ **CLI mode** — run the chatbot directly in your terminal via `main.py`
- 🔒 **Secure config** — API keys loaded from `.env`, never hardcoded

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| LLM | Groq — `llama-3.3-70b-versatile` |
| Orchestration | LangGraph |
| Prompt Templates | LangChain Core |
| UI | Streamlit |
| Memory / State | LangGraph SQLite Checkpointer |
| Config | python-dotenv |

---

## 📁 Project Structure

```
Chatbot/
├── app.py              # Streamlit UI entry point
├── main.py             # CLI chatbot entry point
├── graph.py            # LangGraph graph builder
├── nodes.py            # Graph node definitions
├── state.py            # ChatState TypedDict
├── prompts.py          # System prompt & ChatPromptTemplate
├── llm.py              # Groq LLM initialisation
├── config.py           # App-level configuration (DB path, etc.)
├── utils.py            # Shared helpers (thread ID generation)
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variable template
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/langgraph-chatbot.git
cd langgraph-chatbot
```

### 2. Create and activate a virtual environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

```bash
# Copy the example file
cp .env.example .env   # macOS/Linux
copy .env.example .env  # Windows

# Open .env and add your Groq API key
GROQ_API_KEY=your_groq_api_key_here
```

> Get your free API key at [console.groq.com](https://console.groq.com)

---

## ▶️ Running the App

### Streamlit UI (recommended)

```bash
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

### CLI Mode

```bash
python main.py
```

Type `exit` or `quit` to end the session.

---

## 📸 Screenshots

> _Add screenshots here once the app is running._

---

## 🔮 Future Improvements

- [ ] Add support for multiple LLM providers (OpenAI, Anthropic)
- [ ] Session management UI (view / switch / delete threads)
- [ ] Export conversation history as Markdown or PDF
- [ ] Tool / function calling support (web search, calculator, etc.)
- [ ] Docker support for easy deployment

---

## 📄 License

MIT License — free to use and modify.
