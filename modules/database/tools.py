import sqlite3
from sqlite3 import Cursor, Connection
from pathlib import Path
from typing import Tuple, Union
from urllib.parse import urlparse
from modules.database.models import TableModel
from modules.scrapers import GritrScraper


class Tools():
    # =========== available scrapers ===========
    scrapers = [
        GritrScraper(),
    ]


    # ================ functions ================
    @staticmethod
    def create_db(*, db_name) -> Tuple[Cursor, Connection]:
        '''Creates a connection to the database and
        returns the cursor and connection object'''
        # establish the connection to the db
        if db_name == ':memory:':
            db_path = db_name
        else:
            root = Path(__file__).parent
            db_path = root.joinpath(db_name)
        connection = sqlite3.connect(db_path)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        return cursor, connection

    @staticmethod
    def create_table(cursor: Cursor,
                     connection: Connection, model: TableModel) -> None:
        '''Creates a table from a model'''
        # create the table from the schema
        table_name, column_string = Tools.get_schema_strings(model)
        cmd = f'''--sql
            CREATE TABLE IF NOT EXISTS {table_name}
            ({column_string})
        ;'''
        cursor.execute(cmd)
        connection.commit()

    @staticmethod
    def get_schema_strings(model: TableModel) -> Tuple[str, str]:
        '''Returns two strings, the table name
        and the column labels'''
        table_name = model.__table_name__          # extract table name
        properties = model.schema()['properties']  # extract the column names
        # formats it like -> colname TYPE, colname2 TYPE2, ...
        column_string = [
            f"{key} {str(val['type']).upper()}"
            for key, val in properties.items()
        ]
        column_string = ','.join(column_string)  # join them into csv string
        return table_name, column_string

    @staticmethod
    def get_column_names(model: TableModel) -> str:
        properties = model.schema()['properties']  # extract the column names
        column_string = [f"{key}" for key in properties.keys()]
        column_string = ','.join(column_string)    # join them into csv string
        return column_string

    @staticmethod
    def find_scraper(model: TableModel) -> Union[str, ]:
        '''Checks to see if a scraper for the website exists'''
        path = urlparse(model.website)
        name = path.netloc
        name_list = [s.name for s in Tools.scrapers]
        try:
            index = name_list.index(name)
        except IndexError:
            scraper = None
        else:
            scraper = Tools.scrapers[index]
        return scraper

    @staticmethod
    def add_entry(cur: Cursor, con: Connection, model: TableModel) -> None:
        '''Takes an item and adds it to the database'''
        # data massaging
        col_dict = model.dict()                       # convert to dictionary
        col_names = ','.join(col_dict.keys())         # pull out the column names
        col_vals = tuple(col_dict.values())           # create tuple of column values
        place_holder = ','.join(['?']*len(col_vals))  # create placeholder string

        # cmd creation and execution
        cmd = f'''--sql
        INSERT INTO {model.__table_name__} ({col_names})
        VALUES ({place_holder})
        ;'''
        cur.execute(cmd, col_vals)
        con.commit()