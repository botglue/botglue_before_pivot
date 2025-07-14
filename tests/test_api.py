import json

import pytest

from botglue.llore.api import (
    RequestEnvelope,
    ResponseEnvelope,
)
from botglue.schema import generate_json_schema


@pytest.mark.debug
def test_generate_json_schema():
    """Test that RequestEnvelope generates valid JSON schema."""

    schema = generate_json_schema(list_of_types=[RequestEnvelope, ResponseEnvelope])

    assert set(schema.keys()) == {"$defs", "properties", "required", "title", "type"}
    assert set(schema["$defs"].keys()) == {
        "RequestType",
        "ChatMsg",
        "ChatRequest",
        "ChatResponse",
        "Content",
        "Models",
        "RequestEnvelope",
        "ResponseEnvelope",
    }

    actual_str = json.dumps(schema, indent=2).strip()

    print(actual_str)

    assert (
        actual_str
        == """
{
  "$defs": {
    "ChatMsg": {
      "properties": {
        "role": {
          "title": "Role",
          "type": "string"
        },
        "content": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "items": {
                "$ref": "#/$defs/Content"
              },
              "type": "array"
            }
          ],
          "title": "Content"
        },
        "created": {
          "anyOf": [
            {
              "format": "date-time",
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Created"
        },
        "tool_id": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Tool Id"
        },
        "derived_from": {
          "anyOf": [
            {
              "$ref": "#/$defs/ChatMsg"
            },
            {
              "type": "null"
            }
          ],
          "default": null
        }
      },
      "required": [
        "role",
        "content"
      ],
      "title": "ChatMsg",
      "type": "object"
    },
    "ChatRequest": {
      "properties": {
        "bot_name": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Bot Name"
        },
        "llm_name": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Llm Name"
        },
        "messages": {
          "items": {
            "$ref": "#/$defs/ChatMsg"
          },
          "title": "Messages",
          "type": "array"
        }
      },
      "required": [
        "messages"
      ],
      "title": "ChatRequest",
      "type": "object"
    },
    "ChatResponse": {
      "properties": {
        "generation": {
          "$ref": "#/$defs/ChatMsg"
        }
      },
      "required": [
        "generation"
      ],
      "title": "ChatResponse",
      "type": "object"
    },
    "Content": {
      "properties": {
        "type": {
          "enum": [
            "text",
            "tool_call"
          ],
          "title": "Type",
          "type": "string"
        },
        "value": {
          "title": "Value",
          "type": "string"
        },
        "tool_call_id": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Tool Call Id"
        }
      },
      "required": [
        "type",
        "value"
      ],
      "title": "Content",
      "type": "object"
    },
    "Models": {
      "properties": {
        "llms": {
          "items": {
            "type": "string"
          },
          "title": "Llms",
          "type": "array"
        },
        "bots": {
          "items": {
            "type": "string"
          },
          "title": "Bots",
          "type": "array"
        }
      },
      "required": [
        "llms",
        "bots"
      ],
      "title": "Models",
      "type": "object"
    },
    "RequestEnvelope": {
      "properties": {
        "request_type": {
          "$ref": "#/$defs/RequestType"
        },
        "auth_token": {
          "title": "Auth Token",
          "type": "string"
        },
        "request": {
          "anyOf": [
            {
              "$ref": "#/$defs/ChatRequest"
            },
            {
              "type": "null"
            }
          ],
          "default": null
        }
      },
      "required": [
        "request_type",
        "auth_token"
      ],
      "title": "RequestEnvelope",
      "type": "object"
    },
    "RequestType": {
      "enum": [
        "models",
        "chat"
      ],
      "title": "RequestType",
      "type": "string"
    },
    "ResponseEnvelope": {
      "properties": {
        "response": {
          "anyOf": [
            {
              "$ref": "#/$defs/Models"
            },
            {
              "$ref": "#/$defs/ChatResponse"
            }
          ],
          "title": "Response"
        }
      },
      "required": [
        "response"
      ],
      "title": "ResponseEnvelope",
      "type": "object"
    }
  },
  "properties": {
    "o1": {
      "$ref": "#/$defs/RequestEnvelope"
    },
    "o2": {
      "$ref": "#/$defs/ResponseEnvelope"
    }
  },
  "required": [
    "o1",
    "o2"
  ],
  "title": "X",
  "type": "object"
}
    """.strip()
    )

    # assert False
    #     # Verify schema structure
