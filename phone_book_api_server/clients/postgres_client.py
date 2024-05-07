import logging

import psycopg2


class PostgresClient:
    def __init__(self) -> None:
        self.__logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.connection = psycopg2.connect(
            database="postgres",
            user="postgres",
            host="localhost",
            password="postgres",
            port=5432,
        )
        self.__create_table()

    def __create_table(self):
        cur = self.connection.cursor()
        cur.execute(
            """CREATE TABLE IF NOT EXISTS contacts(
                phone_number VARCHAR (20) PRIMARY KEY,
                first_name VARCHAR (50) NOT NULL,
                last_name VARCHAR (50) NOT NULL,
                email_address VARCHAR (100) NOT NULL
            );
            """
        )
        self.connection.commit()
        cur.close()
        self.connection.close()

    @staticmethod
    def __get_extension(path: str) -> str:
        return path.split(".")[-1]

    def get_extension(self, path: str) -> str:
        self.__logger.debug("Getting extension...")
        return self.__get_extension(path)
