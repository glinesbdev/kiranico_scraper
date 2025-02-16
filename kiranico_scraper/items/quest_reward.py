from scrapy import Field
from kiranico_scraper.items.serialized_item import SerializedItem


class QuestReward(SerializedItem):
    id = Field(serializer=int)
    amount = Field(serializer=int, setter=(lambda item: item.replace('x', '')))
    percentage = Field(serializer=int, setter=(lambda item: item.replace('%', '')))
    item_id = Field(serializer=int)
    quest_id = Field(serializer=int)


    @property
    def db_unique_constraints(self):
        return ['id']
