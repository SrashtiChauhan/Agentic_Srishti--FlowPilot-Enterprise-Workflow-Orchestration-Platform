
import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


OLLAMA_BASE_URL = "http://localhost:11434"


def generate_response(
    model_name: str,
    system_prompt: str,
    user_input: str,
    temperature: float = 0.2,
) -> str:
    """Generate a response from a locally running Ollama model."""

    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input},
        ],
        "stream": False,
        "options": {
            "temperature": temperature,
        },
    }

    request = Request(
        f"{OLLAMA_BASE_URL}/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urlopen(request, timeout=120) as response:
            result = json.loads(response.read().decode("utf-8"))

        message = result.get("message", {})
        content = message.get("content", "")

        if not content.strip():
            raise RuntimeError("Ollama returned an empty response.")

        return content.strip()

    except HTTPError as exc:
        error_details = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"Ollama returned HTTP {exc.code}: {error_details}"
        ) from exc

    except URLError as exc:
        raise RuntimeError(
            "Could not connect to Ollama. Check that Ollama is running."
        ) from exc
