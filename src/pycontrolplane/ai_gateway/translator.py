import time
from typing import Dict, Any, List, Optional, Tuple


class FormatTranslator:
    """
    Bidirectional schema translator between OpenAI-standard payloads and upstream
    provider protocols (Anthropic Messages API, Ollama, Google Gemini).
    Pure-Python implementation mirroring OmniRoute's open-sse translation engine.
    """

    @staticmethod
    def openai_to_anthropic(
        messages: List[Dict[str, Any]],
        model: str = "claude-3-5-sonnet-20241022",
        max_tokens: int = 4096,
    ) -> Dict[str, Any]:
        """Converts OpenAI format messages to Anthropic Messages API format."""
        system_prompts: List[str] = []
        anthropic_messages: List[Dict[str, Any]] = []

        for m in messages:
            role = m.get("role", "user")
            content = m.get("content", "")
            if role == "system":
                system_prompts.append(content)
            else:
                anth_role = "assistant" if role == "assistant" else "user"
                anthropic_messages.append({"role": anth_role, "content": content})

        payload: Dict[str, Any] = {
            "model": model,
            "messages": anthropic_messages,
            "max_tokens": max_tokens,
        }
        if system_prompts:
            payload["system"] = "\n\n".join(system_prompts)

        return payload

    @staticmethod
    def anthropic_to_openai(anthropic_response: Dict[str, Any], model: str) -> Dict[str, Any]:
        """Converts Anthropic Messages API response to OpenAI chat completion format."""
        content_blocks = anthropic_response.get("content", [])
        text_content = ""
        for block in content_blocks:
            if isinstance(block, dict) and block.get("type") == "text":
                text_content += block.get("text", "")
            elif isinstance(block, str):
                text_content += block

        usage = anthropic_response.get("usage", {})
        prompt_tokens = usage.get("input_tokens", len(text_content) // 4)
        completion_tokens = usage.get("output_tokens", len(text_content) // 4)

        return {
            "id": anthropic_response.get("id", f"chatcmpl-anth-{int(time.time())}"),
            "object": "chat.completion",
            "created": int(time.time()),
            "model": model,
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": text_content},
                    "finish_reason": anthropic_response.get("stop_reason", "stop"),
                }
            ],
            "usage": {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": prompt_tokens + completion_tokens,
            },
        }

    @staticmethod
    def openai_to_ollama(
        messages: List[Dict[str, Any]],
        model: str = "llama3",
        stream: bool = False,
    ) -> Dict[str, Any]:
        """Converts OpenAI format to Ollama native /api/chat payload."""
        return {
            "model": model,
            "messages": messages,
            "stream": stream,
        }

    @staticmethod
    def ollama_to_openai(ollama_response: Dict[str, Any], model: str) -> Dict[str, Any]:
        """Converts Ollama /api/chat response to OpenAI chat completion format."""
        msg = ollama_response.get("message", {})
        content = msg.get("content", "")
        prompt_eval = ollama_response.get("prompt_eval_count", 0)
        eval_count = ollama_response.get("eval_count", 0)

        return {
            "id": f"chatcmpl-ollama-{int(time.time())}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": model,
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": content},
                    "finish_reason": "stop" if ollama_response.get("done") else None,
                }
            ],
            "usage": {
                "prompt_tokens": prompt_eval,
                "completion_tokens": eval_count,
                "total_tokens": prompt_eval + eval_count,
            },
        }

    @staticmethod
    def openai_to_gemini(
        messages: List[Dict[str, Any]],
        model: str = "gemini-2.0-flash",
    ) -> Dict[str, Any]:
        """Converts OpenAI format to Gemini native generateContent payload."""
        contents: List[Dict[str, Any]] = []
        system_instruction = None

        for m in messages:
            role = m.get("role", "user")
            content = m.get("content", "")
            if role == "system":
                system_instruction = {"parts": [{"text": content}]}
            else:
                gemini_role = "model" if role == "assistant" else "user"
                contents.append({"role": gemini_role, "parts": [{"text": content}]})

        payload: Dict[str, Any] = {"contents": contents}
        if system_instruction:
            payload["systemInstruction"] = system_instruction
        return payload

    @staticmethod
    def gemini_to_openai(gemini_response: Dict[str, Any], model: str) -> Dict[str, Any]:
        """Converts Gemini generateContent response to OpenAI chat completion format."""
        candidates = gemini_response.get("candidates", [])
        text_content = ""
        finish_reason = "stop"

        if candidates:
            parts = candidates[0].get("content", {}).get("parts", [])
            for p in parts:
                text_content += p.get("text", "")
            finish_reason = candidates[0].get("finishReason", "stop").lower()

        usage = gemini_response.get("usageMetadata", {})
        prompt_tokens = usage.get("promptTokenCount", 0)
        completion_tokens = usage.get("candidatesTokenCount", 0)

        return {
            "id": f"chatcmpl-gemini-{int(time.time())}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": model,
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": text_content},
                    "finish_reason": finish_reason,
                }
            ],
            "usage": {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": prompt_tokens + completion_tokens,
            },
        }
