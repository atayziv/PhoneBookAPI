import pytest
import testing.postgresql
from pytest_mock import MockerFixture
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from phone_book_api_server.clients.db_client import PostgreSQLClient
from phone_book_api_server.data_models.contacts import ContactResponse
from phone_book_api_server.database.models import Contacts
from phone_book_api_server.exceptions.contact import ContactAlreadyExist, ContactNotFoundError


def test_insert_contact_client(
    dummy_contact_insert_request: Contacts,
    mocker: MockerFixture,
) -> None:
    """Test Insert Contact Client."""
    # Create a testing PostgreSQL instance
    with testing.postgresql.Postgresql(port=7654) as psql:
        # Arrange
        engine = create_engine(psql.url())
        db = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        mocker.patch("sqlalchemy.orm.sessionmaker", return_value=db)
        mocker.patch("sqlalchemy.create_engine", return_value=engine)
        postgres_obj = PostgreSQLClient()
        # Act
        postgres_obj.insert_contact(dummy_contact_insert_request)


def test_insert_contact_client_error(
    mocker: MockerFixture,
    dummy_contact_insert_request: Contacts,
) -> None:
    """Test Insert Contact Client."""
    with testing.postgresql.Postgresql(port=7654) as psql:
        # Arrange
        engine = create_engine(psql.url())
        db = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        mocker.patch("sqlalchemy.orm.sessionmaker", return_value=db)
        mocker.patch("sqlalchemy.create_engine", return_value=engine)
        postgres_obj = PostgreSQLClient()
        mock_session = mocker.Mock()
        mocker.patch.object(postgres_obj, "SessionLocal", return_value=mock_session)
        mock_session.add.side_effect = Exception("Some error message")

        # Act
        with pytest.raises(ContactAlreadyExist):
            postgres_obj.insert_contact(dummy_contact_insert_request)


def test_get_contacts_list_client(
    mocker: MockerFixture, dummy_limit_pagination_feature: int
) -> None:
    """Test Get Contacts List Client."""
    with testing.postgresql.Postgresql(port=7654) as psql:
        # Arrange
        engine = create_engine(psql.url())
        db = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        mocker.patch("sqlalchemy.orm.sessionmaker", return_value=db)
        mocker.patch("sqlalchemy.create_engine", return_value=engine)
        postgres_obj = PostgreSQLClient()
        # Act
        postgres_obj.get_contacts(dummy_limit_pagination_feature)


def test_get_contact_client(mocker: MockerFixture, dummy_phone_number: str) -> None:
    """Test Get Contact Client."""
    # Arrange
    with testing.postgresql.Postgresql(port=7654) as psql:
        # Arrange
        engine = create_engine(psql.url())
        db = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        mocker.patch("sqlalchemy.orm.sessionmaker", return_value=db)
        mocker.patch("sqlalchemy.create_engine", return_value=engine)
        postgres_obj = PostgreSQLClient()
        mock_session = mocker.Mock()
        mocker.patch.object(postgres_obj, "SessionLocal", return_value=mock_session)
        mock_session.query.filter_by.one.return_value = None
        # Act
        postgres_obj.get_contact(dummy_phone_number)


def test_get_contact_client_error(mocker: MockerFixture, dummy_phone_number: str) -> None:
    """Test Get Contact Client With Error."""
    # Arrange
    with testing.postgresql.Postgresql(port=7654) as psql:
        # Arrange
        engine = create_engine(psql.url())
        db = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        mocker.patch("sqlalchemy.orm.sessionmaker", return_value=db)
        mocker.patch("sqlalchemy.create_engine", return_value=engine)
        postgres_obj = PostgreSQLClient()
        mock_session = mocker.Mock()
        mocker.patch.object(postgres_obj, "SessionLocal", return_value=mock_session)
        mock_session.query.side_effect = Exception
        # Act
        with pytest.raises(ContactNotFoundError):
            postgres_obj.get_contact(dummy_phone_number)


def test_update_contact_client(
    mocker: MockerFixture, dummy_phone_number: str, update_contact_data_response: ContactResponse
):
    """Test Update Contact Client."""
    # Arrange
    with testing.postgresql.Postgresql(port=7654) as psql:
        # Arrange
        engine = create_engine(psql.url())
        db = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        mocker.patch("sqlalchemy.orm.sessionmaker", return_value=db)
        mocker.patch("sqlalchemy.create_engine", return_value=engine)
        postgres_obj = PostgreSQLClient()
        mock_session = mocker.Mock()
        mocker.patch.object(postgres_obj, "SessionLocal", return_value=mock_session)
        mock_session.query.filter_by.update.return_value = None
        # Act
        postgres_obj.update_contact(dummy_phone_number, update_contact_data_response)


def test_update_contact_client_error(
    mocker: MockerFixture, dummy_phone_number: str, update_contact_data_response: ContactResponse
):
    """Test Update Contact Client With Error."""
    # Arrange
    with testing.postgresql.Postgresql(port=7654) as psql:
        # Arrange
        engine = create_engine(psql.url())
        db = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        mocker.patch("sqlalchemy.orm.sessionmaker", return_value=db)
        mocker.patch("sqlalchemy.create_engine", return_value=engine)
        postgres_obj = PostgreSQLClient()
        mock_session = mocker.Mock()
        mocker.patch.object(postgres_obj, "SessionLocal", return_value=mock_session)
        mock_session.query = Exception
        # Act
        with pytest.raises(ContactAlreadyExist):
            postgres_obj.update_contact(dummy_phone_number, update_contact_data_response)


def test_delete_contact_client(mocker: MockerFixture, dummy_phone_number: str) -> None:
    """Test Delete Contact Client."""
    # Arrange
    with testing.postgresql.Postgresql(port=7654) as psql:
        # Arrange
        engine = create_engine(psql.url())
        db = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        mocker.patch("sqlalchemy.orm.sessionmaker", return_value=db)
        mocker.patch("sqlalchemy.create_engine", return_value=engine)
        postgres_obj = PostgreSQLClient()
        mock_session = mocker.Mock()
        mocker.patch.object(postgres_obj, "SessionLocal", return_value=mock_session)
        mock_session.query.filter_by.delete.return_value = None
        # Act
        postgres_obj.delete_contact(dummy_phone_number)
