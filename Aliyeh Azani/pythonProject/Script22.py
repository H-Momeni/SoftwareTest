from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Initialize WebDriver
driver = webdriver.Chrome()

# Open the target website
driver.get("https://shop.polymer-project.org/detail/mens_outerwear/Anvil+L+S+Crew+Neck+-+Grey")

time.sleep(1)  # Wait for the page to load completely

# Function to access shadow DOM recursively
def get_shadow_element(root_element, selector):
    shadow_root = driver.execute_script("return arguments[0].shadowRoot", root_element)
    return shadow_root.find_element(By.CSS_SELECTOR, selector)

try:
    # Step 1: Find the first shadow host (shop-app)
    shop_app = driver.find_element(By.CSS_SELECTOR, "shop-app")

    # Step 2: Access shadow root of shop-app and find iron-pages
    iron_pages = get_shadow_element(shop_app, "iron-pages")

    # Step 3: Find shop-detail inside iron-pages (No shadow root needed here)
    shop_detail = iron_pages.find_element(By.CSS_SELECTOR, "shop-detail")

    # Step 4: Find the shop-button inside shop-detail's shadow root
    shop_button = get_shadow_element(shop_detail, "shop-button")

    # Step 5: Find the "Add to Cart" button inside shop-button
    add_to_cart_button = shop_button.find_element(By.CSS_SELECTOR, "button[aria-label='Add this item to cart']")

    # Click the "Add to Cart" button
    add_to_cart_button.click()

    time.sleep(1)  # Wait for modal to appear

    # Step 6: Find shop-cart-modal inside shop-app shadow root
    shop_cart_modal = get_shadow_element(shop_app, "shop-cart-modal")

    # Check if modal is opened
    modal_class = shop_cart_modal.get_attribute("class")

    # Step 7: Find the second shop-button inside shop-cart-modal
    checkout_button = get_shadow_element(shop_cart_modal, "shop-button:nth-of-type(2)")

    # Step 8: Find the <a> tag inside the second shop-button and click it
    checkout_link = checkout_button.find_element(By.CSS_SELECTOR, "a[href='/checkout']")

    checkout_link.click()

    time.sleep(1)  # Wait for the checkout page to load

    #-----------------------------------------------------------------------------------------------------

    # Step 1: Find the first shadow host (shop-app)
    shop_app = driver.find_element(By.CSS_SELECTOR, "shop-app")
    print("Found button:", shop_app.tag_name)


    # Step 2: Access shadow root of shop-app and find iron-pages
    iron_pages = get_shadow_element(shop_app, "iron-pages")
    print("Found button:", iron_pages.tag_name)


    # Step 3: Find shop-checkout inside iron-pages (No shadow root needed)
    shop_checkout = iron_pages.find_element(By.CSS_SELECTOR, "shop-checkout")
    print("Found button:", shop_checkout.tag_name)

    # Step 4: Access shadow root of shop-checkout
    shop_checkout_shadow = get_shadow_element(shop_checkout, "div")
    print("Found button:", shop_checkout_shadow.tag_name)


    # Step 5: Access shadow root of shop-input and find the input field
    email_input = shop_checkout_shadow.find_element(By.CSS_SELECTOR, "input#accountEmail")

    # Step 6: Enter email value
    email_input.send_keys("12@سلام")
    print("Entered email: 12@سلام")

    time.sleep(1)  # Wait for validation

    button = shop_checkout_shadow.find_element(By.CSS_SELECTOR, 'input[value="Place Order"]')
    print("Found button:", button.tag_name)

    button.click()

    time.sleep(1)

    # Step 7: Find the error message element inside shop-input
    shop_md_decorator = shop_checkout_shadow.find_element(By.CSS_SELECTOR, "shop-md-decorator")
    print("Found button:", shop_md_decorator.tag_name)

    # Step 8: Check if the error message is displayed
    is_error_hidden = shop_md_decorator.get_attribute("aria-hidden") == "true"

    if is_error_hidden:
        print("Test Passed: No email validation error displayed.")
    else:
        print("Test Failed: Email validation error is displayed.")

except Exception as e:
    print("Error:", e)

# Close the browser
driver.quit()
