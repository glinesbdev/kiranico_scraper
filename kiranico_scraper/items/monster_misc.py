from scrapy import Field
from kiranico_scraper.items.serialized_item import SerializedItem


class MonsterMisc(SerializedItem):
    id = Field(serializer=int)
    name = Field()
    low_high_rank = Field()
    master_rank = Field()
    exhaust_duration = Field(serializer=list[str])
    monster_id = Field(serializer=int)


    @property
    def db_unique_constraints(self):
        return ['name', 'monster_id']


    @property
    def html_fields(self):
        return ['name', 'low_high_rank', 'master_rank', 'exhaust_duration']
