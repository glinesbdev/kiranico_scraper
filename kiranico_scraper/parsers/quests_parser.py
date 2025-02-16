from scrapy.loader import ItemLoader
from kiranico_scraper.items.quest import Quest
from kiranico_scraper.parsers.quest_monster_parser import QuestMonsterParser
from kiranico_scraper.parsers.quest_rewards_parser import QuestRewardsParser
from kiranico_scraper.parsers.quest_supplies_parser import QuestSuppliesParser


class QuestsParser:
    @staticmethod
    def parse(response):
        loader = ItemLoader(item=Quest(), response=response)
        loader.add_css('name', '.project-title h5::text')
        loader.add_css('description', '.project-info .col-lg-6:first-child::text')

        for i, field in enumerate(Quest().html_fields):
            loader.add_css(field, f".project-info .col-lg-6:nth-child(2) tbody tr:nth-child({i+1}) td strong::text")

        quest = loader.load_item()

        yield quest
        yield from QuestMonsterParser(quest['name']).parse(response)
        yield from QuestRewardsParser(quest['name']).parse(response)
        yield from QuestSuppliesParser(quest['name']).parse(response)
