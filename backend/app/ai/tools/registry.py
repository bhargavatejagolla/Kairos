from app.ai.tools.base import BaseTool


class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, BaseTool] = {}
        
    def register(self, tool: BaseTool):
        self._tools[tool.name] = tool
        
    def get_tool(self, name: str) -> BaseTool | None:
        return self._tools.get(name)
        
    def get_all_tools(self) -> dict[str, BaseTool]:
        return self._tools
