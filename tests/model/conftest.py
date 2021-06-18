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


@pytest.fixture(scope="session")
def expected_results_dir(request, tmpdir):
    filename = Path(request.module.__file__)
    test_dir = Path(filename.with_suffix(""))
    if test_dir.isdir():
        shutil.copytree(test_dir, str(tmpdir))
    yield Path(tmpdir)
