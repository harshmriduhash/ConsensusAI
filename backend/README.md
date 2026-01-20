# ConsensusAI Backend

The backend is a FastAPI application that orchestrates the 3-stage AI deliberation process and manages conversation storage.

## Architecture

### Core Components

**`config.py`** - Configuration
- API keys for OpenAI, Gemini, Anthropic, and xAI
- Council member models list
- Chairman model selection
- Data storage directory

**`llm_client.py`** - API Clients
- Direct API integration for each provider
- Unified interface through `query_model()` and `query_models_parallel()`
- Graceful error handling and timeout management
- Async/await for parallel queries

**`council.py`** - Orchestration Logic
- `stage1_collect_responses()` - Parallel model queries
- `stage2_collect_rankings()` - Anonymous peer review
- `stage3_synthesize_final()` - Chairman synthesis
- Ranking parsing and aggregation
- Conversation title generation

**`storage.py`** - Data Persistence
- JSON-based conversation storage
- CRUD operations for conversations
- Message history management

**`main.py`** - FastAPI Application
- REST API endpoints
- CORS configuration
- Request/response handling

## API Endpoints

### Get All Conversations
```http
GET /api/conversations
```

Response:
```json
[
  {
    "id": "conv_123",
    "created_at": "2024-01-01T12:00:00",
    "messages": [],
    "title": "Conversation Title"
  }
]
```

### Create New Conversation
```http
POST /api/conversations
```

Request body:
```json
{
  "title": "New Conversation"
}
```

### Get Conversation by ID
```http
GET /api/conversations/{conversation_id}
```

### Send Message
```http
POST /api/conversations/{conversation_id}/message
```

Request body:
```json
{
  "message": "Your question here"
}
```

Response:
```json
{
  "conversation": {
    "id": "conv_123",
    "messages": [...],
    "title": "Conversation Title"
  },
  "metadata": {
    "label_to_model": {
      "Response A": "openai:gpt-4o",
      "Response B": "gemini:gemini-1.5-pro"
    },
    "aggregate_rankings": [
      {
        "model": "openai:gpt-4o",
        "average_rank": 1.5,
        "rankings_count": 4
      }
    ]
  }
}
```

### Delete Conversation
```http
DELETE /api/conversations/{conversation_id}
```

## Model Configuration

Edit `config.py` to customize which models participate:

```python
# Supported format: "provider:model"
# Providers: openai, gemini, anthropic, xai

COUNCIL_MODELS = [
    "openai:gpt-4o",
    "gemini:gemini-1.5-pro",
    "anthropic:claude-3-5-sonnet-20241022",
    "xai:grok-beta",
]

CHAIRMAN_MODEL = "gemini:gemini-1.5-pro"
```

### Supported Models

**OpenAI** (`openai:`)
- `gpt-4o` - GPT-4 Omni
- `gpt-4-turbo` - GPT-4 Turbo
- `gpt-3.5-turbo` - GPT-3.5 Turbo

**Google Gemini** (`gemini:`)
- `gemini-1.5-pro` - Gemini 1.5 Pro
- `gemini-1.5-flash` - Gemini 1.5 Flash (faster)

**Anthropic** (`anthropic:`)
- `claude-3-5-sonnet-20241022` - Claude 3.5 Sonnet
- `claude-3-opus-20240229` - Claude 3 Opus

**xAI** (`xai:`)
- `grok-beta` - Grok Beta

## How the 3-Stage Process Works

### Stage 1: Independent Responses
```python
async def stage1_collect_responses(user_query: str)
```
- Queries all council models in parallel using `asyncio.gather()`
- Each model receives only the user's question
- Returns list of `{model, response}` dictionaries
- Failed queries return `None` but don't block other responses

### Stage 2: Anonymous Peer Review
```python
async def stage2_collect_rankings(user_query: str, stage1_results: List)
```
- Creates anonymous labels: "Response A", "Response B", etc.
- Stores mapping from labels to actual model names
- Queries all council models to rank the anonymized responses
- Parses ranking from structured format: "FINAL RANKING: 1. Response A, 2. Response B..."
- Returns rankings and label-to-model mapping

### Stage 3: Chairman Synthesis
```python
async def stage3_synthesize_final(user_query: str, stage1_results: List, stage2_results: List)
```
- Provides chairman with full context:
  - Original user question
  - All individual responses with model names
  - All peer rankings with model names
- Chairman synthesizes final answer incorporating insights from all stages
- Returns final response

## Adding a New Provider

To add support for a new AI provider:

1. **Add API client function to `llm_client.py`**:
```python
async def query_newprovider(model: str, messages: List, timeout: float):
    # Implement API call
    # Return {'content': str, 'reasoning_details': Optional[str]}
    pass
```

2. **Update `query_model()` dispatcher**:
```python
async def query_model(model_id: str, messages: List, timeout: float):
    provider, model = model_id.split(":", 1)

    if provider == "newprovider":
        return await query_newprovider(model, messages, timeout)
    # ... existing providers
```

3. **Add API key to `config.py`**:
```python
NEWPROVIDER_API_KEY = os.getenv("NEWPROVIDER_API_KEY")
```

4. **Update `.env.example`** with the new key

## Development

### Running Tests
```bash
# From project root
uv run pytest backend/tests/
```

### Running the Server
```bash
# Development mode (auto-reload)
uv run python -m backend.main

# The server runs on http://localhost:8001
```

### Code Structure Best Practices
- All imports use relative imports (e.g., `from .config import ...`)
- Run backend as module: `python -m backend.main` (not `python backend/main.py`)
- Async/await throughout for parallel operations
- Graceful degradation: system continues if individual models fail

## Error Handling

The backend implements graceful error handling:

- **Individual model failures**: System continues with successful responses
- **Parsing errors**: Fallback regex extracts ranking if structured format fails
- **Network timeouts**: Configurable timeout (default 120s) with async cancellation
- **Missing API keys**: Models requiring missing keys will fail but won't crash the system

## Performance Optimization

- Parallel queries using `asyncio.gather()` for maximum throughput
- Timeout configuration prevents slow models from blocking others
- Async httpx for efficient connection pooling
- JSON storage is fast enough for typical usage; migrate to DB for high volume

## Data Storage

Conversations are stored in `data/conversations/` as JSON files:

```json
{
  "id": "unique-id",
  "created_at": "ISO-8601-timestamp",
  "title": "Auto-generated or custom title",
  "messages": [
    {
      "role": "user",
      "content": "User's question"
    },
    {
      "role": "assistant",
      "stage1": [...],
      "stage2": [...],
      "stage3": {...}
    }
  ]
}
```

Note: Metadata (label mappings, aggregate rankings) is computed on-demand and NOT persisted.
