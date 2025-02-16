import psycopg2
import warnings

from psycopg2.extras import RealDictCursor


class PostgresAdapter:
    connection = None
    cursor = None
    connect_keys = ['password', 'database', 'host', 'user', 'port']


    @classmethod
    def initialize(cls, connect_opts={}):
        if cls.__check_connected():
            return

        if not all(key in connect_opts.keys() for key in cls.connect_keys):
            return

        cls.connection = psycopg2.connect(**connect_opts)
        cls.cursor = cls.connection.cursor(cursor_factory=RealDictCursor)


    @classmethod
    def set_session(cls, **kwargs):
        if cls.__connected():
            cls.connection.set_session(**kwargs)


    @classmethod
    def commit(cls):
        if cls.__connected():
            cls.connection.commit()


    @classmethod
    def fetchall(cls):
        if cls.__connected():
            return cls.cursor.fetchall()


    @classmethod
    def fetchone(cls):
        if cls.__connected():
            return cls.cursor.fetchone()


    @classmethod
    def close(cls):
        if cls.__connected():
            cls.cursor.close()
            cls.connection.close()


    @classmethod
    def execute(cls, query):
        if cls.__connected():
            cls.cursor.execute(query)
            return cls


    @classmethod
    def __connected(cls):
        if not cls.__check_connected():
            warnings.warn('PostgresAdapter is not connected to the database!')
            return False

        return True


    @classmethod
    def __check_connected(cls):
        return cls.connection and cls.cursor
