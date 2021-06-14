import pytest
from knox.model import base, notion
from pathlib import Path

TESTDATA_DIR = Path(__file__).parent.parent.resolve() / "assets"

# Testing Notion Datasource


@pytest.mark.parametrize(
    "data",
    [
        TESTDATA_DIR / "notion/minimal.zip",
        TESTDATA_DIR / "notion/minimal",
    ],
)
def test_open_notion_datasource(data):
    notion_data = notion.Notion(data)
    assert notion_data


@pytest.mark.parametrize(
    "data",
    [
        TESTDATA_DIR / "notion/non-existent.zip",
        TESTDATA_DIR / "notion/non-existent",
    ],
)
def test_fails_when_attempting_to_open_missing_data_source(data):
    with pytest.raises(FileNotFoundError):
        notion.Notion(data)
