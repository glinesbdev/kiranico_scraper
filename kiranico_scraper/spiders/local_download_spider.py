import os
import scrapy

from pathlib import Path


class LocalDownloadSpider(scrapy.Spider):
    name = 'local_download'

    def __init__(self, game='mhworld', *args, **kwargs):
        super(LocalDownloadSpider, self).__init__(*args, **kwargs)
        self.game = game


    def start_requests(self):
        base_url = f"https://{self.game}.kiranico.com/en"
        self.pages = ['monsters', 'quests', 'items', 'weapons', 'armorseries', 'skilltrees',
                     'decorations', 'catseries', 'melodies', 'kinsects', 'catskills', 'foods',
                     'crafting', 'safari', 'melder', 'provisions', 'specialtools', 'deliveries',
                     'bounties', 'pendants', 'room']

        for page in self.pages:
            if not os.path.isdir(f"kiranico_scraper/html/{page}"):
                yield scrapy.Request(url=f"{base_url}/{page}", callback=getattr(self, f"parse_{page}"))


    def parse_monsters(self, response):
        links = response.css('.content-box.p-4 a::attr(href)').getall()

        for link in links:
            yield response.follow(url=link, callback=self.__download_file)


    def parse_quests(self, response):
        links = response.css("a[href*='/quests/']::attr(href)").getall()

        for link in links:
            yield response.follow(url=link, callback=self.__download_file)


    def parse_items(self, response):
        links = response.css("a[href*='/items/']::attr(href)").getall()

        for link in links:
            yield response.follow(url=link, callback=self.__download_file)


    def parse_weapons(self, response):
        links = response.css("a[href*='/weapons/']::attr(href)").getall()

        for link in links:
            yield response.follow(url=link, callback=self.__download_file)


    def parse_armorseries(self, response):
        links = response.css("a[href*='/armorseries/']::attr(href)").getall()

        for link in links:
            yield response.follow(url=link, callback=self.__download_file)


    def parse_skilltrees(self, response):
        links = response.css("a[href*='/skilltrees/']::attr(href)").getall()

        for link in links:
            yield response.follow(url=link, callback=self.__download_file)


    def parse_decorations(self, response):
        links = response.css("a[href*='/items/']::attr(href)").getall()

        for link in links:
            yield response.follow(url=link, callback=self.__download_file)


    def parse_catseries(self, response):
        self.__download_file(response)


    def parse_melodies(self, response):
        self.__download_file(response)


    def parse_kinsects(self, response):
        self.__download_file(response)
        links = response.css("a[href*='/items/']::attr(href)").getall()

        for link in links:
            yield response.follow(url=link, callback=self.__download_file)


    def parse_catskills(self, response):
        self.__download_file(response)


    def parse_foods(self, response):
        self.__download_file(response)


    def parse_crafting(self, response):
        self.__download_file(response)


    def parse_safari(self, response):
        self.__download_file(response)


    def parse_melder(self, response):
        self.__download_file(response)
        links = response.css("td > a[href*='/items/']::attr(href)").getall()

        for link in links:
            yield response.follow(url=link, callback=self.__download_file)


    def parse_provisions(self, response):
        self.__download_file(response)


    def parse_specialtools(self, response):
        self.__download_file(response)


    def parse_deliveries(self, response):
        self.__download_file(response)


    def parse_bounties(self, response):
        self.__download_file(response)


    def parse_pendants(self, response):
        self.__download_file(response)


    def parse_room(self, response):
        links = response.css("a[href*='/items/']::attr(href)").getall()

        for link in links:
            yield response.follow(url=link, callback=self.__download_file)


    def __download_file(self, response):
        directory = next(iter(set(response.url.split('/')).intersection(set(self.pages))))
        directory_path = f"kiranico_scraper/html/{directory}"
        filename = f"{response.url.split('/')[-1]}.html"
        filepath = f"{directory_path}/{filename}"

        if not os.path.isdir(directory_path):
            os.mkdir(directory_path)

        if not os.path.exists(filepath):
            Path(filepath).write_bytes(response.body)
