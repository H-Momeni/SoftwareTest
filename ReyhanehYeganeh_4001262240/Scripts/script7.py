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

    # Test 1
    if "opened" in modal_class:
        print("Test1 Passed: Cart modal is displayed.")
    else:
        print("Test1 Failed: Cart modal is NOT displayed.")

    #-----------------------------------------------------------------------------------------------------

    # find checkout button
    checkout_button = get_shadow_element(shop_cart_modal, "shop-button:nth-of-type(2)")

    checkout_link = checkout_button.find_element(By.CSS_SELECTOR, "a[href='/checkout']")
    print("Found Checkout button:", checkout_link.text)

    # click checkout button
    checkout_link.click()
    print("Clicked on Checkout button!")

    time.sleep(2)

    # Test2
    expected_url = "https://shop.polymer-project.org/checkout"
    current_url = driver.current_url

    if current_url == expected_url:
        print("Test2 Passed: Successfully navigated to checkout page.")
    else:
        print("Test2 Failed: Did not navigate to checkout page. Current URL:", current_url)

    #======================================================================================================

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

    # find submit button
    button = shop_checkout_shadow.find_element(By.CSS_SELECTOR, 'input[value="Place Order"]')
    print("Found button:", button.tag_name)

    # submit
    button.click()

    time.sleep(1)

    # find email error
    shop_md_decorator = shop_checkout_shadow.find_element(By.CSS_SELECTOR, "shop-md-decorator")
    print("Found element:", shop_md_decorator.tag_name)

    # Test3
    is_error_hidden = shop_md_decorator.get_attribute("aria-hidden") == "true"

    if is_error_hidden:
        print("Test3 Passed: Email validation error is displayed.")
    else:
        print("Test3 Failed: No email validation error displayed.")

    #-----------------------------------------------------------------------------------------------------

    # write value
    email_input.send_keys("rh@gmail.com")
    print("Entered email: rh@gmail.com")

    time.sleep(1)

    # submit
    button.click()

    time.sleep(1)

    # Test4
    is_error_hidden = shop_md_decorator.get_attribute("aria-hidden") == "true"

    if is_error_hidden:
        print("Test4 Passed: No email validation error displayed.")
    else:
        print("Test4 Failed: Email validation error is displayed.")

    #-----------------------------------------------------------------------------------------------------

    # write value
    email_input.clear()
    email_input.send_keys("rh")
    print("Entered email: rh")

    time.sleep(1)

    # submit
    button.click()

    time.sleep(1)

    # Test5
    is_error_hidden = shop_md_decorator.get_attribute("aria-hidden") == "true"

    if is_error_hidden:
        print("Test5 Passed: Email validation error is displayed.")
    else:
        print("Test5 Failed: No email validation error displayed.")

    # -----------------------------------------------------------------------------------------------------

    # write value
    email_input.clear()
    email_input.send_keys("rh@gmail")
    print("Entered email: rh@gmail")

    time.sleep(1)

    # submit
    button.click()

    time.sleep(1)

    # Test6
    is_error_hidden = shop_md_decorator.get_attribute("aria-hidden") == "true"

    if is_error_hidden:
        print("Test6 Failed: No email validation error displayed.")
    else:
        print("Test6 Passed: Email validation error is displayed.")



except Exception as e:
    print("Error:", e)

driver.quit()
