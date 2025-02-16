from glob import glob
from itemadapter import ItemAdapter
from kiranico_scraper.adapters.postgres_adapter import PostgresAdapter


class PostgresPipeline:
    def __init__(self, game):
        self.game = game
        self.dependant_relations = []


    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.get('GAME'))


    def open_spider(self, spider):
        self.__run_migrations()


    def close_spider(self, spider):
        PostgresAdapter.commit()
        PostgresAdapter.close()


    def process_item(self, item, spider):
        if ItemAdapter.is_item(item):
            item.insert()

        return item


    def __run_migrations(self):
        PostgresAdapter.set_session(autocommit=True)

        for migration in sorted(glob(f"kiranico_scraper/migrations/{self.game}/*.sql")):
            PostgresAdapter.execute(open(migration, 'r').read())

        PostgresAdapter.set_session(autocommit=False)
