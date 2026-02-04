from datetime import datetime
from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator



class Models(BaseModel):
    llms: list[str]
    bots: list[str]


class Tool(BaseModel):
    id: str
    name: str
    description: str
    parameters: dict[str, Any]


class Content(BaseModel):
    type: Literal["text", "tool_call"]
    value: str
    tool_call_id: str | None = Field(default=None)


class ChatMsg(BaseModel):
    role: str
    content: str | list[Content]
    created: datetime | None = Field(default=None)
    tool_id: str | None = Field(default=None)
    derived_from: "None | ChatMsg" = Field(default=None)
    sender: Identity | None = Field(default=None, description="Identity of the message sender")

    def to_output_dict(self) -> dict[str, Any]:
        return {"role": self.role, "content": self.content}


class ChatRequest(BaseModel):
    bot_name: str | None = Field(default=None)
    llm_name: str | None = Field(default=None)
    messages: list[ChatMsg]
    user: User | None = Field(default=None, description="User making the request")
    agent: Agent | None = Field(default=None, description="Agent handling the request")

    @model_validator(mode="before")
    @classmethod
    def validate_before_creation(cls, values: dict[str, Any]) -> dict[str, Any]:
        if values.get("bot_name", None) is None and values.get("llm_name", None) is None:
            raise ValueError("Either bot_name or llm_name must be provided")
        return values


class ChatResponse(BaseModel):
    generation: ChatMsg
    agent: Agent | None = Field(default=None, description="Agent that generated the response")


class RequestType(Enum):
    MODELS = "models"
    CHAT = "chat"

    @property
    def request_type(self) -> type[BaseModel] | None:
        if self == RequestType.MODELS:
            return None
        elif self == RequestType.CHAT:
            return ChatRequest
        return None

    @property
    def response_type(self) -> type[BaseModel]:
        if self == RequestType.MODELS:
            return Models
        elif self == RequestType.CHAT:
            return ChatResponse
        raise ValueError(f"Unknown request type: {self}")


class RequestEnvelope(BaseModel):
    request_type: RequestType
    auth_token: str
    request: ChatRequest | None = Field(default=None)

    def validate_request(self):
        assert self.request_type.request_type is not None and isinstance(
            self.request, self.request_type.request_type
        )

    def validate_response(self, response: Any):
        assert isinstance(response, self.request_type.response_type)


class ResponseEnvelope(BaseModel):
    response: Models | ChatResponse
