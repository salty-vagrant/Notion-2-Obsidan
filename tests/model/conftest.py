import pytest
from tempfile import mkdtemp
import shutil
from pathlib import Path


TESTDATA_SRCDIR = Path(__file__).parent.parent.resolve() / "assets"


@pytest.fixture(scope="session")
def testdata_dir(request):
    tmpdir = mkdtemp()
    testdata_path = Path(tmpdir) / "data"
    shutil.copytree(TESTDATA_SRCDIR, testdata_path)
    yield testdata_path
    shutil.rmtree(testdata_path.parent)
