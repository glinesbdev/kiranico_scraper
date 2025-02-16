from scrapy import Field
from kiranico_scraper.items.serialized_item import SerializedItem


class Monster(SerializedItem):
    id = Field(serializer=int)
    name = Field()
    health = Field(serializer=int)
    description = Field()
    mini_crown = Field()
    large_crown = Field()
    king_crown = Field()


    @property
    def db_unique_constraints(self):
        return ['name']
