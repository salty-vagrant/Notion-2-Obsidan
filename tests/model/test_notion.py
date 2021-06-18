import pytest
from knox.model import base, notion as model
from pathlib import Path

GOOD_PAGES = [
    (
        "notion/minimal",
        Path("Getting Started 1a3c3f5c5ebe44c7805dedcec04872e6.md"),
    ),
    (
        "notion/minimal.zip",
        Path("Getting Started 1a3c3f5c5ebe44c7805dedcec04872e6.md"),
    ),
]


@pytest.fixture(scope="function")
def datastore(request, testdata_dir):
    return model.Notion(testdata_dir / request.param)


@pytest.fixture(scope="function")
def data(request, testdata_dir):
    return testdata_dir / request.param


@pytest.mark.usefixtures("testdata_dir")
class TestNotion:

    # Testing Notion Datasource

    @pytest.mark.parametrize(
        "data",
        [
            "notion/minimal.zip",
            "notion/minimal",
        ],
        indirect=["data"],
    )
    def test_open_notion_datasource(self, data):
        notion_data = model.Notion(data)
        assert notion_data

    @pytest.mark.parametrize(
        "data",
        [
            "notion/non-existent.zip",
            "notion/non-existent",
        ],
        indirect=["data"],
    )
    def test_fails_when_attempting_to_open_missing_data_source(self, data):
        with pytest.raises(FileNotFoundError):
            model.Notion(data)

    @pytest.mark.parametrize(
        "data",
        [
            "notion/minimal.txt",
        ],
        indirect=["data"],
    )
    def test_fails_when_attempting_to_open_wrong_type_for_datasource(self, data):
        with pytest.raises(base.BadDataStore):
            model.Notion(data)

    @pytest.mark.parametrize(
        "data",
        [
            "notion/empty.zip",
        ],
        indirect=["data"],
    )
    def test_fails_when_attempting_to_open_bad_zip_datasource(self, data):
        with pytest.raises(base.BadDataStore):
            model.Notion(data)

    # Test Notion Page

    @pytest.mark.parametrize(
        "datastore,path",
        GOOD_PAGES,
        indirect=["datastore"],
    )
    def test_create_page_from_datastore(self, datastore, path):
        page = datastore.load_page(path)
        assert isinstance(page, base.IPage)
        assert datastore.exists

    @pytest.mark.parametrize(
        "datastore,path",
        [
            (
                "notion/minimal",
                Path(
                    "Reading List 5d3ed53dffa14158b5a8956fff02e055/Media f8b83da7fb624c3f8ec44c945b2becc3/Jane Eyre and the Invention of Self 3142ec2744134c40b90387939bc13cec/Untitled.png"
                ),
            ),
        ],
        indirect=["datastore"],
    )
    def test_fail_create_page_from_non_page_resource_in_datastore(
        self, datastore, path
    ):
        with pytest.raises(base.exceptions.BadPage):
            datastore.load_page(path)

    def test_create_unattached_default_page(self):
        page = model.Page()
        assert isinstance(page, model.Page)
        assert isinstance(page, base.IPage)

    @pytest.mark.parametrize(
        "datastore,path",
        GOOD_PAGES,
        indirect=["datastore"],
    )
    def test_attach_unattached_empty_page_to_existing_page(self, datastore, path):
        page = model.Page()
        page.attach(datastore, path)
        assert isinstance(page, model.Page)

    @pytest.mark.parametrize(
        "datastore,path",
        [
            (
                "notion/minimal",
                Path("nonexistent.md"),
            ),
            (
                "notion/minimal.zip",
                Path("nonexistent.md"),
            ),
        ],
        indirect=["datastore"],
    )
    def test_fail_attempt_to_load_non_existent_page_from_datasource(
        self, datastore, path
    ):
        with pytest.raises(FileNotFoundError):
            datastore.load_page(path)

    @pytest.mark.parametrize(
        "datastore,path",
        [
            (
                "notion/minimal",
                Path("new_page.md"),
            ),
            (
                "notion/minimal.zip",
                Path("new_page.md"),
            ),
        ],
        indirect=["datastore"],
    )
    def test_create_empty_page_in_datasource(self, datastore, path):
        page = datastore.new_page(path)
        assert isinstance(page, model.Page)
        assert datastore.exists(path)
