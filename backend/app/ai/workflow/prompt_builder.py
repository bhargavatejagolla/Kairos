class PromptBuilder:
    def build(self, template: str, context: str) -> str:
        return f"{template}\n\nContext:\n{context}"
