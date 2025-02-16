import psycopg2.sql as sql
import warnings

from scrapy import Item
from kiranico_scraper.adapters.postgres_adapter import PostgresAdapter


class QueryableItem(Item):
    @classmethod
    def find_by(cls, **kwargs):
        if cls.__noop(**kwargs):
            return cls()

        try:
            return cls(**PostgresAdapter.execute(cls.__where(**kwargs)).fetchone())
        except Exception:
            # Return expected default value if not found
            return cls()


    @classmethod
    def where(cls, **kwargs):
        if cls.__noop(**kwargs):
            return [cls()]

        results = []

        try:
            for row in PostgresAdapter.execute(cls.__where(**kwargs)).fetchall():
                results.append(cls(**row))

            return results
        except Exception:
            # Return expected default value if not found
            return [cls()]


    def insert(self):
        query = sql.SQL('INSERT INTO {table} ({columns}) VALUES ({values}) ON CONFLICT ({conflict}) DO NOTHING;').format(
            table=sql.Identifier(self.table_name),
            columns=sql.SQL(',').join([sql.Identifier(field) for field in self.db_fields if field != 'id']),
            values=sql.SQL(',').join([sql.Literal(self[field]) for field in self.db_fields if field != 'id']),
            conflict=sql.SQL(',').join([sql.Identifier(field) for field in self.db_unique_constraints])
        )

        PostgresAdapter.execute(query)


    @classmethod
    def __where(cls, **kwargs):
        return sql.SQL('SELECT * FROM {table} WHERE {where}').format(
            table=sql.Identifier(cls().table_name),
            where=sql.SQL(' AND ').join([sql.Composed([(sql.Identifier(key) + sql.Literal(value)).join('=')]) for key, value in kwargs.items()])
        )


    @classmethod
    def __noop(cls, **kwargs):
        for key, _value in kwargs.items():
            if not key in cls.fields:
                warnings.warn(f"{key} is not a valid key for {cls.__name__}")
                return True

        return False
