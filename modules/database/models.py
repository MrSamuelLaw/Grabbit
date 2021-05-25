from pydantic import BaseModel
import datetime as dt

# ============== models ==============
class TableModel(BaseModel):
    __table_name__: str
    __primary_key__: str = None


class WebsiteModel(TableModel, extra='forbid'):
    __table_name__ = 'websites'
    website: str
    customer_email: str
    scraper: str = None
    instock: bool = None
    start_date: int = dt.datetime.now() # using seconds epoch
    end_date: int = None                # using the seconds epoch
