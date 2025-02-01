from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

driver.get("https://shop.polymer-project.org/detail/mens_outerwear/Anvil+L+S+Crew+Neck+-+Grey")

import time

time.sleep(2)


# Function to access shadow DOM recursively
def get_shadow_element(root_element, selector):
    shadow_root = driver.execute_script("return arguments[0].shadowRoot", root_element)
    return shadow_root.find_element(By.CSS_SELECTOR, selector)


try:
    # Find element
    shop_app = driver.find_element(By.CSS_SELECTOR, "shop-app")
    print("Found element:", shop_app.tag_name)

    iron_pages = get_shadow_element(shop_app, "iron-pages")
    print("Found element:", iron_pages.tag_name)

    shop_detail = iron_pages.find_element(By.CSS_SELECTOR, "shop-detail")
    print("Found element:", shop_detail.tag_name)

    shop_button = get_shadow_element(shop_detail, "shop-button")
    print("Found element:", shop_button.tag_name)

    add_to_cart_button = shop_button.find_element(By.CSS_SELECTOR, "button[aria-label='Add this item to cart']")
    print("Found element:", add_to_cart_button.tag_name)

    # print button's text
    print("Found button:", add_to_cart_button.text)

    # click button
    add_to_cart_button.click()

    time.sleep(2)

    # Find shop-cart-modal window
    shop_cart_modal = get_shadow_element(shop_app, "shop-cart-modal")

    print("Found element:", shop_cart_modal.tag_name)

    modal_class = shop_cart_modal.get_attribute("class")

    # Test
    if "opened" in modal_class:
        print("Test Passed: Cart modal is displayed.")
    else:
        print("Test Failed: Cart modal is NOT displayed.")




except Exception as e:
    print("Error:", e)

driver.quit()
