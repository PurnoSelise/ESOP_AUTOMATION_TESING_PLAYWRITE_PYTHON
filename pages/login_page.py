import time

from utils.config import CONFIG


class LoginPage:
    def __init__(self, page):
        self.page = page
        self.esop_input = '//input[@id="input_wp_protect_password"]'
        self.enter_btn='//input[@type="submit"]'
        self.username_input = '//input[@placeholder="Email"]'
        self.password_input = '//input[@placeholder="Kennwort"]'
        self.login_button = '//button[normalize-space()="Anmeldung"]'
        self.cookie_btn='//button[contains(text(), "Cookies zulassen")]'
        self.cross_btn='//span[@aria-hidden="true"]'
        self.loing_btm='//img[@src="https://stgw.vorwerk-schweiz.ch/wp-content/themes/switzerland-thermomix/vw-assets/img/user.svg"]'

    def open(self):
        self.page.goto(CONFIG["base_url"])

    def login(self, username, password,esop_pass):
        self.page.fill(self.esop_input, esop_pass)
        self.page.click(self.enter_btn)
        time.sleep(2)
        self.page.fill(self.esop_input, esop_pass)
        self.page.click(self.enter_btn)
        time.sleep(2)
        self.page.click(self.cookie_btn)
        self.page.click(self.cross_btn)
        time.sleep(2)
        self.page.click(self.loing_btm)
        time.sleep(2)
        self.page.fill(self.username_input, username)
        self.page.fill(self.password_input, password)
        time.sleep(2)
        self.page.click(self.login_button)
        time.sleep(2)
        self.page.wait_for_load_state('networkidle')