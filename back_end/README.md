# 🚀 LangGraph FastAPI Agent

A simple FastAPI application that wraps a [LangGraph](https://github.com/langchain-ai/langgraph) agent using [LangChain](https://github.com/langchain-ai/langchain) and the OpenAI API. Includes a built-in `multiply` tool and basic tool routing logic.

---

## ⚙️ Requirements

- Python **3.10+**
- [uv](https://github.com/astral-sh/uv) *(optional but recommended)*

---

## 🧪 Setup Instructions

### 1. Clone the project

```bash
git clone https://github.com/your-username/langgraph-demo.git
cd langgraph-demo
```

### 2. Create virtual environment

Using [`uv`](https://github.com/astral-sh/uv):

```bash
uv venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows
```

Or with plain `venv`:

```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```bash
uv pip install -e .
# or without uv:
pip install -e .
```

---

## 🔐 Environment Variables

Create a `.env` file in the root folder and add your OpenAI API key:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

---

## 🚦 Run FastAPI Server

Run the server locally using Uvicorn:

```bash
uvicorn app.main:app --reload
```

Expected output:

```text
Uvicorn running on http://127.0.0.1:8000
```

---

## 📬 Example API Request

POST `/ask` — Send a question to the chatbot:

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is 6 times 7?"}'
```

Response:

```json
{
  "messages": [
    {"type": "human", "content": "What is 6 times 7?"},
    {"type": "ai", "content": "6 times 7 is 42."},
    {"type": "ai", "content": "I have finished processing your question: 6 times 7 is 42."}
  ]
}
```

---

## 📈 Visualize LangGraph

To output the LangGraph structure in [Mermaid](https://mermaid.live) format:

```python
print(graph.get_graph().draw_mermaid())
```

Then paste the output into [Mermaid Live Editor](https://mermaid.live) to see the diagram.

---

## 💡 Tip

For production, run:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --log-level info
```

Disable `--reload` in production deployments.
