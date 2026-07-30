from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class SMTPConfig(BaseSettings):
    host: str = Field(alias="SMTP_HOST", default="smtp.gmail.com")
    port: int = Field(alias="SMTP_PORT", default=587)
    user: str | None = Field(alias="SMTP_USER", default=None)
    password: str | None = Field(alias="SMTP_PASSWORD", default=None)
    use_tls: bool = Field(alias="SMTP_USE_TLS", default=True)
    from_email: str = Field(alias="SMTP_FROM_EMAIL", default="noreply@kairos.dev")
    from_name: str = Field(alias="SMTP_FROM_NAME", default="KAIROS Platform")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

smtp_config = SMTPConfig()
