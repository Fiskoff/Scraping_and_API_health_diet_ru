import asyncio
import logging

from fastapi import FastAPI
from uvicorn import run

from core.settings import settings
from core.scraping.run_scraping import run_scraping


loger = logging.getLogger(__name__)

main_app = FastAPI()


if __name__ == '__main__':
    settings.log.configure_logging()
    # asyncio.run(run_scraping())
    run("main:main_app", host=settings.run.host, port=settings.run.port, reload=True)

