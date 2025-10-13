from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from utils.config import load_config, get_credentials
from utils.email_notifier import EmailNotifier

def test_login_success():
    cfg = load_config()
    creds = get_credentials()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=cfg["browser"]["headless"])
        page = browser.new_page()
        page.set_default_timeout(cfg["timeouts"]["default"])

        login_page = LoginPage(page, cfg["base_url"])
        login_page.open()
        success = login_page.login(creds["username"], creds["password"], creds["webpass"])

        print(f"Login result: {success}")
        print(f"Final URL: {page.url}")

        browser.close()
        
        # Send email notification
        email_notifier = EmailNotifier()
        if success:
            email_notifier.send_test_result(
                test_name="verify user can able to buy a product",
                result="Pass",
                environment="stage",
                tester="Purno"
            )
        else:
            email_notifier.send_test_result(
                test_name="verify user can able to buy a product",
                result="Fail",
                environment="stage",
                tester="Purno"
            )
