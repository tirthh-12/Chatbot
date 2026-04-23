# 🤖 LangGraph Chatbot

A conversational AI chatbot built with **LangGraph** and **Streamlit**, powered by **Groq's Llama 3.3-70B** model. Built and improved incrementally as a public learning journey on LinkedIn — from a basic chatbot to a production-level application.

---

## ✨ Current Features

- 🧠 **Persistent memory** — conversation history survives page reloads
- 💬 **Multiple chats** — create, switch, and delete conversations from the sidebar
- 📝 **Auto-titled chats** — each chat is named from the first message
- 🗄️ **Owned data layer** — messages stored in app-controlled SQLite table
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
| App Data | SQLite (owned schema) |
| Config | python-dotenv |

---

## 📁 Project Structure

Chatbot/
├── app.py              # Streamlit UI entry point
├── main.py             # CLI chatbot entry point
├── graph.py            # LangGraph graph builder
├── nodes.py            # Graph node definitions
├── state.py            # ChatState TypedDict
├── prompts.py          # System prompt & ChatPromptTemplate
├── llm.py              # Groq LLM initialisation
├── db.py               # Owned data layer — chat_messages table
├── chat_manager.py     # Chat thread management
├── config.py           # App-level configuration
├── utils.py            # Shared helpers
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variable template
├── .gitignore          # Git ignore rules
└── README.md           # This file

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

## 📦 Version History

### v1.0 — The Beginning
The baseline. A working chatbot with a simple Streamlit UI and CLI interface. No memory between reloads. Single conversation only.

### v1.1 — Memory + Chat Management
Fixed page reload wiping the conversation. Added sidebar with multiple chats, new chat button, delete chat, and auto-titled conversations from first message.

### v2.0 — Owned Data Layer ← current
**Problem:** Chat history was read from LangGraph's internal checkpointer tables using msgpack deserialization. Fragile, version-sensitive, and caused duplicate messages in the UI.

**Fix:** Introduced `db.py` with an app-owned `chat_messages` table. All message reads and writes go through this layer. LangGraph checkpointer is used only for AI memory — never for UI rendering. Eliminated duplicate responses and fixed old chat history rendering.

---

## 🔮 What's Coming Next

### v2.1 — Smart Memory Management
**Problem to solve:** Every turn appends the full message history to the prompt. By turn 20 the prompt is huge. By turn 50 it hits the model's token limit and responses degrade.

**Planned approach:**
- Threshold at 20 messages triggers summarization
- Messages older than the last 10 are compressed into a precise bullet-point summary
- Last 10 messages always stay verbatim — the protected window
- Every prompt is built as `[SUMMARY] + [LAST 10 MESSAGES]`
- Summary stored in SQLite and updated as conversation grows

**Why a protected window:** A summarizer can silently lose precision. A single word like "not" changes meaning completely. Recent messages stay exact.

### v3.0 — Tool Use
Web search, calculator, and other tools via LangGraph tool nodes.

### v4.0 — Projects Feature
Group conversations under a project with shared context — similar to Claude Projects.

### v5.0 — Production Hardening
Docker, environment management, structured logging, and deployment.

---

## 📄 License

MIT License — free to use and modify.
