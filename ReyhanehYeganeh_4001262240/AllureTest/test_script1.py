import time
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By

@allure.step("Initializing WebDriver")
@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Chrome()
    driver.get("https://shop.polymer-project.org/detail/mens_outerwear/Anvil+L+S+Crew+Neck+-+Grey")
    time.sleep(2)  # Wait for page to load
    yield driver
    driver.quit()

@allure.step("Accessing shadow root of an element")
def get_shadow_element(driver, root_element, selector):
    shadow_root = driver.execute_script("return arguments[0].shadowRoot", root_element)
    return shadow_root.find_element(By.CSS_SELECTOR, selector)

@allure.feature("Add to Cart Feature")
@allure.story("Verify 'Add to Cart' button and Cart Modal")
def test_add_to_cart(driver):
    with allure.step("Find shop-app root element"):
        shop_app = driver.find_element(By.CSS_SELECTOR, "shop-app")
        assert shop_app is not None, "shop-app not found"

    with allure.step("Find iron-pages inside shop-app"):
        iron_pages = get_shadow_element(driver, shop_app, "iron-pages")
        assert iron_pages is not None, "iron-pages not found"

    with allure.step("Find shop-detail inside iron-pages"):
        shop_detail = iron_pages.find_element(By.CSS_SELECTOR, "shop-detail")
        assert shop_detail is not None, "shop-detail not found"

    with allure.step("Find shop-button inside shop-detail shadow root"):
        shop_button = get_shadow_element(driver, shop_detail, "shop-button")
        assert shop_button is not None, "shop-button not found"

    with allure.step("Find and click 'Add to Cart' button"):
        add_to_cart_button = shop_button.find_element(By.CSS_SELECTOR, "button[aria-label='Add this item to cart']")
        assert add_to_cart_button is not None, "'Add to Cart' button not found"
        add_to_cart_button.click()
        time.sleep(2)

    with allure.step("Find shop-cart-modal and verify if it is displayed"):
        shop_cart_modal = get_shadow_element(driver, shop_app, "shop-cart-modal")
        assert shop_cart_modal is not None, "shop-cart-modal not found"

        modal_class = shop_cart_modal.get_attribute("class")
        assert "opened" in modal_class, "Cart modal did not open"

    allure.attach(driver.get_screenshot_as_png(), name="Cart Modal", attachment_type=allure.attachment_type.PNG)
