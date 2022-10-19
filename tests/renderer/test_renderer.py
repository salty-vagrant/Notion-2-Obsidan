import pytest
from markdown_it import MarkdownIt
from mdit_py_plugins import dollarmath
from knox.model import notion as model


@pytest.fixture(scope="function")
def data(request, testdata_dir):
    return testdata_dir / request.param


class TestRenderer:
    @pytest.mark.parametrize(
        "data, config",
        [
            ("markdown/test_files/base_markdown_test_page.md", {}),
            (
                "markdown/test_files/notion_export_markdown_test_page.md",
                {
                    "hr": "---",
                    "indent": 3,
                    "ordered_list": {"count": "+", "indent": 4},
                    "bullet_list": {"count": "", "indent": 4},
                },
            ),
        ],
        indirect=["data"],
    )
    def test_render_file_as_markdown(self, data, config):
        # pylint: disable=protected-access
        with open(data, "r") as f:
            original_content = f.read()
        md = MarkdownIt("gfm-like").use(dollarmath.dollarmath_plugin)
        parsed_page = md.parse(original_content)
        # print("\n".join([str(t) for t in parsed_page]))
        renderer = model.Page.create_renderer(data.suffix, config=config)
        produced_content = renderer.render(parsed_page)
        assert original_content == produced_content
