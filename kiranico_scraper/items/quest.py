from scrapy import Field
from kiranico_scraper.items.serialized_item import SerializedItem


class Quest(SerializedItem):
    id = Field(serializer=int)
    name = Field()
    description = Field()
    goal = Field()
    location = Field()
    conditions = Field()
    client = Field()
    failure_conditions = Field()
    reward_money = Field()
    rewards = Field()
    time_limit = Field()
    max_players = Field()


    @property
    def db_unique_constraints(self):
        return ['name']


    @property
    def html_fields(self):
        return ['goal', 'location', 'conditions', 'client', 'failure_conditions', 'reward_money', 'rewards', 'time_limit', 'max_players']
