import os
import json
import urllib.request
import urllib.error
from typing import Dict, Any, List, Optional
from .translator import FormatTranslator


class ProviderDispatcher:
    """
    Zero-dependency upstream LLM network dispatcher based on urllib.request.
    Detects environment API keys, formats provider payloads, and manages real HTTP dispatch.
    """

    @classmethod
    def get_api_key(cls, provider: str) -> Optional[str]:
        """Resolves API key from environment variables for a given provider."""
        provider_lower = provider.lower()
        if provider_lower == "openai":
            return os.getenv("OPENAI_API_KEY")
        elif provider_lower == "anthropic":
            return os.getenv("ANTHROPIC_API_KEY")
        elif provider_lower == "deepseek":
            return os.getenv("DEEPSEEK_API_KEY")
        elif provider_lower == "groq":
            return os.getenv("GROQ_API_KEY")
        elif provider_lower == "gemini":
            return os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        return None

    @classmethod
    def has_credentials(cls, provider: str) -> bool:
        if provider.lower() == "ollama":
            return True  # Ollama is local, does not require API keys
        return cls.get_api_key(provider) is not None

    @classmethod
    def dispatch(
        cls,
        provider: str,
        base_url: str,
        model_name: str,
        messages: List[Dict[str, Any]],
        timeout: float = 10.0,
    ) -> Optional[Dict[str, Any]]:
        """
        Dispatches request to upstream provider if credentials are present.
        Returns parsed OpenAI-compatible response dict, or None if credentials are missing
        (signaling the engine to fall back to synthesized response).
        Raises urllib.error.HTTPError on upstream HTTP error (e.g. 429).
        """
        provider_lower = provider.lower()
        api_key = cls.get_api_key(provider)

        # 1. Anthropic API
        if provider_lower == "anthropic":
            if not api_key:
                return None
            url = f"{base_url.rstrip('/')}/messages" if not base_url.endswith("/messages") else base_url
            anthropic_model = "claude-3-5-sonnet-20241022" if "3-5" in model_name else model_name
            payload = FormatTranslator.openai_to_anthropic(messages, model=anthropic_model)
            data_bytes = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                url,
                data=data_bytes,
                headers={
                    "x-api-key": api_key,
                    "anthropic-version": "2023-06-01",
                    "Content-Type": "application/json",
                },
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw_json = json.loads(resp.read().decode("utf-8"))
                return FormatTranslator.anthropic_to_openai(raw_json, model=model_name)

        # 2. Ollama Local
        elif provider_lower == "ollama":
            url = f"{base_url.rstrip('/')}/chat/completions"
            data_bytes = json.dumps({"model": model_name, "messages": messages, "stream": False}).encode("utf-8")
            req = urllib.request.Request(
                url,
                data=data_bytes,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            try:
                with urllib.request.urlopen(req, timeout=timeout) as resp:
                    return json.loads(resp.read().decode("utf-8"))
            except (urllib.error.URLError, ConnectionRefusedError, TimeoutError):
                # Local Ollama not running; return None to allow offline fallback
                return None

        # 3. Standard OpenAI-compatible providers (OpenAI, DeepSeek, Groq, Gemini OpenAI compatibility)
        else:
            if not api_key:
                return None
            url = f"{base_url.rstrip('/')}/chat/completions" if not base_url.endswith("/chat/completions") else base_url
            # Map aliases if necessary
            target_model = model_name
            if provider_lower == "groq" and "llama" in model_name:
                target_model = "llama-3.3-70b-versatile"
            elif provider_lower == "gemini" and "gemini" in model_name:
                target_model = "gemini-2.0-flash"

            data_bytes = json.dumps({"model": target_model, "messages": messages, "stream": False}).encode("utf-8")
            req = urllib.request.Request(
                url,
                data=data_bytes,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
