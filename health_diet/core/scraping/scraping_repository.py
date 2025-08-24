from core.db_halper import db_helper
from core.models.product_model import Product
from core.scraping.scraping_services import get_date_from_csv


async def fill_table_product():
    date_list = get_date_from_csv()

    async with db_helper.session_factory() as session:
        for date in date_list:
            product = Product(
                title=date[0],
                calories=date[1],
                protein=date[2],
                fats=date[3],
                carbs=date[4],
            )
            session.add(product)

        await session.commit()