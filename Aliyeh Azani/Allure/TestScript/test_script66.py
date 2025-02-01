import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


# Function to access shadow DOM recursively
def get_shadow_element(driver, root_element, selector):
    shadow_root = driver.execute_script("return arguments[0].shadowRoot", root_element)
    return shadow_root.find_element(By.CSS_SELECTOR, selector)


@allure.feature("Shop Tabs Test")
@allure.story("Test if expected tabs exist on the homepage")
def test_shop_tabs():
    # Initialize WebDriver
    driver = webdriver.Chrome()
    driver.get("https://shop.polymer-project.org/")

    # Attach page source for context in the allure report
    allure.attach(driver.page_source, name="Page Source", attachment_type=allure.attachment_type.HTML)

    time.sleep(2)

    try:
        # Step 1: Find the first shadow host (shop-app)
        shop_app = driver.find_element(By.CSS_SELECTOR, "shop-app")
        allure.attach(shop_app.tag_name, name="Shop App tag")

        # Step 2: Access shadow root and find shop-tabs
        shop_tabs = get_shadow_element(driver, shop_app, "shop-tabs")
        allure.attach(shop_tabs.tag_name, name="Shop Tabs tag")

        # Step 3: Get all category links
        categories = shop_tabs.find_elements(By.CSS_SELECTOR, "a")
        actual_tabs = [tab.text.strip() for tab in categories]
        allure.attach(str(actual_tabs), name="Actual Tabs")

        # Expected tabs to check
        expected_tabs = ["Men's Outerwear", "Ladies Outerwear", "Men's T-Shirts", "Ladies T-Shirts"]
        allure.attach(str(expected_tabs), name="Expected Tabs")

        # Step 4: Verify if the expected tabs exist in the actual tabs
        for tab_name in expected_tabs:
            assert tab_name in actual_tabs, f"Test Failed: Tab '{tab_name}' not found"
            allure.attach(f"Test Passed: Tab '{tab_name}' found", name="Tab Verification Status")

    except Exception as e:
        # Attach the error message if something goes wrong
        print(f"Error: {e}")
        allure.attach(str(e), name="Error Message")

    finally:
        # Close the browser
        driver.quit()
