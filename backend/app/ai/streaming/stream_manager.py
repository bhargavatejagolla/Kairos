from collections.abc import AsyncGenerator


class StreamManager:
    async def stream_response(self, response_generator: AsyncGenerator[str, None]) -> AsyncGenerator[str, None]:
        async for chunk in response_generator:
            yield f"data: {chunk}\n\n"
        yield "data: [DONE]\n\n"
