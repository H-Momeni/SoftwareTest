from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.get("https://shop.polymer-project.org/detail/mens_outerwear/Anvil+L+S+Crew+Neck+-+Grey")

time.sleep(1)

def get_shadow_element(root_element, selector):
    shadow_root = driver.execute_script("return arguments[0].shadowRoot", root_element)
    return shadow_root.find_element(By.CSS_SELECTOR, selector)

shop_app = driver.find_element(By.CSS_SELECTOR, "shop-app")
shop_detail = get_shadow_element(shop_app, "iron-pages").find_element(By.CSS_SELECTOR, "shop-detail")
add_to_cart_button = get_shadow_element(shop_detail, "shop-button").find_element(By.CSS_SELECTOR, "button[aria-label='Add this item to cart']")

add_to_cart_button.click()
time.sleep(1)

cart_modal = get_shadow_element(shop_app, "shop-cart-modal")
checkout_button = get_shadow_element(cart_modal, "shop-button:nth-of-type(2)").find_element(By.CSS_SELECTOR, "a[href='/checkout']")

checkout_button.click()
time.sleep(1)

assert "/checkout" in driver.current_url, "Test Failed: Did not navigate to checkout page"

print("Test Passed: Navigated to checkout page successfully")

driver.quit()
