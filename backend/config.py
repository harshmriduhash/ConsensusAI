"""Configuration for ConsensusAI."""

import os
from dotenv import load_dotenv

load_dotenv()

# API Keys for different providers
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
XAI_API_KEY = os.getenv("XAI_API_KEY")

# Council members - list of model identifiers in format "provider:model"
# Supported providers: openai, gemini, anthropic, xai
# NOTE: You need at least 2 working models (with valid API keys) for the system to work
# Models without API keys will be automatically skipped
COUNCIL_MODELS = [
    "openai:gpt-4o",                        # OpenAI GPT-4 Omni
    "gemini:gemini-2.5-flash",              # Google Gemini 2.5 Flash
    "anthropic:claude-3-5-sonnet-20241022", # Anthropic Claude 3.5 Sonnet
    "xai:grok-beta",                        # xAI Grok
]

# Chairman model - synthesizes final response
# This should be one of your configured models (with valid API key)
CHAIRMAN_MODEL = "gemini:gemini-2.5-flash"

# Data directory for conversation storage
DATA_DIR = "data/conversations"
