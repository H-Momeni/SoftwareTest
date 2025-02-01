from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()

driver.get("https://shop.polymer-project.org/detail/mens_outerwear/Anvil+L+S+Crew+Neck+-+Grey")

time.sleep(1)

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

    # Click the "Add to Cart" button
    add_to_cart_button.click()

    time.sleep(1)

    # find checkout button
    shop_cart_modal = get_shadow_element(shop_app, "shop-cart-modal")

    checkout_button = get_shadow_element(shop_cart_modal, "shop-button:nth-of-type(2)")

    checkout_link = checkout_button.find_element(By.CSS_SELECTOR, "a[href='/checkout']")

    # click checkout button
    checkout_link.click()

    time.sleep(1)

    #-----------------------------------------------------------------------------------------------------

    # find email input
    shop_app = driver.find_element(By.CSS_SELECTOR, "shop-app")
    print("Found element:", shop_app.tag_name)

    iron_pages = get_shadow_element(shop_app, "iron-pages")
    print("Found element:", iron_pages.tag_name)

    shop_checkout = iron_pages.find_element(By.CSS_SELECTOR, "shop-checkout")
    print("Found element:", shop_checkout.tag_name)

    shop_checkout_shadow = get_shadow_element(shop_checkout, "div")
    print("Found element:", shop_checkout_shadow.tag_name)

    email_input = shop_checkout_shadow.find_element(By.CSS_SELECTOR, "input#accountEmail")

    # write value
    email_input.send_keys("rh")
    print("Entered email: rh")

    time.sleep(1)

    # find submit button
    button = shop_checkout_shadow.find_element(By.CSS_SELECTOR, 'input[value="Place Order"]')
    print("Found button:", button.tag_name)

    # submit
    button.click()

    time.sleep(1)

    # find email error
    shop_md_decorator = shop_checkout_shadow.find_element(By.CSS_SELECTOR, "shop-md-decorator")
    print("Found element:", shop_md_decorator.tag_name)

    # Test
    is_error_hidden = shop_md_decorator.get_attribute("aria-hidden") == "true"

    if is_error_hidden:
        print("Test Passed: Email validation error is displayed.")
    else:
        print("Test Failed: No email validation error displayed.")

except Exception as e:
    print("Error:", e)

# Close the browser
driver.quit()
