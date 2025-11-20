import pytest
import traceback
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

from playwright.sync_api import Page
from pages.login_page import LoginPage


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)

_test_results: list[dict] = []


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield
    report = outcome.get_result()

    if report.when != "call":
        return

    error_text = None
    if report.failed and call.excinfo is not None:
        error_text = "".join(
            traceback.format_exception(
                call.excinfo.type, call.excinfo.value, call.excinfo.tb
            )
        )

    _test_results.append(
        {
            "name": item.name,
            "nodeid": report.nodeid,
            "outcome": report.outcome,
            "duration": report.duration,
            "error": error_text,
        }
    )


def pytest_sessionfinish(session, exitstatus):
    root = Path(__file__).parent

    total = len(_test_results)
    passed = sum(1 for t in _test_results if t["outcome"] == "passed")
    failed = sum(1 for t in _test_results if t["outcome"] == "failed")
    skipped = sum(1 for t in _test_results if t["outcome"] == "skipped")

    summary = {
        "total": total,
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
    }

    env = Environment(loader=FileSystemLoader(str(root)))
    template = env.get_template("config/report_template.html.j2")

    html = template.render(tests=_test_results, summary=summary)

    output_path = root / "result" / "custom_report.html"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")

    print(f"\nCustom report is generated: {output_path}")
