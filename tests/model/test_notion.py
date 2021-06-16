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


@pytest.mark.parametrize(
    "data",
    [
        TESTDATA_DIR / "notion/minimal.txt",
    ],
)
def test_fails_when_attempting_to_open_wrong_type_for_datasource(data):
    with pytest.raises(base.BadDataStore):
        model.Notion(data)


@pytest.mark.parametrize(
    "data",
    [
        TESTDATA_DIR / "notion/empty.zip",
    ],
)
def test_fails_when_attempting_to_open_bad_zip_datasource(data):
    with pytest.raises(base.BadDataStore):
        model.Notion(data)


# Test Notion Page


@pytest.mark.parametrize(
    "page_ref",
    [
        {
            "datastore": model.Notion(TESTDATA_DIR / "notion/minimal"),
            "path": Path("Getting Started 1a3c3f5c5ebe44c7805dedcec04872e6.md"),
        },
    ],
)
def test_create_page_from_datastore(page_ref):
    page = model.Page(page_ref["datastore"], page_ref["path"])
    assert isinstance(page, base.IPage)
    assert page.exists


## Test Notion Markdown Parser
#
#
# @pytest.mark.parametrize(
#    "page",
#    [
#        model.Page(
#            model.Notion(TESTDATA_DIR / "notion/minimal"),
#            Path("Getting Started 1a3c3f5c5ebe44c7805dedcec04872e6.md"),
#        ),
#    ],
# )
# def test_parse_a_markdown_page(page):
#    _parser = parser.MarkdownParser()
#    parsed_page = _parser.parse(page)
#    assert isinstance(parsed_page, parser.MarkdownAST)
#
#
# @pytest.mark.skip(reason="No Yet In Play")
# def test_parse_a_database_page():
#    pass
