import re

class Sanitizer:
    def sanitize(self, text: str) -> str:
        # Stub for masking passwords, secrets, API keys, JWTs
        text = re.sub(r'ey[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+', '[MASKED_JWT]', text)
        return text
