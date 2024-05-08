import logging

import psycopg2

from phone_book_api_server.data_models.contacts import ContactRequest, ContactResponse


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

    def __create_table(self) -> None:
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

    def insert_contact(self, data: ContactRequest) -> None:
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
        self.connection.commit()
        cursor.close()

    def get_contact(self, contact_phone_number: str) -> ContactResponse:
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM contacts WHERE phone_number = %s;", (contact_phone_number,))
        data = cursor.fetchall()
        self.connection.commit()
        cursor.close()
        return data