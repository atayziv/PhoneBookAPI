import logging

import psycopg2

from phone_book_api_server.data_models.contacts import ContactRequest


class PostgresClient:
    def __init__(self) -> None:
        self.__logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.connection = psycopg2.connect(
            host="localhost",
            port=5432,
            database="postgres",
            user="postgres",
            password="postgres",
        )
        self.__create_table()

    def __create_table(self):
        cursor = self.connection.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS contacts(
                phone_number VARCHAR (20) PRIMARY KEY,
                first_name VARCHAR (50) NOT NULL,
                last_name VARCHAR (50) NOT NULL,
                email_address VARCHAR (100) NOT NULL
            );
            """
        )
        self.connection.commit()
        cursor.close()
        # self.connection.close()

    def insert_contact(self, data: ContactRequest):
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO contacts (phone_number, first_name, last_name, email_address) VALUES (%s, %s, %s, %s)",
            (
                data.phone_number,
                data.first_name,
                data.last_name,
                data.email_address,
            ),
        )

        cursor.close()
        # self.connection.close()
