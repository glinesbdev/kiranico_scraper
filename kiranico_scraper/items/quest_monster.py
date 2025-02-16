from scrapy import Field
from kiranico_scraper.items.serialized_item import SerializedItem


class QuestMonster(SerializedItem):
    id = Field(serializer=int)
    players = Field(serializer=int)
    health = Field(serializer=int, setter=(lambda item: item.replace(',', '')))
    attack = Field()
    defense = Field()
    part_breakability = Field()
    ailments = Field(serializer=list[str])
    stun = Field()
    exhaust = Field()
    mount = Field()
    quest_id = Field(serializer=int)
    monster_id = Field(serializer=int)


    @property
    def db_unique_constraints(self):
        return ['id']


    @property
    def html_fields(self):
        return ['players', 'health', 'attack', 'defense', 'part_breakability', 'ailments', 'stun', 'exhaust', 'mount']
