from modules.database import DataBase, WebsiteModel

DB_NAME = ':memory:'
DB = DataBase(db_name=DB_NAME)


def check_stock(model: WebsiteModel) -> None:
    DB.cursor.execute(f'''--sql
        SELECT {DB.get_column_names(model)} FROM
        {model.__table_name__}
    ;''')
    result = DB.cursor.fetchall()
    result = [WebsiteModel(**dict(r)) for r in result]
    for r in result:
        r.scraper = DB.find_scraper(r)
        content = r.scraper.get_content(r.website)
        data = r.scraper.scrape(content)
        r.instock = r.scraper.instock(data)


def add_item_watch(model: WebsiteModel) -> None:
    model.scraper = DB.find_scraper(model)
    DB.add_entry(model)


if __name__ == '__main__':
    model = WebsiteModel(
        website = r'https://gritrsports.com/taurus-g3c-9mm-1' \
                    r'2rd-black-stainless-pistol-1-g3c939',
        customer_email = 'sam@email.com'
    )
    add_item_watch(model)
    check_stock(model)