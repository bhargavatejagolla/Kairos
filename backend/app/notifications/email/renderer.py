import jinja2

class TemplateEngine:
    def __init__(self):
        # Allow loading templates directly from strings (from DB)
        self.env = jinja2.Environment(
            loader=jinja2.DictLoader({}),
            autoescape=jinja2.select_autoescape(['html', 'xml'])
        )

    def render(self, template_str: str, context: dict) -> str:
        template = self.env.from_string(template_str)
        # Add global variables if needed
        context["company_name"] = "KAIROS"
        return template.render(**context)
