from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time

# Initialize the WebDriver
driver = webdriver.Chrome()
driver.get("https://shop.polymer-project.org/detail/mens_tshirts/Inbox+-+Subtle+Actions+T-Shirt")

time.sleep(2)  # Allow time for the page to load

# Function to access shadow DOM recursively
def get_shadow_element(root_element, selector):
    shadow_root = driver.execute_script("return arguments[0].shadowRoot", root_element)
    return shadow_root.find_element(By.CSS_SELECTOR, selector)

try:
    # Step 1: Find the first shadow host (shop-app)
    shop_app = driver.find_element(By.CSS_SELECTOR, "shop-app")
    print("Found button:", shop_app.tag_name)

    # Step 2: Access shadow root of shop-app and find iron-pages
    iron_pages = get_shadow_element(shop_app, "iron-pages")
    print("Found button:", iron_pages.tag_name)

    # Step 3: Find shop-detail inside iron-pages' shadow root
    shop_detail = iron_pages.find_element(By.CSS_SELECTOR, "shop-detail")
    print("Found button:", shop_detail.tag_name)

    # Step 4: Get <div class='pickers'> inside shop-detail
    pickers = get_shadow_element(shop_detail, "div.pickers")
    print("Found button:", pickers.tag_name)

    # Step 5: Get <select id='quantitySelect'> inside pickers
    quantity_select = pickers.find_element(By.CSS_SELECTOR, "shop-select select#quantitySelect")
    print("Found button:", quantity_select.tag_name)

    # Select a quantity (e.g., "3")
    select = Select(quantity_select)

    # Try selecting a value, and catch errors if the value is invalid
    try:
        select.select_by_value("10")  
        print("Successfully selected quantity to 10")
    except Exception as e:
        print("Error: Invalid quantity value. Valid values are between 1 and 5.")
        print("Details:", e)

    time.sleep(2)  # Wait to see the changes

except Exception as e:
    print("Error:", e)

# Close the browser
driver.quit()
