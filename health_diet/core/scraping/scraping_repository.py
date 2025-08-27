from core.db_halper import db_helper
from core.models.categories_model import Category
from core.models.product_model import Product
from core.scraping.scraping_services import get_date_from_csv, get_all_categories


async def fill_table_categories():
    categories = get_all_categories()

    async with db_helper.session_factory() as session:
        for category in categories:
            new_record = Category(title=category)
            session.add(new_record)

        await session.commit()


async def fill_table_product():
    date_list = await get_date_from_csv()

    async with db_helper.session_factory() as session:
        for date in date_list:
            product = Product(
                title=date[0],
                calories=date[1],
                protein=date[2],
                fats=date[3],
                carbs=date[4],
                category_id=date[5],
            )
            session.add(product)

        await session.commit()