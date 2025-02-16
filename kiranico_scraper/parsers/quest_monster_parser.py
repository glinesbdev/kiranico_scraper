from itertools import batched
from kiranico_scraper.helpers.parser_helper import content_container
from kiranico_scraper.items.monster import Monster
from kiranico_scraper.items.quest import Quest
from kiranico_scraper.items.quest_monster import QuestMonster


class QuestMonsterParser:
    def __init__(self, quest_name):
        self.quest_name = quest_name


    def parse(self, response):
        container = content_container('Monsters', response)
        monster_names = container.css("tbody tr td[rowspan='5'] div a span::text").getall()
        monster_data = container.xpath("./table/tbody/tr[descendant::td[not(@rowspan)]]")
        batched_rows = batched(monster_data, len(monster_data) // len(monster_names))

        for i, batch in enumerate(batched_rows):
            quest_monster = QuestMonster(ailments=[])

            for row in batch:
                quest_monster['ailments'].clear()
                quest_monster['players'] = row.css('td:first-child::text').get()
                quest_monster['health'] = row.css('td:nth-child(2)::text').get()
                quest_monster['attack'] = row.css('td:nth-child(3)::text').get()
                quest_monster['defense'] = row.css('td:nth-child(4)::text').get()
                quest_monster['part_breakability'] = row.css('td:nth-child(5)::text').get()
                quest_monster['ailments'].append(row.css('td:nth-child(6)::text').get())
                quest_monster['ailments'].append(row.css('td:nth-child(7)::text').get())
                quest_monster['stun'] = row.css('td:nth-child(8)::text').get()
                quest_monster['exhaust'] = row.css('td:nth-child(9)::text').get()
                quest_monster['mount'] = row.css('td:nth-child(10)::text').get()
                quest_monster['monster_id'] = Monster.find_by(name=monster_names[i])['id']
                quest_monster['quest_id'] = Quest.find_by(name=self.quest_name)['id']

                yield quest_monster
