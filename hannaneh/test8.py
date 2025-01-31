from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Function to access Shadow DOM recursively
def get_shadow_element(root_element, selector):
    shadow_root = driver.execute_script("return arguments[0].shadowRoot", root_element)
    return shadow_root.find_element(By.CSS_SELECTOR, selector)

# Set up WebDriver
driver = webdriver.Firefox()

# Open the target website
driver.get("https://shop.polymer-project.org/")
time.sleep(5)  # Wait for the page to fully load

try:
    # Step 1: Locate the main element `shop-app`
    shop_app = driver.find_element(By.CSS_SELECTOR, "shop-app")
    print("✅ shop-app found:", shop_app.tag_name)

    # Step 2: Access shadow root of `shop-app` and find `iron-pages`
    iron_pages = get_shadow_element(shop_app, "iron-pages")
    print("✅ iron-pages found:", iron_pages.tag_name)

    # Step 3: Find `shop-home` inside `iron-pages` (no shadow root needed)
    shop_home = iron_pages.find_element(By.CSS_SELECTOR, "shop-home.iron-selected")
    print("✅ shop-home found:", shop_home.tag_name)

    # Step 4: Access the shadow root of `shop-home` before finding elements inside it
    shop_home_shadow = driver.execute_script("return arguments[0].shadowRoot", shop_home)

    # Step 5: Locate the correct button using aria-label
    button = shop_home_shadow.find_element(By.CSS_SELECTOR, "a[aria-label=\"Men's T-Shirts Shop Now\"]")
    print("✅ Correct button found:", button.tag_name)

    # Verify the button's text
    assert button.text.strip() == "SHOP NOW", f"Button text does not match! Expected: 'Shop Now', Found: '{button.text.strip()}'"
    print("✅ Button text is correct:", button.text.strip())

    # Click the button
    button.click()
    print("✅ Button clicked successfully.")

    # Wait for the new page to load
    time.sleep(5)

    # Verify the URL
    expected_url = "https://shop.polymer-project.org/list/mens_tshirts"
    current_url = driver.current_url
    assert current_url == expected_url, f"URL does not match! Expected: '{expected_url}', Found: '{current_url}'"
    print("✅ URL is correct:", current_url)

except Exception as e:
    print("🚨 Error:", e)

# Close the browser
driver.quit()
