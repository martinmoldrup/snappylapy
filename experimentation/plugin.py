"""
Pytest plugin for snapshot testing.


"""
import pytest
from snappylapy import Expect
from dataclasses import dataclass
import jinja2
import pathlib
import difflib
# from diff_match_patch import diff_match_patch

HTML_REPORT_TEMPLATE = pathlib.Path(__file__).parent.parent / "snappylapy" / "report_template.html"

@pytest.fixture
def expect(request) -> Expect:
    """Initialize the snapshot object with update_snapshots flag from pytest option."""
    update_snapshots = request.config.getoption("--snapshot-update")
    return Expect(update_snapshots=update_snapshots)

# TODO https://github.com/pytest-dev/pytest-html/blob/master/src/pytest_html/plugin.py
@dataclass
class SnappylapyReportItem:
    name: str
    outcome: str
    expect: Expect


def pytest_addoption(parser):
    group = parser.getgroup("terminal reporting")
    group.addoption(
        "--snapshot-update",
        action="store_true",
        dest="snapshot_update",
        default=False,
        help="update snapshots.",
    )
    group.addoption(
        "--snappylapy-html",
        action="store",
        dest="htmlpath",
        metavar="path",
        default=None,
        help="create html report file showing the diffs at given path.",
    )

def pytest_configure(config) -> None:
    htmlpath = config.getoption("htmlpath")
    if htmlpath:
        config._snappylapy_htmlpath = htmlpath
        config._snappylapy_results = []

def pytest_terminal_summary(terminalreporter, exitstatus, config) -> None:
    htmlpath = getattr(config, "_snappylapy_htmlpath", None)
    if htmlpath:
        # dmp = diff_match_patch()
        results: list[SnappylapyReportItem] = getattr(config, "_snappylapy_results", [])
        html_string = jinja2.Template(HTML_REPORT_TEMPLATE.read_text()).render(results=results)
        pathlib.Path(htmlpath).write_text(html_string)
        for result in results:
            snapshot = result.expect.read_snapshot()
            result_data = result.expect.read_test_results()
            # diff = dmp.diff_main(snapshot.decode(), result_data.decode())
            # dmp.diff_cleanupSemantic(diff)
            # result_html = dmp.diff_prettyHtml(diff)
            # Use difflib instead of diff_match_patch
            # difflib_result = difflib.ndiff(snapshot.decode().splitlines(), result_data.decode().splitlines())
            result_html = difflib.HtmlDiff().make_file(snapshot.decode().splitlines(), result_data.decode().splitlines())
            path = pathlib.Path(htmlpath).parent / f"{result.name}.html"
            path.write_text(result_html)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call) -> None:
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and "expect" in item.funcargs:
        config = item.config
        expect_object = item.funcargs['expect']
        if hasattr(config, "_snappylapy_results"):
            config._snappylapy_results.append(
                SnappylapyReportItem(
                    name=item.name,
                    outcome=rep.outcome,
                    expect=expect_object
                )
            )

if __name__ == "__main__":
    pytest.main(["--snapshot-update", "--snappylapy-html", "report.html"])