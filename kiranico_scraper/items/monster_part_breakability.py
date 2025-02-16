from scrapy import Field
from kiranico_scraper.items.serialized_item import SerializedItem


class MonsterPartBreakability(SerializedItem):
    part = Field()
    value = Field(serializer=int)
    sever = Field()
    extract_color = Field()
    monster_id = Field(serializer=int)


    @property
    def db_unique_constraints(self):
        return ['part', 'monster_id']


    @property
    def html_fields(self):
        return ['part', 'value', 'sever', 'extract_color']
