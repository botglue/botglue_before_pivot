from typing import Any, ClassVar

from pydantic import BaseModel, Field
from typedtemplate import BaseTemplateEngine, JinjaTemplateEngine, TypedTemplate


class ReferencedTypesClassTemplate(TypedTemplate):
    list_of_types: list[type[BaseModel]] = Field(description="List of types")
    template_engine: ClassVar[BaseTemplateEngine] = JinjaTemplateEngine(debug=True)
    template_string: ClassVar[str | None] = """{% for t in list_of_types %}
from {{ t.__module__}} import {{ t.__name__ }} as T_{{loop.index}}{% endfor %}
from pydantic import BaseModel

class X(BaseModel):{% for t in list_of_types %}
    o{{loop.index}}: T_{{loop.index}}{% endfor %}


x=X.model_json_schema()"""


def generate_json_schema(list_of_types: list[type[BaseModel]]) -> dict[str, Any]:
    template = ReferencedTypesClassTemplate(list_of_types=list_of_types)
    code = template.render()
    context = {}
    compiled = compile(code, "<string>", "exec")
    exec(compiled, context)
    schema = context["x"]

    return schema
