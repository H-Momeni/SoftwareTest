import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

@allure.step("Get shadow root of element: {selector}")
def get_shadow_element(driver, root_element, selector):
    """Access shadow DOM recursively"""
    shadow_root = driver.execute_script("return arguments[0].shadowRoot", root_element)
    return shadow_root.find_element(By.CSS_SELECTOR, selector)

@allure.feature("Checkout Process")
@allure.story("Verify email validation on checkout")
def test_checkout():
    driver = webdriver.Chrome()
    driver.get("https://shop.polymer-project.org/detail/mens_outerwear/Anvil+L+S+Crew+Neck+-+Grey")
    time.sleep(1)  # Wait for page to load

    try:
        with allure.step("Find and click 'Add to Cart' button"):
            shop_app = driver.find_element(By.CSS_SELECTOR, "shop-app")
            iron_pages = get_shadow_element(driver, shop_app, "iron-pages")
            shop_detail = iron_pages.find_element(By.CSS_SELECTOR, "shop-detail")
            shop_button = get_shadow_element(driver, shop_detail, "shop-button")
            add_to_cart_button = shop_button.find_element(By.CSS_SELECTOR, "button[aria-label='Add this item to cart']")
            add_to_cart_button.click()
            time.sleep(1)

        with allure.step("Find and click 'Checkout' button"):
            shop_cart_modal = get_shadow_element(driver, shop_app, "shop-cart-modal")
            checkout_button = get_shadow_element(driver, shop_cart_modal, "shop-button:nth-of-type(2)")
            checkout_link = checkout_button.find_element(By.CSS_SELECTOR, "a[href='/checkout']")
            checkout_link.click()
            time.sleep(1)

        with allure.step("Access checkout page and find 'Place Order' button"):
            iron_pages = get_shadow_element(driver, shop_app, "iron-pages")
            shop_checkout = iron_pages.find_element(By.CSS_SELECTOR, "shop-checkout")
            shop_checkout_shadow = get_shadow_element(driver, shop_checkout, "div")

            button = shop_checkout_shadow.find_element(By.CSS_SELECTOR, 'input[value="Place Order"]')
            button.click()
            time.sleep(1)

        with allure.step("Verify email validation error is displayed"):
            shop_md_decorator = shop_checkout_shadow.find_element(By.CSS_SELECTOR, "shop-md-decorator")
            is_error_hidden = shop_md_decorator.get_attribute("aria-hidden") == "true"

            assert is_error_hidden, "Test Failed: No email validation error displayed"
            allure.attach(driver.get_screenshot_as_png(), name="Validation Error", attachment_type=allure.attachment_type.PNG)

    except Exception as e:
        allure.attach(driver.get_screenshot_as_png(), name="Error Screenshot", attachment_type=allure.attachment_type.PNG)
        pytest.fail(f"Test encountered an error: {e}")

    finally:
        driver.quit()
