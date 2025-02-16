import re

from kiranico_scraper.items.queryable_item import QueryableItem

class SerializedItem(QueryableItem):
    def __setitem__(self, key, value):
        if key in self.fields:
            field = self.fields[key]
            setter = lambda item: item
            serializer = str

            if 'serializer' in field:
                serializer = field['serializer']

            if 'setter' in field:
                setter = field['setter']

            value = self.__value_or_default(setter(value), serializer)

            if isinstance(value, list):
                for i, item in enumerate(value):
                    value[i] = setter(self.__value_or_default(item, serializer))

            # This is here for a really annoying reason: when using scrapy's ItemLoader#add_`whatever`
            # methods, it adds it to the loader as a list and not its raw value. So here,
            # we extract the raw value from the list, if available.
            if isinstance(value, list) and value and not isinstance(serializer, list):
                value = value[0]

            self._values[key] = serializer(value)
        else:
            raise KeyError(f"{self.__class__.__name__} does not support field: {key}")


    @property
    def table_name(self):
        return self.__tableize_classname()


    @property
    def db_fields(self):
        return sorted(self.fields.keys())


    @property
    def csv_fields(self):
        return sorted([field for field in self.db_fields if field != 'id'])


    @property
    def html_fields(self):
        return []


    def __strip_whitespace(self, value):
        return re.sub(r'\s+', ' ', value.strip())


    def __value_or_default(self, value, serializer):
        if str(value).isspace():
            return serializer()

        if isinstance(value, str):
            return self.__strip_whitespace(value)

        return value


    def __tableize_classname(self):
        classname = self.__class__.__name__

        if classname.endswith('y'):
            classname = f"{classname[:-1]}ies"
        else:
            classname = f"{classname}s"

        return re.sub(r'([A-Z])', r'_\1', classname).strip('_').lower()
