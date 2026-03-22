# ConsensusAI

**Get better answers through AI deliberation and peer review.**

ConsensusAI is a 3-stage collaborative AI system that brings together multiple leading language models (GPT-4, Gemini, Claude, Grok) to provide well-reasoned, peer-reviewed answers to your

Instead of relying on a single AI model, ConsensusAI orchestrates a deliberation process where multiple models independently answer your question, anonymously evaluate each other's responses, and synthesize a

## How It Works

When you submit a question, ConsensusAI executes a three-stage process:

### Stage 1: Independent Responses
Your question is sent to all configured AI models in parallel. Each model provides its own independent answer without knowing what the others said. You can view all individual responses in a tab interface.

### Stage 2: Anonymous Peer Review
Each model evaluates and ranks all responses (including its own) without knowing which model produced which response.

### Stage 3: Final Synthesis
A designated "Chairman" model reviews all original responses and peer evaluations to synthesize a comprehensive final answer that represents the collective wisdom of the AI council.

## Why ConsensusAI?

- **Better Accuracy**: Multiple perspectives reduce individual model biases and errors
- **Transparency**: See all individual responses and peer evaluations
- **Flexibility**: Use any combination of OpenAI, Google, Anthropic, and xAI models


## Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
 (Python package manager)

### Installation

1. **Clone the repository**
```bash
git clone <github.com/harshmriduhash>
cd consensusai
```

2. **Install dependencies**

Backend:
```bash
uv sync
```

Frontend:
```bash
cd frontend
npm install
cd ..
```

3. **Configure API Keys**

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
```env
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=AIza...
ANTHROPIC_API_KEY=sk-ant-...
XAI_API_KEY=xai-...
```

**Getting API Keys:**
- OpenAI: https://platform.openai.com/api-keys
- Gemini: https://makersuite.google.com/app/apikey
- Anthropic: https://console.anthropic.com/settings/keys
- xAI: https://console.x.ai/

**Important Notes:**
- You need **at least 2 API keys** for the council to work effectively
- The system gracefully skips models whose API keys aren't configured
- You can start with just OpenAI + Gemini and add others later
- Models without API keys will be automatically excluded from deliberation

4. **Customize Models (Optional)**

Edit `backend/config.py` to choose which models participate:

```python
COUNCIL_MODELS = [
    "openai:gpt-4o",                        # OpenAI GPT-4 Omni
    "gemini:gemini-1.5-pro",                # Google Gemini 1.5 Pro
    "anthropic:claude-3-5-sonnet-20241022", # Anthropic Claude 3.5 Sonnet
    "xai:grok-beta",                        # xAI Grok
]

CHAIRMAN_MODEL = "gemini:gemini-1.5-pro"
```

### Running ConsensusAI

**Option 1: Use the start script**
```bash
./start.sh
```

**Option 2: Manual start**

Terminal 1 - Backend:
```bash
uv run python -m backend.main
```

Terminal 2 - Frontend:
```bash
cd frontend
npm run dev
```

Open http://localhost:5173 in your browser.

## Project Structure

```
consensusai/
├── backend/           # Python FastAPI backend
│   ├── config.py     # Model and API configuration
│   ├── llm_client.py # Direct API clients for each provider
│   ├── council.py    # 3-stage orchestration logic
│   ├── storage.py    # Conversation persistence
│   └── main.py       # FastAPI application
├── frontend/         # React frontend
│   └── src/
│       ├── App.jsx           # Main application
│       ├── api.js            # Backend API client
│       └── components/       # UI components
├── data/             # Conversation storage
└── .env              # API keys (create from .env.example)
```

## Tech Stack

- **Backend:** FastAPI (Python 3.10+), async httpx, direct API integrations
- **Frontend:** React + Vite, react-markdown for rendering
- **Storage:** JSON files in `data/conversations/`
- **Package Management:** uv for Python, npm for JavaScript
- **APIs:** Direct integration with OpenAI, Google Gemini, Anthropic, and xAI

## Documentation

- [Backend Documentation](backend/README.md) - API details and architecture
- [Frontend Documentation](frontend/README.md) - UI components and setup

## License

MIT License - Feel free to use this for any purpose.

## Contributing

This project is provided as-is. Fork it and customize it however you like!
