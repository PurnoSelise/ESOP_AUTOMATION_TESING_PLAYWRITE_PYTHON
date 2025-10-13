from playwright.sync_api import sync_playwright
from utils.config import load_config

cfg = load_config()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    # Navigate to login page
    url = cfg["base_url"] + "/login"
    print(f"Navigating to: {url}")
    page.goto(url)
    page.wait_for_load_state("networkidle")
    
    # Check for maintenance page
    maintenance_xpath = "//h3[text()='Webseite in Wartung: Wir sind bald zurück.']"
    if page.locator(maintenance_xpath).count() > 0:
        print("Maintenance page found")
        
        # Enter site password
        site_password_xpath = "//input[@id='input_wp_protect_password']"
        if page.locator(site_password_xpath).count() > 0:
            print("Site password field found")
            page.fill(site_password_xpath, "@fGa<2Qz73!:")
            
            site_submit_xpath = "//input[@type='submit' and contains(@class, 'button-login')]"
            if page.locator(site_submit_xpath).count() > 0:
                print("Site submit button found")
                page.click(site_submit_xpath)
                page.wait_for_load_state("networkidle")
            else:
                print("Site submit button not found")
        else:
            print("Site password field not found")
    else:
        print("Maintenance page not found")
    
    # Take screenshot
    page.screenshot(path="debug_after_site_password.png")
    print("Screenshot saved as debug_after_site_password.png")
    
    # Print all input fields on the page
    inputs = page.locator("input").all()
    print(f"\nFound {len(inputs)} input fields:")
    for i, inp in enumerate(inputs):
        try:
            inp_type = inp.get_attribute("type") or "text"
            inp_name = inp.get_attribute("name") or "no-name"
            inp_id = inp.get_attribute("id") or "no-id"
            inp_class = inp.get_attribute("class") or "no-class"
            print(f"  {i+1}. Type: {inp_type}, Name: {inp_name}, ID: {inp_id}, Class: {inp_class}")
        except:
            print(f"  {i+1}. Could not get attributes")
    
    # Check for specific login fields
    login_username_xpath = "//input[@id='odc_user_name']"
    login_password_xpath = "//input[@id='odc_password']"
    
    print(f"\nChecking for login fields:")
    print(f"Username field (odc_user_name): {page.locator(login_username_xpath).count()}")
    print(f"Password field (odc_password): {page.locator(login_password_xpath).count()}")
    
    # Try alternative selectors
    alternatives = [
        'input[name*="user"]',
        'input[name*="email"]',
        'input[id*="user"]',
        'input[id*="email"]',
        'input[type="email"]',
        'input[type="text"]'
    ]
    
    print(f"\nTrying alternative selectors:")
    for selector in alternatives:
        count = page.locator(selector).count()
        if count > 0:
            print(f"Found {count} elements with: {selector}")
    
    input("Press Enter to close browser...")
    browser.close()
