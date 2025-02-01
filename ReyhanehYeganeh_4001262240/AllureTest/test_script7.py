import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

@pytest.fixture(scope="function")
def setup_driver():
    """Setup WebDriver and navigate to the product page"""
    driver = webdriver.Chrome()
    driver.get("https://shop.polymer-project.org/detail/mens_outerwear/Anvil+L+S+Crew+Neck+-+Grey")
    time.sleep(1)
    yield driver
    driver.quit()

@allure.step("Get shadow root of element: {selector}")
def get_shadow_element(driver, root_element, selector):
    """Access shadow DOM recursively"""
    shadow_root = driver.execute_script("return arguments[0].shadowRoot", root_element)
    return shadow_root.find_element(By.CSS_SELECTOR, selector)

@allure.feature("Cart Functionality")
@allure.story("Verify cart modal is displayed after adding an item")
def test_add_to_cart(setup_driver):
    driver = setup_driver

    with allure.step("Click 'Add to Cart' button"):
        shop_app = driver.find_element(By.CSS_SELECTOR, "shop-app")
        iron_pages = get_shadow_element(driver, shop_app, "iron-pages")
        shop_detail = iron_pages.find_element(By.CSS_SELECTOR, "shop-detail")
        shop_button = get_shadow_element(driver, shop_detail, "shop-button")
        add_to_cart_button = shop_button.find_element(By.CSS_SELECTOR, "button[aria-label='Add this item to cart']")
        add_to_cart_button.click()
        time.sleep(1)

    with allure.step("Check if cart modal is displayed"):
        shop_cart_modal = get_shadow_element(driver, shop_app, "shop-cart-modal")
        modal_class = shop_cart_modal.get_attribute("class")
        allure.attach(driver.get_screenshot_as_png(), name="Cart Modal", attachment_type=allure.attachment_type.PNG)
        assert "opened" in modal_class, "Cart modal is NOT displayed."

@allure.feature("Checkout Navigation")
@allure.story("Verify checkout button redirects to the correct page")
def test_checkout_navigation(setup_driver):
    driver = setup_driver

    with allure.step("Add item to cart and proceed to checkout"):
        shop_app = driver.find_element(By.CSS_SELECTOR, "shop-app")
        iron_pages = get_shadow_element(driver, shop_app, "iron-pages")
        shop_detail = iron_pages.find_element(By.CSS_SELECTOR, "shop-detail")
        shop_button = get_shadow_element(driver, shop_detail, "shop-button")
        add_to_cart_button = shop_button.find_element(By.CSS_SELECTOR, "button[aria-label='Add this item to cart']")
        add_to_cart_button.click()
        time.sleep(1)

        shop_cart_modal = get_shadow_element(driver, shop_app, "shop-cart-modal")
        checkout_button = get_shadow_element(driver, shop_cart_modal, "shop-button:nth-of-type(2)")
        checkout_link = checkout_button.find_element(By.CSS_SELECTOR, "a[href='/checkout']")
        checkout_link.click()
        time.sleep(1)

    with allure.step("Verify checkout page URL"):
        expected_url = "https://shop.polymer-project.org/checkout"
        allure.attach(driver.get_screenshot_as_png(), name="Checkout Page", attachment_type=allure.attachment_type.PNG)
        assert driver.current_url == expected_url, f"Did not navigate to checkout page. Current URL: {driver.current_url}"

@allure.feature("Email Validation")
@allure.story("Verify email validation error messages")
@pytest.mark.parametrize("email, expected_error", [
    ("", True),  # Empty email should show error
    ("rh@gmail.com", False),  # Valid email should NOT show error
    ("rh", True),  # Invalid email should show error
    ("rh@gmail", True)  # Incomplete email should show error
])
def test_email_validation(setup_driver, email, expected_error):
    driver = setup_driver

    with allure.step("Navigate to checkout page"):
        shop_app = driver.find_element(By.CSS_SELECTOR, "shop-app")
        iron_pages = get_shadow_element(driver, shop_app, "iron-pages")
        shop_detail = iron_pages.find_element(By.CSS_SELECTOR, "shop-detail")
        shop_button = get_shadow_element(driver, shop_detail, "shop-button")
        add_to_cart_button = shop_button.find_element(By.CSS_SELECTOR, "button[aria-label='Add this item to cart']")
        add_to_cart_button.click()
        time.sleep(2)

        shop_cart_modal = get_shadow_element(driver, shop_app, "shop-cart-modal")
        checkout_button = get_shadow_element(driver, shop_cart_modal, "shop-button:nth-of-type(2)")
        checkout_link = checkout_button.find_element(By.CSS_SELECTOR, "a[href='/checkout']")
        checkout_link.click()
        time.sleep(1)

    with allure.step("Locate email input field and place order button"):
        shop_app = driver.find_element(By.CSS_SELECTOR, "shop-app")
        iron_pages = get_shadow_element(driver, shop_app, "iron-pages")
        shop_checkout = iron_pages.find_element(By.CSS_SELECTOR, "shop-checkout")
        shop_checkout_shadow = get_shadow_element(driver, shop_checkout, "div")
        email_input = shop_checkout_shadow.find_element(By.CSS_SELECTOR, "input#accountEmail")


    with allure.step(f"Enter email: {email} and submit order"):
        email_input.clear()
        email_input.send_keys(email)
        place_order_button = shop_checkout_shadow.find_element(By.CSS_SELECTOR, 'input[value="Place Order"]')
        place_order_button.click()
        time.sleep(1)

    with allure.step("Check for email validation error"):
        shop_md_decorator = shop_checkout_shadow.find_element(By.CSS_SELECTOR, "shop-md-decorator")
        error_visible = driver.execute_script("""
                    const element = arguments[0];
                    const style = window.getComputedStyle(element, '::after');
                    return style.content !== 'none' && style.display !== 'none';
                """, shop_md_decorator)

        allure.attach(driver.get_screenshot_as_png(), name="Email Validation", attachment_type=allure.attachment_type.PNG)
        assert error_visible == expected_error, f"Test Failed for email '{email}': Expected error {expected_error}, but got {error_visible}."
