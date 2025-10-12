from pydantic_settings import BaseSettings
from pydantic import field_validator, ValidationError


class Settings(BaseSettings):
    ENVIRONMENT: str
    APP_NAME: str
    SECRET: str

    @field_validator("ENVIRONMENT")
    @classmethod
    def validate_environment(cls, value):
        if value in ("dev", "test", "prod"):
            return value
        raise ValidationError(f"Invalid environment value: {value}")
