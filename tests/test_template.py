from typing import ClassVar

import pytest
from pydantic import BaseModel, Field
from typedtemplate import BaseTemplateEngine, JinjaTemplateEngine, TypedTemplate


class User(BaseModel):
    """User model for template testing."""

    name: str = Field(description="User's full name")
    email: str = Field(description="User's email address")
    age: int = Field(description="User's age", ge=0)
    is_active: bool = Field(default=True, description="Whether user is active")
    tags: list[str] = Field(default_factory=list, description="User tags")


@pytest.mark.debug
def test_template_with_pydantic_model():
    """Test template rendering with Pydantic model data."""

    class UserTemplate(TypedTemplate):
        template_engine: ClassVar[BaseTemplateEngine] = JinjaTemplateEngine(debug=True)
        template_string: ClassVar[str | None] = """
    User Profile:
    Name: {{ user.name }}
    Email: {{ user.email }}
    Age: {{ user.age }}
    Active: {{ user.is_active }}
    Tags: {{ ", ".join(user.tags) }}
    """
        # The typed input data for this template
        user: User = Field(description="The user to build profile from")

    # If you don't provide `name` at creation, it will raise a ValidationError
    user = User(
        name="Bob Smith",
        email="bob@example.com",
        age=30,
        is_active=True,
        tags=["developer", "python"],
    )
    template = UserTemplate(user=user)
    # Model validation is also run when `render` is called
    result = template.render()

    expected = """
    User Profile:
    Name: Bob Smith
    Email: bob@example.com
    Age: 30
    Active: True
    Tags: developer, python
    """

    assert result.strip() == expected.strip()
