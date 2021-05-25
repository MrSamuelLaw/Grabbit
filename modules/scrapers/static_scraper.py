import sqlite3
from urllib import request
from urllib.parse import urlparse
from abc import ABC, abstractmethod


class StaticScraper(ABC):
    '''Abstract Base Class for scrapers that scrape sites that
    do not need to be rendered in order to get the relevent information'''

    homepage = None

    def __init__(self) -> None:
        if not isinstance(self.homepage, (str,)):
            raise ValueError('homepage must be defined')
        else:
            path = urlparse(self.homepage)
            self.name = path.netloc

    def __conform__(self, protocol):
        if protocol is sqlite3.PrepareProtocol:
            return self.name

    @abstractmethod
    def scrape(self, content):
        '''Method that scrapes all the information necessary
        for the instock function to work properly.
        Must be over-ridden by child class'''
        pass

    @abstractmethod
    def instock(self, results):
        '''Method that sorts though the results from the
        scrape function and determines if the item is instock
        or not.
        Must be over-ridden by child class'''

    def get_content(self, url):
        '''Parses the web page and returns the content'''
        req = request.urlopen(url)
        if req.status != 200:
            raise ValueError(f'Request failed with status {req.status}')
        else:
            content = req.read().decode('utf-8')
            return content
