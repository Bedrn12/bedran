from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_hostname: str
    database_port:int
    database_password:str
    database_name:str
    database_username:str
    secret_key:str
    algorithm:str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"


settings = Settings()   #When you instantiate the Settings class (settings = Settings()), Pydantic will automatically load values from environment variables (based on the attribute names) and validate their types. If any required environment variables are missing or if their values don't match the expected types, Pydantic will raise validation errors. This ensures that your application's settings are correctly configured before execution