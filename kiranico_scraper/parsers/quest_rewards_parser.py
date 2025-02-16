from kiranico_scraper.helpers.parser_helper import content_container
from kiranico_scraper.items.item import Item
from kiranico_scraper.items.quest import Quest
from kiranico_scraper.items.quest_reward import QuestReward


class QuestRewardsParser:
    def __init__(self, quest_name):
        self.quest_name = quest_name


    def parse(self, response):
        container = content_container('Quest Rewards', response, additional_path='/div/div/')
        rows = container.css('tbody tr')

        for row in rows:
            item_name = row.css('td:first-child a span::text').get()
            item = Item.find_by(name=item_name)
            quest = Quest.find_by(name=self.quest_name)

            if not 'id' in item or not 'id' in quest:
                continue

            quest_reward = QuestReward()
            amount = row.css('td:first-child::text').get()
            quest_reward['amount'] = amount if str(amount or '').strip() else 'x1'
            quest_reward['percentage'] = row.css('td:last-child::text').get()
            quest_reward['item_id'] = item['id']
            quest_reward['quest_id'] = quest['id']

            yield quest_reward
