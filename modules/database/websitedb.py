from modules.database import Tools
from modules.database.models import WebsiteModel


class WebsiteDB():

    db_name = 'websites.db'

    def __init__(self) -> None:
        self.cur, self.con = Tools.create_db(self.db_name)
        Tools.create_table(self.cur, self.con, WebsiteModel)

    def add_entry(self, model: WebsiteModel) -> None:
        Tools.add_entry(self.cur, self.con, model)
