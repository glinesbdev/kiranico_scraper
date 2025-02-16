import csv
import os

from itemadapter import ItemAdapter


class CSVPipeline:
    def __init__(self, game, project_root):
        self.game = game
        self.csv_dir = f"{project_root}/csv/{self.game}"
        self.items = {}


    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            crawler.settings.get('GAME'),
            crawler.settings.get('PROJECT_ROOT')
        )


    def open_spider(self, spider):
        if not os.path.isdir(self.csv_dir):
            os.mkdir(self.csv_dir)


    def close_spider(self, spider):
        for kind in self.items:
            with open(f"{self.csv_dir}/{kind}.csv", 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=self.capitalize_list(self.items[kind][0].csv_fields), dialect='unix')
                writer.writeheader()

                for item in self.items[kind]:
                    writer.writerow(self.capitalize_keys({ f"{field}": item[field] for field in item.csv_fields }))


    def process_item(self, item, spider):
        if ItemAdapter.is_item(item):
            classname = item.__class__.__name__

            if not classname in self.items:
                self.items[classname] = []

            self.items[classname].append(item)

        return item


    def capitalize_keys(self, dikt):
        return { self.titleize_csv_fieldname(key): value for key, value in dikt.items() }


    def capitalize_list(self, lst):
        return [self.titleize_csv_fieldname(item) for item in lst]


    def titleize_csv_fieldname(self, fieldname):
        return fieldname.title().replace('_', ' ')
