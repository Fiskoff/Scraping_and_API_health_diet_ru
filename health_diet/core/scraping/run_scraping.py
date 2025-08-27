import logging

from core.scraping.scraping_repository import fill_table_categories, fill_table_product
from core.scraping.scraping_services import get_index_html, get_links_to_categories, get_csv_file_with_all_products


scraping_loger = logging.getLogger(__name__)


async def run_scraping():
    try:
        scraping_loger.info("Сервис по сбору информации запущен")
        get_index_html()
        scraping_loger.info("Получена страница сайта. Создан файл index.html")
        get_links_to_categories()
        scraping_loger.info("Получены ссылки на страницы с информацией. Создан файл all_categories_dict.json")
        get_csv_file_with_all_products()
        scraping_loger.info("Информация выгружена с сайта. Создан файл с all_products.csv")
        await fill_table_categories()
        scraping_loger.info("Таблица с категориями заполнена")
        await fill_table_product()
        scraping_loger.info("Таблица продуктов заполнена")
        scraping_loger.info("Работа сервиса завершена")
    except Exception:
        scraping_loger.error("Ошибка во время выполнения скрапинга", exc_info=True)
