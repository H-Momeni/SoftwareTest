import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

@allure.feature("Shop Tabs Test")
@allure.story("Verify that all expected tabs are present")
def test_check_tabs():
    driver = webdriver.Chrome()

    # Open the target website
    driver.get("https://shop.polymer-project.org/")

    time.sleep(2)

    def get_shadow_element(root_element, selector):
        shadow_root = driver.execute_script("return arguments[0].shadowRoot", root_element)
        return shadow_root.find_element(By.CSS_SELECTOR, selector)

    try:
        # Step 1: Find the shop-app element
        shop_app = driver.find_element(By.CSS_SELECTOR, "shop-app")
        # Step 2: Get the shadow root of shop-app and find the tabs
        shop_tabs = get_shadow_element(shop_app, "shop-tabs")
        categories = shop_tabs.find_elements(By.CSS_SELECTOR, "a")

        expected_tabs = ["Men's Outerwear", "Ladies Outerwear", "Men's T-Shirts", "Ladies T-Shirts"]
        actual_tabs = [tab.text.strip() for tab in categories]

        # Step 3: Check if all expected tabs are present
        for tab_name in expected_tabs:
            assert tab_name in actual_tabs, f"Test Failed: Tab '{tab_name}' not found"
            print(f"Test Passed: Tab '{tab_name}' found")

    except Exception as e:
        print("Error:", e)
    finally:
        driver.quit()

