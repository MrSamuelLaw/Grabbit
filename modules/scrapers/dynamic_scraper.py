from abc import ABC, abstractmethod

class DynamicScraper(ABC):

    def __init__(self) -> None:
        msg = 'Dynamic scraping is not supported at' \
              'this time, but will be in the future'
        raise NotImplementedError(msg)

    @abstractmethod
    def scrape(self):
        pass