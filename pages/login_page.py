import time
from .base_page import BasePage
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError


class LoginPage(BasePage):

    # 🔹 All XPaths in one place
    XPATHS = {
        "wartung_h3": "//h3[contains(normalize-space(.), 'Wartung') or contains(normalize-space(.), 'bald zurück')]",
        "seitenpass_input": "//input[@id='input_wp_protect_password']",
        "seitenpass_submit": "//input[@type='submit' and contains(@class, 'button-login')]",
        "user_input": "//input[@id='odc_user_name' or @name='username' or contains(@placeholder, 'User')]",
        "pass_input": "//input[@id='odc_password' or @name='password' or @type='password']",
        "submit_btn": "//button[contains(normalize-space(.), 'Anmeldung') or contains(normalize-space(.), 'Login') or @type='submit']",
        "cookie_btn": "//button[contains(text(), 'Cookies zulassen')]",
        "cross_btn": "//span[@aria-hidden='true']",
        "shop_btn": "//a[normalize-space(text())='Shop']",
        "negozio_btn": "//a[contains(text(), 'Zum Shop') or contains(text(), 'Shop') or contains(text(), 'Al negozio')]",
        "thermomix_label": "//label[@class='thermomixtm5-de']",
        "product_img": "//img[@data-src='https://stg-storage17.slsweb.ch/product-images-stg/tm7-s.png']",
        "add_to_cart_btn": "//button[contains(text(), 'In den Warenkorb')]",
        "cart_btn": "//a[@class='relative cart-contents']",
        "checkout_btn": "//a[@href='https://stgw.vorwerk-schweiz.ch/checkout/']",
    }

    def safe_action(self, func, *args, **kwargs):
        """Run an action safely without breaking flow."""
        try:
            return func(*args, **kwargs)
        except Exception:
            pass

    def open(self):
        """Open login page and prepare browser window."""
        self.goto("/login")
        self.safe_action(
            self.page.evaluate,
            "() => { window.moveTo(0, 0); window.resizeTo(screen.width, screen.height); }"
        )
        self.safe_action(self.page.set_viewport_size, {"width": 1500, "height": 1080})
        self.safe_action(self.page.context.new_page)

    def login(self, benutzername=None, passwort=None, seitenpasswort=None):
        """Main login logic."""
        page = self.page
        xp = self.XPATHS

        # Handle site password if page protected
        if self.safe_action(page.locator(xp["seitenpass_input"]).first.is_visible) or page.locator(xp["wartung_h3"]).count() > 0:
            if not seitenpasswort:
                raise ValueError("Site password required but not provided")

            for _ in range(2):
                self.safe_action(page.fill, xp["seitenpass_input"], seitenpasswort)
                self.safe_action(page.click, xp["seitenpass_submit"])
                time.sleep(2)
            self.safe_action(page.wait_for_load_state, "networkidle")

        # Normal login
        try:
            page.locator(xp["user_input"]).first.wait_for(state="visible", timeout=10000)
        except PlaywrightTimeoutError:
            print("Login form not found after site password.")
            return False

        self.safe_action(page.fill, xp["user_input"], benutzername or "")
        self.safe_action(page.fill, xp["pass_input"], passwort or "")
        self.safe_action(page.locator(xp["submit_btn"]).first.click)
        self.safe_action(page.locator(xp["cookie_btn"]).click)
        self.safe_action(page.locator(xp["cross_btn"]).click)
        time.sleep(5)

        # Shop flow
        self.safe_action(page.locator(xp["shop_btn"]).click)
        time.sleep(3)
        
        self.safe_action(page.locator(xp["negozio_btn"]).click)
        time.sleep(3)
        
        self.safe_action(page.locator(xp["thermomix_label"]).click)
        time.sleep(2)
        
        self.safe_action(page.locator(xp["product_img"]).click)
        time.sleep(2)
        
        self.safe_action(page.locator(xp["add_to_cart_btn"]).click)
        time.sleep(2)
        
        self.safe_action(page.locator(xp["checkout_btn"]).click)
        time.sleep(2)

        # Final check
        current = page.url
        print(f"Final URL: {current}")
        return not ("login" in current.lower() or "login-before-checkout" in current.lower())
