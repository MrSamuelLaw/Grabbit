import re
from typing import List
from bs4 import BeautifulSoup as BS
from modules.scrapers import StaticScraper


class GritrScraper(StaticScraper):

    homepage = str(r'https://gritrsports.com/shooting/firearms/')

    def __init__(self) -> None:
        super().__init__()

    def scrape(self, content) -> List[str]:
        '''Returns the data necessary for the
        instock function to work'''
        soup = BS(content, 'html.parser')             # load html content into scraper
        data = soup.find_all('meta')                  # find all the meta tags
        c = re.compile(r'(property.*availability)')   # compile regex expression
        data = [r for r in data if c.search(str(r))]  # filter using expression
        return data                                   # return the scraped data

    def instock(self, data) -> bool:
        '''Checks the data to see if the item is in stock'''
        c = re.compile(r'(instock)')
        instock = any([r for r in data if c.search(str(r))])
        return instock
