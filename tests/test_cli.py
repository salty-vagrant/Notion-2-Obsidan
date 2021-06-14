from click.testing import CliRunner
from knox.cli import knox
from pathlib import Path
import pytest

TESTDATA_DIR = Path(__file__).parent.resolve() / "assets"


@pytest.mark.parametrize(
    "datafile",
    [
        TESTDATA_DIR / "notion/minimal.zip",
    ],
)
def test_file_provided(datafile):
    runner = CliRunner()
    result = runner.invoke(knox, ["import", str(datafile)])
    assert result.exit_code == 0


@pytest.mark.parametrize(
    "datafile",
    [
        TESTDATA_DIR / "non-existent.zip",
    ],
)
def test_non_existent_file_provided(datafile):
    runner = CliRunner()
    result = runner.invoke(knox, ["import", str(datafile)])
    assert result.exit_code == 2
    assert (
        f"Error: Invalid value for 'SOURCE': Path '{datafile}' does not exist."
        in result.output
    )


def test_file_NOT_provided():
    runner = CliRunner()
    result = runner.invoke(knox, ["import"])
    assert result.exit_code == 2
    assert "Error: Missing argument 'SOURCE'" in result.output
