from pydantic import BaseModel
from environs import Env

env = Env()
env.read_env()


class BotSettings(BaseModel):
    bot_token: str = env("BOT-TOKEN")


class WebHook(BaseModel):
    web_server_host: str = "127.0.0.1"
    web_server_port: int = 8080
    webhook_path: str = "/webhook"
    webhook_secret: str = "my-secret"  # (optional)
    base_webhook_url: str = "https://domen/"
    webhook_ssl_cert: str = "/path/to/cert.pem"
    webhook_ssl_priv: str = "/path/to/private.key"


class StartSettings(BaseModel):
    is_webhook: bool = False
    is_ssl: bool = False


settings_bot = BotSettings()
web_hook_settings = WebHook()
start_settings = StartSettings()
