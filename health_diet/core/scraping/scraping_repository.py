from core.db_halper import db_helper
from core.models.product_model import Product
from core.scraping.scraping_services import get_date_from_csv


async def fill_table_product():
    date_list = get_date_from_csv()

    async with db_helper.session_factory() as session:
        for date in date_list:
            product = Product(
                category=date[0],
                title=date[1],
                calories=date[2],
                protein=date[3],
                fats=date[4],
                carbs=date[5],
            )
            session.add(product)

        await session.commit()