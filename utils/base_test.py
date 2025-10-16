from playwright.sync_api import sync_playwright
from utils.config import CONFIG
from pages.login_page import LoginPage
import pytest


class BaseTest:
    @pytest.fixture(scope="class", autouse=True)
    def setup_class(self, request):

        if not hasattr(request.config, "_test_results_cleared"):
            with open("test_results.txt", "w") as f:
                f.write("")
            print("\n🧹 Cleared old test results.\n")
            request.config._test_results_cleared = True

        playwright = sync_playwright().start()
        browser_type = CONFIG["browser"].lower()

        # Common launch options
        launch_args = {
            "headless": False
        }

        if browser_type in ["chromium", "chrome"]:
            launch_args["args"] = ["--start-maximized"]
            browser = getattr(playwright, browser_type).launch(**launch_args)
            context = browser.new_context(no_viewport=True)

        elif browser_type == "firefox":
            # Firefox doesn't support --start-maximized
            browser = getattr(playwright, browser_type).launch(**launch_args)
            context = browser.new_context(
                viewport={"width": 1920, "height": 1080}
            )

        else:
            raise ValueError(f"Unsupported browser: {browser_type}")

        # Create page and perform login
        page = context.new_page()
        login_page = LoginPage(page)
        login_page.open()
        login_page.login(CONFIG["username"], CONFIG["password"],CONFIG["esop_pass"])

        # Attach references to test class
        request.cls.page = page
        request.cls.context = context
        request.cls.browser = browser

        yield
        context.close()
        browser.close()
        playwright.stop()
