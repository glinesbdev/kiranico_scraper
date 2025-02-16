import os
import scrapy

from glob import glob
from importlib import import_module
from pathlib import Path
from kiranico_scraper.adapters.postgres_adapter import PostgresAdapter


class KiranicoSpider(scrapy.Spider):
    name = 'kiranico'

    def __init__(self, game='mhworld', *args, **kwargs):
        super(KiranicoSpider, self).__init__(*args, **kwargs)
        self.game = game
        self.project_dir_path = Path(__file__).parent.parent.absolute()
        self.__init_adapters(game)


    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(KiranicoSpider, cls).from_crawler(crawler, *args, **kwargs)
        spider.settings.set('GAME', spider.game, priority='spider')
        spider.settings.set('PROJECT_ROOT', spider.project_dir_path, priority='spider')

        return spider


    def start_requests(self):
        yield from self.__parse_primary_models()
        yield from self.__parse_dependant_models()


    def __parse_primary_models(self):
        # Specific models are dependend upon by other models, think SQL Join tables.
        # So they need to come first, natrually. They need to be processed within
        # their own functions sequentially as scrapy yields items to its pipelines,
        # meaning that ordering is thrown out the window. Doing things this way guarantees
        # that specific ordering is kept as required.
        # Ordering here is paramount!
        yield from self.__parse_monsters()
        yield from self.__parse_items()
        yield from self.__parse_quests()


    def __parse_monsters(self):
        from kiranico_scraper.parsers.monsters_parser import MonstersParser

        files = glob(f"{self.project_dir_path}/html/monsters/*")
        for file in sorted(files):
            yield scrapy.Request(url=f"file://{file}", callback=MonstersParser.parse)


    def __parse_quests(self):
        from kiranico_scraper.parsers.quests_parser import QuestsParser

        files = glob(f"{self.project_dir_path}/html/quests/*")
        for file in sorted(files):
            yield scrapy.Request(url=f"file://{file}", callback=QuestsParser.parse)


    def __parse_items(self):
        from kiranico_scraper.parsers.items_parser import ItemsParser

        files = glob(f"{self.project_dir_path}/html/items/*")
        for file in sorted(files):
            yield scrapy.Request(url=f"file://{file}", callback=ItemsParser.parse)


    def __parse_dependant_models(self):
        directories = [dir for dir in glob(f"{self.project_dir_path}/html/*") if not any(exclude in dir for exclude in ['monsters', 'quests', 'items'])]
        for dir in sorted(directories):
            try:
                parser_kind = dir.split('/')[-1]
                parser_mod = import_module(f"kiranico_scraper.parsers.{parser_kind}_parser")
                parser = getattr(parser_mod, f"{parser_kind.capitalize()}Parser")

                for file in sorted(glob(f"{dir}/*")):
                    yield scrapy.Request(url=f"file://{file}", callback=parser.parse)
            except Exception:
                # If the parser doesn't exist or isn't found, skip to the next one
                continue


    def __init_adapters(self, game):
        connect_opts = {
            'database': None,
            'password': None,
            'host': os.getenv('POSTGRES_HOST'),
            'user': os.getenv('POSTGRES_USER'),
            'port': os.getenv('POSTGRES_PORT'),
        }

        match game:
            case 'mhworld':
                connect_opts['database'] = os.getenv('POSTGRES_MHWORLD_DB')
                connect_opts['password'] = os.getenv('POSTGRES_MHWORLD_PASS')

        PostgresAdapter.initialize(connect_opts)
