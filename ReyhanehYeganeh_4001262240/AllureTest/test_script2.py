import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


@allure.step("Get shadow root of element: {selector}")
def get_shadow_element(driver, root_element, selector):
    shadow_root = driver.execute_script("return arguments[0].shadowRoot", root_element)
    return shadow_root.find_element(By.CSS_SELECTOR, selector)


@allure.feature("Checkout Process")
@allure.story("Add item to cart and proceed to checkout")
def test_checkout():
    driver = webdriver.Chrome()
    driver.get("https://shop.polymer-project.org/detail/mens_outerwear/Anvil+L+S+Crew+Neck+-+Grey")
    time.sleep(2)  # Wait for page to load

    try:
        with allure.step("Find shop-app element"):
            shop_app = driver.find_element(By.CSS_SELECTOR, "shop-app")

        with allure.step("Access iron-pages inside shop-app shadow DOM"):
            iron_pages = get_shadow_element(driver, shop_app, "iron-pages")

        with allure.step("Find shop-detail inside iron-pages"):
            shop_detail = iron_pages.find_element(By.CSS_SELECTOR, "shop-detail")

        with allure.step("Access shop-button inside shop-detail shadow DOM"):
            shop_button = get_shadow_element(driver, shop_detail, "shop-button")

        with allure.step("Find and click 'Add to Cart' button"):
            add_to_cart_button = shop_button.find_element(By.CSS_SELECTOR, "button[aria-label='Add this item to cart']")
            add_to_cart_button.click()
            time.sleep(2)

        with allure.step("Find shop-cart-modal inside shop-app shadow DOM"):
            shop_cart_modal = get_shadow_element(driver, shop_app, "shop-cart-modal")

        with allure.step("Find and click 'Checkout' button"):
            checkout_button = get_shadow_element(driver, shop_cart_modal, "shop-button:nth-of-type(2)")
            checkout_link = checkout_button.find_element(By.CSS_SELECTOR, "a[href='/checkout']")
            checkout_link.click()
            time.sleep(2)

        with allure.step("Verify navigation to checkout page"):
            expected_url = "https://shop.polymer-project.org/checkout"
            current_url = driver.current_url
            assert current_url == expected_url, f"Test Failed: Expected {expected_url}, but got {current_url}"

        allure.attach(driver.get_screenshot_as_png(), name="Checkout Page", attachment_type=allure.attachment_type.PNG)

    except Exception as e:
        allure.attach(driver.get_screenshot_as_png(), name="Error Screenshot",
                      attachment_type=allure.attachment_type.PNG)
        pytest.fail(f"Test encountered an error: {e}")

    finally:
        driver.quit()
