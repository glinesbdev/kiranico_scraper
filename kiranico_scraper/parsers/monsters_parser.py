from scrapy.loader import ItemLoader
from kiranico_scraper.items.monster import Monster


class MonstersParser:
    @staticmethod
    def parse(response):
        loader = ItemLoader(item=Monster(), response=response)
        loader.add_css('name', '.project-title .align-self-center::text')
        loader.add_css('description', '.project-info .col-sm-6::text')
        loader.add_css('health', '.balance-table tbody tr:nth-child(1) td:nth-child(2) strong::text')
        loader.add_css('mini_crown', '.balance-table tbody tr:nth-child(2) td:nth-child(1) strong::text')
        loader.add_css('large_crown', '.balance-table tbody tr:nth-child(2) td:nth-child(2) strong::text')
        loader.add_css('king_crown', '.balance-table tbody tr:nth-child(2) td:nth-child(3) strong::text')

        yield loader.load_item()
