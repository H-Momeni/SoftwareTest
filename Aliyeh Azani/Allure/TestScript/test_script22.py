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
@allure.story("Test the checkout process with email validation")
def test_checkout_process():
    driver = webdriver.Chrome()

    try:
        # Open the target product page
        driver.get("https://shop.polymer-project.org/detail/mens_outerwear/Anvil+L+S+Crew+Neck+-+Grey")
        time.sleep(1)  # Wait for the page to load completely

        # Step 1: Find the first shadow host (shop-app)
        shop_app = driver.find_element(By.CSS_SELECTOR, "shop-app")
        allure.attach(shop_app.tag_name, name="Shop App tag")

        # Step 2: Access shadow root of shop-app and find iron-pages
        iron_pages = get_shadow_element(driver, shop_app, "iron-pages")
        allure.attach(iron_pages.tag_name, name="Iron Pages tag")

        # Step 3: Find shop-detail inside iron-pages (No shadow root needed here)
        shop_detail = iron_pages.find_element(By.CSS_SELECTOR, "shop-detail")
        allure.attach(shop_detail.tag_name, name="Shop Detail tag")

        # Step 4: Find the shop-button inside shop-detail's shadow root
        shop_button = get_shadow_element(driver, shop_detail, "shop-button")
        allure.attach(shop_button.tag_name, name="Shop Button tag")

        # Step 5: Find the "Add to Cart" button inside shop-button
        add_to_cart_button = shop_button.find_element(By.CSS_SELECTOR, "button[aria-label='Add this item to cart']")
        allure.attach(add_to_cart_button.get_attribute('aria-label'), name="Add to Cart button label")

        # Click the "Add to Cart" button
        add_to_cart_button.click()
        time.sleep(1)  # Wait for modal to appear

        # Step 6: Find shop-cart-modal inside shop-app shadow root
        shop_cart_modal = get_shadow_element(driver, shop_app, "shop-cart-modal")
        allure.attach(shop_cart_modal.get_attribute("class"), name="Cart Modal class")

        # Step 7: Find the second shop-button inside shop-cart-modal
        checkout_button = get_shadow_element(driver, shop_cart_modal, "shop-button:nth-of-type(2)")
        allure.attach(checkout_button.tag_name, name="Checkout Button tag")

        # Step 8: Find the <a> tag inside the second shop-button and click it
        checkout_link = checkout_button.find_element(By.CSS_SELECTOR, "a[href='/checkout']")
        allure.attach(checkout_link.get_attribute('href'), name="Checkout link URL")

        checkout_link.click()
        time.sleep(1)  # Wait for the checkout page to load

        # Step 9: Check for email input field in checkout page
        shop_app = driver.find_element(By.CSS_SELECTOR, "shop-app")
        iron_pages = get_shadow_element(driver, shop_app, "iron-pages")
        shop_checkout = iron_pages.find_element(By.CSS_SELECTOR, "shop-checkout")
        shop_checkout_shadow = get_shadow_element(driver, shop_checkout, "div")
        email_input = shop_checkout_shadow.find_element(By.CSS_SELECTOR, "input#accountEmail")

        # Step 10: Enter invalid email to trigger validation error
        email_input.send_keys("12@سلام")
        allure.attach("Entered email: 12@سلام", name="Email Input")

        time.sleep(1)  # Wait for validation

        # Step 11: Check if email validation error appears
        button = shop_checkout_shadow.find_element(By.CSS_SELECTOR, 'input[value="Place Order"]')
        button.click()
        time.sleep(1)

        # Step 12: Check for error message element inside shop-input
        shop_md_decorator = shop_checkout_shadow.find_element(By.CSS_SELECTOR, "shop-md-decorator")
        is_error_hidden = shop_md_decorator.get_attribute("aria-hidden") == "true"

        if is_error_hidden:
            allure.attach("No error message displayed", name="Error Check")
            print("Test Passed: No email validation error displayed.")
        else:
            allure.attach("Error message displayed", name="Error Check")
            print("Test Failed: Email validation error is displayed.")

    except Exception as e:
        print("Error:", e)
        allure.attach(str(e), name="Error Message")

    finally:
        driver.quit()
