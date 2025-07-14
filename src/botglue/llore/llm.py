import logging
from abc import ABCMeta, abstractmethod
from datetime import UTC, datetime
from typing import Any, ClassVar

from pydantic import BaseModel

from botglue.llore.api import ChatMsg, ChatResponse

logger = logging.getLogger(__name__)


def response_to_chat_result(response: dict[str, Any]) -> ChatResponse:
    # Handle OpenAI format
    if "choices" in response:
        choices = response["choices"]
        assert len(choices) == 1
        ch = choices[0]
        content = ch["message"]["content"]
        role = ch["message"]["role"]
        created = datetime.fromtimestamp(response["created"])
    # Handle Ollama format
    elif "message" in response:
        content = response["message"]["content"]
        role = response["message"]["role"]
        created = datetime.fromisoformat(response["created_at"].replace("Z", "+00:00"))
    # Handle Claude format
    elif "content" in response:
        content = response["content"]
        assert len(content) == 1
        assert content[0]["type"] == "text"
        content = content[0]["text"]
        role = response["role"]
        created = datetime.now(UTC)
    elif "chatCompletion" in response:
        content = response["chatCompletion"]["chatCompletionContent"]
        role = "assistant"
        created = datetime.now(UTC)
    else:
        raise ValueError(f"Unsupported response format: {response}")

    logger.debug(f"Response: {created}")
    return ChatResponse(generation=ChatMsg(content=content, role=role, created=created))


class Tool(metaclass=ABCMeta):
    config_type: ClassVar[type[BaseModel]]
    name: str

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def __call__(self, input: ChatMsg) -> list[ChatMsg]:
        raise NotImplementedError


class ToolMap:
    tools: dict[str, Tool]

    def __init__(self):
        self.tools = {}

    def update(self, tool: Tool):
        self.tools[tool.name] = tool
