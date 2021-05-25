import pytest
from pathlib import Path
from unittest.mock import Mock
from modules.scrapers import StaticScraper


class TestStaticScraper():

    @pytest.fixture
    def testpage(self):
        '''Function used for mocking html content from the
        web using a page saved in memory'''
        curdir = Path(__file__).parent
        path = curdir.joinpath('test_pages/gritr_item.html')
        html = path.read_text('utf-8')
        return html

    def test_get_content(self, testpage):
        '''Test to see if the page returns content as expected'''
        url = 'https://gritrsports.com/open-box-merrell' \
              '-jungle-moc-ct-black-size-9-width-m-j15792-9-m'
        StaticScraper.get_content = Mock(return_value=testpage)
        content = StaticScraper.get_content(StaticScraper, url)
        assert content

    def test_init(self):
        with pytest.raises(TypeError) as e:
            StaticScraper()


if __name__ == '__main__':
    pytest.main([__file__, '-s'])