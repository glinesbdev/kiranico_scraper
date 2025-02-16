from scrapy import Field
from kiranico_scraper.items.serialized_item import SerializedItem


class MonsterPhysiology(SerializedItem):
    id = Field(serializer=int)
    part = Field()
    sever = Field(serializer=int)
    blunt = Field(serializer=int)
    ranged = Field(serializer=int)
    fire = Field(serializer=int)
    water = Field(serializer=int)
    lightning = Field(serializer=int)
    ice = Field(serializer=int)
    dragon = Field(serializer=int)
    status = Field(serializer=int)
    stamina = Field(serializer=int)
    monster_id = Field(serializer=int)


    @property
    def db_unique_constraints(self):
        return ['part', 'monster_id']


    @property
    def html_fields(self):
        return ['part', 'sever', 'blunt', 'ranged', 'fire', 'water', 'lightning', 'ice', 'dragon', 'status', 'stamina']
