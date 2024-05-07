import json
from datetime import datetime, timezone

from fastapi_server.data_models.base import SharedBaseModel


class ModelTest(SharedBaseModel):
    aware_datetime: datetime
    unaware_datetime: datetime


def test_datetime_json_encoder() -> None:
    # Arrange
    test = ModelTest(
        aware_datetime=datetime(2021, 12, 30, 12, 34, 56, tzinfo=timezone.utc),
        unaware_datetime=datetime(2021, 12, 30, 12, 34, 56),
    )

    assert test.aware_datetime != test.unaware_datetime

    # Act
    result = json.loads(test.json())

    # Assert
    assert result["aware_datetime"] == result["unaware_datetime"]
    assert datetime.fromisoformat(result["aware_datetime"]).tzinfo == timezone.utc
    assert datetime.fromisoformat(result["unaware_datetime"]).tzinfo == timezone.utc
