from scrapy import Field
from kiranico_scraper.items.serialized_item import SerializedItem


class Item(SerializedItem):
    id = Field(serializer=int)
    name = Field()
    description = Field()
    rarity = Field()
    max_count = Field()
    buy_cost = Field()
    sell_cost = Field()


    @property
    def db_unique_constraints(self):
        return ['name']
