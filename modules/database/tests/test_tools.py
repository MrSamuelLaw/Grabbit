import pytest
import sqlite3
from pydantic import BaseModel
from modules.scrapers import GritrScraper
from modules.database import Tools
from modules.database.models import WebsiteModel


class TestTools():

    @pytest.fixture
    def db_name(self) -> str:
        return ':memory:'

    def test_create_db(self, db_name) -> None:
        '''Test with bad inputs to ensure an error
         is thrown.'''
        # bad in puts
        with pytest.raises(sqlite3.OperationalError):
            Tools.create_db(db_name='')
            Tools.create_db(db_name=0)
        # valid input
        Tools.create_db(db_name=db_name)

    def test_get_schema_strings(self) -> None:
        '''Test to make sure that the schema
        strings work properly'''
        # create fake model for testing
        class Fake(BaseModel):
            __table_name__ = 'faketable'
            column1: str
        table_name_expected = 'faketable'
        column_string_expected = 'column1 STRING'
        table_name, column_string = Tools.get_schema_strings(Fake)
        assert table_name == table_name_expected
        assert column_string == column_string_expected

    def test_find_scraper(self) -> None:
        '''Test to make sure that the correct scraper comes up'''
        model = WebsiteModel(
            customer_email='Bob@email.com',
            website=r'https://gritrsports.com/',
        )
        scraper = Tools.find_scraper(model)
        assert isinstance(scraper, (GritrScraper,))

    def test_add_entry(self, db_name) -> None:
        # create a database & table
        cur, con = Tools.create_db(db_name=db_name)
        Tools.create_table(cur, con, WebsiteModel)

        # create defined model
        model = WebsiteModel(
            customer_email='Bob@email.com',
            website=r'https://gritrsports.com/',
        )
        model.scraper = Tools.find_scraper(model)
        model.instock = True

        # append the data to the table and view the result
        Tools.add_entry(cur, con, model)
        cur.execute('SELECT * FROM websites')
        assert cur.fetchall()


if __name__ == "__main__":
    pytest.main([__file__, '-s'])
