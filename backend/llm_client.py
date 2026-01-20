"""Direct API clients for OpenAI and Google Gemini."""

import httpx
from typing import List, Dict, Any, Optional
from .config import (
    OPENAI_API_KEY,
    GEMINI_API_KEY,
    ANTHROPIC_API_KEY,
    XAI_API_KEY
)


async def query_openai(
    model: str,
    messages: List[Dict[str, str]],
    timeout: float = 120.0
) -> Optional[Dict[str, Any]]:
    """
    Query OpenAI API directly.

    Args:
        model: Model name (e.g., "gpt-4", "gpt-3.5-turbo")
        messages: List of message dicts with 'role' and 'content'
        timeout: Request timeout in seconds

    Returns:
        Response dict with 'content', or None if failed
    """
    if not OPENAI_API_KEY:
        print(f"Skipping OpenAI model {model}: OPENAI_API_KEY not configured")
        return None

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": messages,
    }

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload
            )
            response.raise_for_status()

            data = response.json()
            message = data['choices'][0]['message']

            return {
                'content': message.get('content'),
                'reasoning_details': None  # OpenAI doesn't have this field
            }

    except Exception as e:
        print(f"Error querying OpenAI model {model}: {e}")
        return None


async def query_gemini(
    model: str,
    messages: List[Dict[str, str]],
    timeout: float = 120.0
) -> Optional[Dict[str, Any]]:
    """
    Query Google Gemini API directly.

    Args:
        model: Model name (e.g., "gemini-pro", "gemini-1.5-pro")
        messages: List of message dicts with 'role' and 'content'
        timeout: Request timeout in seconds

    Returns:
        Response dict with 'content', or None if failed
    """
    if not GEMINI_API_KEY:
        print(f"Skipping Gemini model {model}: GEMINI_API_KEY not configured")
        return None

    # Convert messages to Gemini format
    contents = []
    for msg in messages:
        role = "user" if msg["role"] == "user" else "model"
        contents.append({
            "role": role,
            "parts": [{"text": msg["content"]}]
        })

    payload = {
        "contents": contents,
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 8192,
        }
    }

    try:
        # Use the REST API endpoint
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_API_KEY}"

        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                url,
                json=payload
            )
            response.raise_for_status()

            data = response.json()

            # Extract content from Gemini response format
            if 'candidates' in data and len(data['candidates']) > 0:
                candidate = data['candidates'][0]
                if 'content' in candidate and 'parts' in candidate['content']:
                    text = candidate['content']['parts'][0].get('text', '')
                    return {
                        'content': text,
                        'reasoning_details': None
                    }

            return None

    except Exception as e:
        print(f"Error querying Gemini model {model}: {e}")
        return None


async def query_anthropic(
    model: str,
    messages: List[Dict[str, str]],
    timeout: float = 120.0
) -> Optional[Dict[str, Any]]:
    """
    Query Anthropic API directly.

    Args:
        model: Model name (e.g., "claude-3-5-sonnet-20241022")
        messages: List of message dicts with 'role' and 'content'
        timeout: Request timeout in seconds

    Returns:
        Response dict with 'content', or None if failed
    """
    if not ANTHROPIC_API_KEY:
        print(f"Skipping Anthropic model {model}: ANTHROPIC_API_KEY not configured")
        return None

    headers = {
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": 8192,
    }

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=payload
            )
            response.raise_for_status()

            data = response.json()

            # Extract content from Anthropic response format
            if 'content' in data and len(data['content']) > 0:
                text = data['content'][0].get('text', '')
                return {
                    'content': text,
                    'reasoning_details': None
                }

            return None

    except Exception as e:
        print(f"Error querying Anthropic model {model}: {e}")
        return None


async def query_xai(
    model: str,
    messages: List[Dict[str, str]],
    timeout: float = 120.0
) -> Optional[Dict[str, Any]]:
    """
    Query xAI (Grok) API directly.

    Args:
        model: Model name (e.g., "grok-beta")
        messages: List of message dicts with 'role' and 'content'
        timeout: Request timeout in seconds

    Returns:
        Response dict with 'content', or None if failed
    """
    if not XAI_API_KEY:
        print(f"Skipping xAI model {model}: XAI_API_KEY not configured")
        return None

    headers = {
        "Authorization": f"Bearer {XAI_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": messages,
    }

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                "https://api.x.ai/v1/chat/completions",
                headers=headers,
                json=payload
            )
            response.raise_for_status()

            data = response.json()
            message = data['choices'][0]['message']

            return {
                'content': message.get('content'),
                'reasoning_details': None
            }

    except Exception as e:
        print(f"Error querying xAI model {model}: {e}")
        return None


async def query_model(
    model_id: str,
    messages: List[Dict[str, str]],
    timeout: float = 120.0
) -> Optional[Dict[str, Any]]:
    """
    Query a model using the appropriate API based on model ID.

    Args:
        model_id: Full model identifier (e.g., "openai:gpt-4", "gemini:gemini-pro")
        messages: List of message dicts with 'role' and 'content'
        timeout: Request timeout in seconds

    Returns:
        Response dict with 'content' and optional 'reasoning_details', or None if failed
    """
    if ":" not in model_id:
        print(f"Invalid model ID format: {model_id}. Expected 'provider:model'")
        return None

    provider, model = model_id.split(":", 1)

    if provider == "openai":
        return await query_openai(model, messages, timeout)
    elif provider == "gemini":
        return await query_gemini(model, messages, timeout)
    elif provider == "anthropic":
        return await query_anthropic(model, messages, timeout)
    elif provider == "xai":
        return await query_xai(model, messages, timeout)
    else:
        print(f"Unknown provider: {provider}")
        return None


async def query_models_parallel(
    models: List[str],
    messages: List[Dict[str, str]]
) -> Dict[str, Optional[Dict[str, Any]]]:
    """
    Query multiple models in parallel.

    Args:
        models: List of model identifiers (provider:model format)
        messages: List of message dicts to send to each model

    Returns:
        Dict mapping model identifier to response dict (or None if failed)
    """
    import asyncio

    # Create tasks for all models
    tasks = [query_model(model, messages) for model in models]

    # Wait for all to complete
    responses = await asyncio.gather(*tasks)

    # Map models to their responses
    return {model: response for model, response in zip(models, responses)}
