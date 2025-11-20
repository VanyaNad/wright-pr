import os
from playwright.sync_api import Page


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username = page.locator("#user-name")
        self.password = page.locator("#password")
        self.login_button = page.locator("#login-button")

    def open(self):
        self.page.goto("https://www.saucedemo.com/")

    def login(self, user, pwd):
        self.username.fill(user)
        self.password.fill(pwd)
        self.login_button.click()

    def creds(self, user, pwd):
        username = os.getenv(user)
        password = os.getenv(pwd)
        assert username, "USER is not set"
        assert password, "PASSWORD is not set"
        return username, password
