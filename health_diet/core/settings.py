import logging
from os import getenv

from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings


class EnvLoader:
    load_dotenv()


class GetENV(EnvLoader):
    WEB_SITE_URL: str = getenv("WEB_SITE_URL")
    WEB_SITE_DOMAIN: str = getenv("WEB_SITE_DOMAIN")

    DATABASE_URL: str = getenv("DATABASE_URL")

    SERVER_HOST: str = getenv("SERVER_HOST")
    SERVER_PORT: int = int(getenv("SERVER_PORT"))


class ScrapingConfig(BaseModel):
    url: str = GetENV.WEB_SITE_URL
    domain: str = GetENV.WEB_SITE_DOMAIN
    parser: str = "lxml"
    headers: dict = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1"
    }


class LogerConfig:
    loger_level = logging.DEBUG
    log_handlers_console = logging.StreamHandler()
    #log_handlers_file = logging.FileHandler("app.log", encoding="utf-8")


    def configure_logging(self):
        logging.basicConfig(
            level=self.loger_level,
            datefmt= "%Y-%m-%d %H:%M:%S",
            format="[%(asctime)s.%(msecs)03d] %(module)20s:%(lineno)-4d %(levelname)8s - %(message)s",
            handlers=[self.log_handlers_console]
        )


class DataBaseConfig(BaseModel):
    url: str = GetENV.DATABASE_URL
    echo: bool = False
    pool_size: int = 10
    max_overflow: int = 15


class RunConfig(BaseModel):
    host: str = GetENV.SERVER_HOST
    port: int = GetENV.SERVER_PORT


class ApiPrefix(BaseModel):
    prefix: str = "/api"


class Settings(BaseSettings):
    scraping: ScrapingConfig = ScrapingConfig()
    log: LogerConfig = LogerConfig()
    db: DataBaseConfig = DataBaseConfig()
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()


settings = Settings()
