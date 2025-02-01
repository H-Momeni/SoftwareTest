from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()

driver.get("https://shop.polymer-project.org/detail/mens_outerwear/Anvil+L+S+Crew+Neck+-+Grey")

time.sleep(2)

# Function to access shadow DOM recursively
def get_shadow_element(root_element, selector):
    shadow_root = driver.execute_script("return arguments[0].shadowRoot", root_element)
    return shadow_root.find_element(By.CSS_SELECTOR, selector)

try:
    # Find element
    shop_app = driver.find_element(By.CSS_SELECTOR, "shop-app")

    iron_pages = get_shadow_element(shop_app, "iron-pages")

    shop_detail = iron_pages.find_element(By.CSS_SELECTOR, "shop-detail")

    shop_button = get_shadow_element(shop_detail, "shop-button")

    add_to_cart_button = shop_button.find_element(By.CSS_SELECTOR, "button[aria-label='Add this item to cart']")

    # click the "Add to Cart" button
    add_to_cart_button.click()

    time.sleep(2)

    # find shop-cart-modal window
    shop_cart_modal = get_shadow_element(shop_app, "shop-cart-modal")

    # find checkout button
    checkout_button = get_shadow_element(shop_cart_modal, "shop-button:nth-of-type(2)")

    checkout_link = checkout_button.find_element(By.CSS_SELECTOR, "a[href='/checkout']")
    print("Found Checkout button:", checkout_link.text)

    # click checkout button
    checkout_link.click()
    print("Clicked on Checkout button!")

    time.sleep(2)

    # Test
    expected_url = "https://shop.polymer-project.org/checkout"
    current_url = driver.current_url

    if current_url == expected_url:
        print("Test Passed: Successfully navigated to checkout page.")
    else:
        print("Test Failed: Did not navigate to checkout page. Current URL:", current_url)


except Exception as e:
    print("Error:", e)

driver.quit()
