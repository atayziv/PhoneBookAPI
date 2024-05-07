from pathlib import Path
from typing import Any, Dict, cast

import pytest
import yaml


@pytest.fixture(scope="session")
def test_data_folder() -> Path:
    return Path.cwd().parent / "tests/test_data"


@pytest.fixture(scope="session")
def config(test_data_folder: Path) -> Dict[str, Any]:
    with open(test_data_folder / "config.yaml") as file:
        return dict(yaml.safe_load(file))


@pytest.fixture(scope="session")
def examples_config(config: Dict[str, Any]) -> Dict[str, Any]:
    return cast(Dict[str, Any], config["examples"])


@pytest.fixture(scope="session")
def dummy_path() -> str:
    return "file.txt"
