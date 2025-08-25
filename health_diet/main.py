import logging

from fastapi import FastAPI
from uvicorn import run

from core.settings import settings


loger = logging.getLogger(__name__)

main_app = FastAPI()


if __name__ == '__main__':
    settings.log.configure_logging()
    run("main:main_app", host=settings.run.host, port=settings.run.port, reload=True)
