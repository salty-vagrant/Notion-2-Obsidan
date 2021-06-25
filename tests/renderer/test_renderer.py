import pytest
from markdown_it import MarkdownIt
from knox.model import notion as model


@pytest.fixture(scope="function")
def data(request, testdata_dir):
    return testdata_dir / request.param


class TestRenderer:
    @pytest.mark.parametrize(
        "data",
        [
            "markdown/test_files/base_markdown_test_page.md",
        ],
        indirect=["data"],
    )
    def test_render_page_as_markdown(self, data):
        # pylint: disable=protected-access
        with open(data, "r") as f:
            original_content = f.read()
        md = MarkdownIt("gfm-like")
        parsed_page = md.parse(original_content)
        renderer = model.Page.create_renderer(data.suffix)
        produced_content = renderer.render(parsed_page)
        assert original_content == produced_content
