import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


# Function to access shadow DOM recursively
def get_shadow_element(driver, root_element, selector):
    shadow_root = driver.execute_script("return arguments[0].shadowRoot", root_element)
    return shadow_root.find_element(By.CSS_SELECTOR, selector)


@allure.feature("E-Commerce Checkout Test")
@allure.story("Test adding item to cart and navigating to checkout page")
def test_checkout_process():
    # Initialize WebDriver
    driver = webdriver.Chrome()
    driver.get("https://shop.polymer-project.org/detail/mens_outerwear/Anvil+L+S+Crew+Neck+-+Grey")
    allure.attach(driver.page_source, name="Page Source", attachment_type=allure.attachment_type.HTML)

    time.sleep(1)

    try:
        # Find the first shadow host (shop-app)
        shop_app = driver.find_element(By.CSS_SELECTOR, "shop-app")
        allure.attach(shop_app.tag_name, name="Shop App tag")

        # Access shadow root and find shop-detail
        shop_detail = get_shadow_element(driver, shop_app, "iron-pages").find_element(By.CSS_SELECTOR, "shop-detail")
        allure.attach(shop_detail.tag_name, name="Shop Detail tag")

        # Find "Add to Cart" button inside shop-detail's shadow root
        add_to_cart_button = get_shadow_element(driver, shop_detail, "shop-button").find_element(By.CSS_SELECTOR,
                                                                                                 "button[aria-label='Add this item to cart']")
        allure.attach(add_to_cart_button.get_attribute('aria-label'), name="Add to Cart button label")

        # Click the "Add to Cart" button
        add_to_cart_button.click()
        allure.attach("Clicked Add to Cart", name="Add to Cart Action")
        time.sleep(1)

        # Find the shop-cart-modal
        cart_modal = get_shadow_element(driver, shop_app, "shop-cart-modal")
        allure.attach(cart_modal.get_attribute("class"), name="Cart Modal class")

        # Find the checkout button inside the modal and click it
        checkout_button = get_shadow_element(driver, cart_modal, "shop-button:nth-of-type(2)").find_element(
            By.CSS_SELECTOR, "a[href='/checkout']")
        allure.attach(checkout_button.get_attribute('href'), name="Checkout Button URL")

        checkout_button.click()
        allure.attach("Clicked Checkout", name="Checkout Action")
        time.sleep(1)

        # Verify if the URL contains "/checkout"
        assert "/checkout" in driver.current_url, "Test Failed: Did not navigate to checkout page"
        allure.attach("Navigated to checkout page successfully", name="Test Status")

        print("Test Passed: Navigated to checkout page successfully")

    except Exception as e:
        print(f"Error: {e}")
        allure.attach(str(e), name="Error Message")

    finally:
        driver.quit()
