from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Literal, List
import os

env = os.getenv("ENV", "dev")
# env = os.getenv("ENV", "prod")  # Default to 'prod' if ENV is not set
env_file = f".env.{env}"

# class SettingsBase(BaseSettings):
#     class Config:
#         env_file = env_file
#         # env_file_encoding = "utf-8"
#         # extra = "allow"
#         extra = "ignore"
class configMongo(BaseSettings):
    MONGO_HOST: str = Field("localhost", env="MONGO_HOST")
    MONGO_PORT: int = Field(27017, env="MONGO_PORT")
    MONGO_USERNAME: str = Field("user", env="MONGO_USERNAME")
    MONGO_PASSWORD: str = Field("secret", env="MONGO_PASSWORD")
    MONGO_DB: str = Field("devmcp", env="MONGO_DB")

    DB_NAME: str = Field("devmcp", env="DB_NAME")  # Có thể trùng với MONGO_DB

    MONGO_MAX_POOL_SIZE: int = Field(100, env="MONGO_MAX_POOL_SIZE")
    MONGO_MIN_POOL_SIZE: int = Field(10, env="MONGO_MIN_POOL_SIZE")
    MONGO_CONNECT_TIMEOUT_MS: int = Field(30000, env="MONGO_CONNECT_TIMEOUT_MS")
    MONGO_SERVER_SELECTION_TIMEOUT_MS: int = Field(30000, env="MONGO_SERVER_SELECTION_TIMEOUT_MS")
    MONGO_SOCKET_TIMEOUT_MS: int = Field(30000, env="MONGO_SOCKET_TIMEOUT_MS")
    MONGO_WAIT_QUEUE_TIMEOUT_MS: int = Field(30000, env="MONGO_WAIT_QUEUE_TIMEOUT_MS")

    MONGO_RETRY_WRITES: bool = Field(True, env="MONGO_RETRY_WRITES")
    MONGO_WRITE_CONCERN: str = Field("majority", env="MONGO_WRITE_CONCERN")
    MONGO_JOURNAL: bool = Field(True, env="MONGO_JOURNAL")
    MONGO_TZ_AWARE: bool = Field(True, env="MONGO_TZ_AWARE")

    @property
    def MONGO_URI(self) -> str:
        return f"mongodb://{self.MONGO_USERNAME}:{self.MONGO_PASSWORD}@{self.MONGO_HOST}:{self.MONGO_PORT}/{self.MONGO_DB}"

 
class configQdrant(BaseSettings):
    QDRANT_HOST: str = Field("localhost", env="QDRANT_HOST")
    QDRANT_PORT: int = Field(6333, env="QDRANT_PORT")
    COLLECTION: str = Field("qa", env="COLLECTION")
class configRedis(BaseSettings):
    REDIS_HOST: str = Field("localhost", env="REDIS_HOST")
    REDIS_PORT: int = Field(6379, env="REDIS_PORT")
    REDIS_DB: int = Field(0, env="REDIS_DB")
    REDIS_PASSWORD: str = Field("", env="REDIS_PASSWORD")
    REDIS_SSL: bool = Field(False, env="REDIS_SSL")

    REDIS_MAX_CONNECTIONS: int = Field(100, env="REDIS_MAX_CONNECTIONS")
    REDIS_SOCKET_TIMEOUT: int = Field(5, env="REDIS_SOCKET_TIMEOUT")
    REDIS_CACHE_EXPIRY: int = Field(3600, env="REDIS_CACHE_EXPIRY")
    REDIS_RETRY_ON_TIMEOUT: bool = Field(True, env="REDIS_RETRY_ON_TIMEOUT")

    REDIS_ENCODING: str = Field("utf-8", env="REDIS_ENCODING")
    REDIS_DECODE_RESPONSES: bool = Field(True, env="REDIS_DECODE_RESPONSES")
class configServer(BaseSettings):
    SERVER_HOST: str = Field("localhost", env="SERVER_HOST")
    SERVER_PORT: int = Field(8000, env="SERVER_PORT")
class configApp(BaseSettings):
    APP_NAME: str = Field("MCP Server", env="APP_NAME")
    APP_VERSION: str = Field("1.0.0", env="APP_VERSION")
    ALLOWED_HOSTS: List[str] = Field(["*"], env="ALLOWED_HOSTS")  # Default to allow all hosts
class corsOrigins(BaseSettings):
    CORS_ORIGINS: List[str] = Field(["*"], env="CORS_ORIGINS")  # Default to allow all origins
    DEBUG: bool = Field(False, env="DEBUG")  # Default to False
    ENVIRONMENT: Literal["dev", "prod"] = Field("dev", env="ENVIRONMENT")  # Default to 'dev'
    
class Settings(configMongo, configQdrant, configRedis, configServer, configApp, corsOrigins):
    class Config:
        env_file = env_file
        env_file_encoding = "utf-8"
        extra = "ignore"
    # pass
config_env_manager = Settings()