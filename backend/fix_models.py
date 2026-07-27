import os

models_dir = "/home/ironman/projects/kairos/backend/app/db/models"
files = ["ai_conversation.py", "ai_message.py", "ai_prompt.py", "ai_response.py", "knowledge_document.py", "knowledge_chunk.py", "embedding.py", "ai_usage.py", "api_key.py"]

for f in files:
    path = os.path.join(models_dir, f)
    with open(path, "r") as file:
        content = file.read()
    
    content = content.replace("from app.db.base import Base\nfrom app.db.mixins.timestamp import TimestampMixin\nfrom app.db.mixins.uuid import UUIDPrimaryKeyMixin", "from app.db.models.base import BaseModel")
    content = content.replace("from app.db.base import Base\nfrom app.db.mixins.uuid import UUIDPrimaryKeyMixin", "from app.db.models.base import BaseModel")
    content = content.replace("(Base, UUIDPrimaryKeyMixin, TimestampMixin)", "(BaseModel)")
    content = content.replace("(Base, UUIDPrimaryKeyMixin)", "(BaseModel)")
    
    with open(path, "w") as file:
        file.write(content)
        
# For ai_cache.py, just use Base
with open(os.path.join(models_dir, "ai_cache.py"), "r") as file:
    content = file.read()
content = content.replace("from app.db.base import Base", "from app.db.base import Base")
# Nothing needed for ai_cache.py since it just uses Base which is correct
