import pytest
from knox.model import base, notion as model
from knox.parser import notion as parser
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
    notion_data = model.Notion(data)
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
        model.Notion(data)


# Test Notion Page


@pytest.mark.parametrize(
    "page",
    [
        model.Page(
            model.Notion(TESTDATA_DIR / "notion/minimal"),
            Path("Getting Started 1a3c3f5c5ebe44c7805dedcec04872e6.md"),
        ),
    ],
)
def test_parse_a_markdown_page(page):
    parsed_page = model.Page.parse(parser.MarkdownParser())
    assert isinstance(parsed_page, parser.MarkdownAST)


@pytest.mark.skip(reason="No Yet In Play")
def test_parse_a_database_page():
    pass
