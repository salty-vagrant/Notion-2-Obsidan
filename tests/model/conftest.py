import pytest
from tempfile import mkdtemp, TemporaryDirectory
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


@pytest.fixture(scope="class")
def expected_results_dir(request):
    filename = Path(request.module.__file__)
    test_dir = Path(str(filename.with_suffix("")) + "_expected_results")
    yield test_dir
