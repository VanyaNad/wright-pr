from playwright.sync_api import Page,expect

def test_successful_login(page: Page, login_page):
    login_page.open()
    username, password = login_page.creds("STAND_USER","PASSWORD")
    login_page.login(username, password)
    expect(page.get_by_text("Products")).to_be_visible()
    expect(page.get_by_text("Swag Labs")).to_be_visible()

def test_locked_login(page: Page, login_page):
    login_page.open()
    username, password = login_page.creds("LOCKED_USER","PASSWORD")
    login_page.login(username, password)
    expect(page.get_by_text("Epic sadface: Sorry, this user has been locked out.")).to_be_visible()

def test_problem_login(page: Page, login_page):
    login_page.open()
    username, password = login_page.creds("PROBLEM_USER", "PASSWORD")
    login_page.login(username, password)
    page.get_by_text("Sauce Labs Backpack").click()
    expect(page.get_by_text("Sauce Labs Fleece Jacket")).to_be_visible()


def test_perf_glitch_login(page: Page, login_page):
    login_page.open()
    username, password = login_page.creds("PERF_GLITCH_USER", "PASSWORD")
    login_page.login(username, password)
    expect(page.get_by_text("Products")).to_be_visible(timeout=500)

def test_error_login(page: Page, login_page):
    login_page.open()
    username, password = login_page.creds("ERROR_USER", "PASSWORD")
    login_page.login(username, password)
    expect(page.get_by_text("Swag Labs")).to_be_visible()

def test_visual_login(page: Page, login_page):
    login_page.open()
    username, password = login_page.creds("VISUAL_USER", "PASSWORD")
    login_page.login(username, password)
    expect(page.get_by_text("Products")).to_be_visible()
