from abc import ABC, abstractmethod

class EmailProvider(ABC):
    @abstractmethod
    async def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: str | None = None
    ) -> bool:
        pass
