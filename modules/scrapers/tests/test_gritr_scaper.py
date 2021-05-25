import pytest
from pathlib import Path
from modules.scrapers import GritrScraper


class TestGritrScraper():

    @pytest.fixture
    def testpage(self):
        '''Function used for mocking html content from the
        web using a page saved in memory'''
        curdir = Path(__file__).parent
        path = curdir.joinpath('test_pages/gritr_item.html')
        html = path.read_text('utf-8')
        return html

    def test_scrape(self, testpage):
        gs = GritrScraper()
        results = gs.scrape(testpage)
        assert len(results) == 1

    def test_instock(self, testpage):
        gs = GritrScraper()
        results = gs.scrape(testpage)
        instock = gs.instock(results)
        assert instock == True


if __name__ == '__main__':
    pytest.main([__file__, '-s'])