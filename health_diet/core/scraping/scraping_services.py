import csv
import json
import logging
import re

import requests
from bs4 import BeautifulSoup
from sqlalchemy import select

from core.db_halper import db_helper
from core.models.categories_model import Category
from core.settings import settings


services_loger = logging.getLogger(__name__)


def get_index_html():
    req = requests.get(settings.scraping.url, headers=settings.scraping.headers)
    src = req.text

    with open("core/scraping/index.html", "w", encoding="utf-8") as file:
        file.write(src)


def get_links_to_categories():
    with open("core/scraping/index.html", encoding="utf-8") as file:
        src = file.read()

    soup = BeautifulSoup(src, settings.scraping.parser)
    all_products_href = soup.find_all("a", class_="mzr-tc-group-item-href")
    category_link_dict = {}
    for product in all_products_href:
        category_link_dict[f"{product.text}"] = f"https://{settings.scraping.domain}{product.get("href")}"

    with open("core/scraping/all_categories_dict.json", "w", encoding="utf-8") as file:
        json.dump(category_link_dict, file, indent=4, ensure_ascii=False)


def get_csv_file_with_all_products():
    with open("core/scraping/all_categories_dict.json", encoding="utf-8") as file:
        all_category = json.load(file)

    with open("core/scraping/all_products.csv", "w", encoding="utf-8", newline='') as file:
        writer = csv.writer(file)

        writer.writerow(["Категория", "Продукт", "Калории", "Белки", "Жиры", "Углеводы"])

        for category_name, category_href in all_category.items():
            req = requests.get(category_href, headers=settings.scraping.headers)
            services_loger.info(f"Запрос к категории - {category_name}")
            src = req.text
            soup = BeautifulSoup(src, "lxml")

            alert_block = soup.find(class_="uk-alert-danger")
            if alert_block is not None:
                continue

            products_data = soup.find(class_="mzr-tc-group-table").find("tbody").find_all("tr")

            for item in products_data:
                product_tds = item.find_all("td")

                category = category_name
                title = product_tds[0].text.strip()
                calorie = product_tds[1].text.strip()
                protein = product_tds[2].text.strip()
                fats = product_tds[3].text.strip()
                carbohydrates = product_tds[4].text.strip()

                writer.writerow([
                    category,
                    title,
                    calorie,
                    protein,
                    fats,
                    carbohydrates
                ])

            services_loger.info(f"Данные категории - {category_name} записаны ")


def extract_number(text):
    if not text:
        return 0.0

    match = re.search(r'[\d,]+\.?\d*', str(text).replace(',', '.'))
    if match:
        try:
            return float(match.group())
        except ValueError:
            return 0.0
    return 0.0


async def get_date_from_csv() -> list[list]:
    with open("core/scraping/all_products.csv", 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)

        date_from_csv = []
        next(csv_reader)  # Заголовки

        for row in csv_reader:
            title = str(row[1])
            calories = int(extract_number(row[2]))
            protein = float(extract_number(row[3]))
            fats = float(extract_number(row[4]))
            carbs = float(extract_number(row[5]))
            category_id = int(await get_category_id(str(row[0])))

            date_from_csv.append([title, calories, protein, fats, carbs, category_id])

        return date_from_csv


def get_all_categories() -> list:
    with open("core/scraping/all_categories_dict.json", "r",  encoding='utf-8') as file:
        data = json.load(file)

    return list(data.keys())


async def get_category_id(category_title: str) -> int:
    async with db_helper.session_factory() as session:
        result = await session.execute(select(Category.id).where(Category.title == category_title))
        return result.scalar()
