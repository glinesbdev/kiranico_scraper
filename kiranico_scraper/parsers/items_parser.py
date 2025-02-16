from scrapy.loader import ItemLoader
from kiranico_scraper.items.item import Item


class ItemsParser:
    @staticmethod
    def parse(response):
        loader = ItemLoader(item=Item(), response=response)
        loader.add_css('name', '.project-title .align-self-center::text')
        loader.add_css('description', '.project-info .col-sm-6:first-child::text')
        loader.add_css('rarity', '.project-info .col-sm-6:nth-child(2) tbody td:first-child strong::text')
        loader.add_css('max_count', '.project-info .col-sm-6:nth-child(2) tbody td:nth-child(2) strong::text')
        loader.add_css('buy_cost', '.project-info .col-sm-6:nth-child(2) tbody td:nth-child(3) strong::text')
        loader.add_css('sell_cost', '.project-info .col-sm-6:nth-child(2) tbody td:last-child strong::text')

        item = loader.load_item()
        yield item
