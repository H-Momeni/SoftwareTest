import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Function to access Shadow DOM recursively
def get_shadow_element(driver, root_element, selector):
    shadow_root = driver.execute_script("return arguments[0].shadowRoot", root_element)
    return shadow_root.find_element(By.CSS_SELECTOR, selector)

@pytest.fixture
def setup():
    driver = webdriver.Firefox()
    driver.get("https://shop.polymer-project.org/")
    time.sleep(3)  # Allow time for the page to load
    yield driver
    driver.quit()

@allure.feature("Page Load")
@allure.story("Verify the main page loads successfully")
def test_page_load(setup):
    driver = setup
    with allure.step("Check if the 'shop-app' element exists"):
        element = driver.find_element(By.TAG_NAME, "shop-app")
        assert element is not None, "shop-app not found!"

@allure.feature("Page Title")
@allure.story("Check if the page title is correct")
def test_page_title(setup):
    driver = setup
    expected_title = "Home - SHOP"
    with allure.step("Get the page title"):
        actual_title = driver.title
    with allure.step("Verify the title matches the expected value"):
        assert actual_title == expected_title, f"Expected '{expected_title}', but got '{actual_title}'"

@allure.feature("Favicon")
@allure.story("Ensure the favicon is present")
def test_favicon(setup):
    driver = setup
    with allure.step("Check if the favicon link exists"):
        favicon = driver.find_element(By.CSS_SELECTOR, "link[rel='shortcut icon']")
        assert favicon is not None, "Favicon not found!"

@allure.feature("Manifest File")
@allure.story("Check if manifest.json is available")
def test_manifest(setup):
    driver = setup
    with allure.step("Check if manifest.json is linked"):
        manifest = driver.find_element(By.CSS_SELECTOR, "link[rel='manifest']")
        assert manifest is not None, "Manifest.json not found!"

@allure.feature("Meta Tags")
@allure.story("Verify the meta description is correct")
def test_meta_description(setup):
    driver = setup
    expected_description = "Polymer Shop Demo"
    with allure.step("Find the meta description tag"):
        meta_description = driver.find_element(By.CSS_SELECTOR, "meta[name='description']")
        content = meta_description.get_attribute("content")
    with allure.step("Verify the description content"):
        assert content == expected_description, f"Expected '{expected_description}', but got '{content}'"

@allure.feature("Theme Color")
@allure.story("Verify the theme color meta tag")
def test_theme_color(setup):
    driver = setup
    expected_color = "#fff"
    with allure.step("Find the theme color meta tag"):
        meta_theme = driver.find_element(By.CSS_SELECTOR, "meta[name='theme-color']")
        color = meta_theme.get_attribute("content")
    with allure.step("Verify the theme color"):
        assert color == expected_color, f"Expected '{expected_color}', but got '{color}'"

@allure.feature("Shop Button Navigation")
@allure.story("Verify the 'Shop Now' button for Men's Outerwear")
def test_shop_now_outerwear(setup):
    driver = setup
    with allure.step("Locate the main 'shop-app' element"):
        shop_app = driver.find_element(By.CSS_SELECTOR, "shop-app")

    with allure.step("Access shadow root of 'shop-app' and find 'iron-pages'"):
        iron_pages = get_shadow_element(driver, shop_app, "iron-pages")

    with allure.step("Find 'shop-home' inside 'iron-pages'"):
        shop_home = iron_pages.find_element(By.CSS_SELECTOR, "shop-home.iron-selected")

    with allure.step("Locate the 'Shop Now' button inside 'shop-home'"):
        button = get_shadow_element(driver, shop_home, "div.item shop-button a")
    
    with allure.step("Verify the button text"):
        assert button.text.strip() == "SHOP NOW", f"Button text mismatch! Expected: 'SHOP NOW', Found: '{button.text.strip()}'"
    
    with allure.step("Click the button"):
        button.click()
    
    time.sleep(5)  # Wait for navigation
    expected_url = "https://shop.polymer-project.org/list/mens_outerwear"
    with allure.step("Verify the redirected URL"):
        assert driver.current_url == expected_url, f"URL mismatch! Expected: '{expected_url}', Found: '{driver.current_url}'"

@allure.feature("Shop Button Navigation")
@allure.story("Verify the 'Shop Now' button for Men's T-Shirts")
def test_shop_now_tshirts(setup):
    driver = setup
    with allure.step("Locate the main 'shop-app' element"):
        shop_app = driver.find_element(By.CSS_SELECTOR, "shop-app")

    with allure.step("Access shadow root of 'shop-app' and find 'iron-pages'"):
        iron_pages = get_shadow_element(driver, shop_app, "iron-pages")

    with allure.step("Find 'shop-home' inside 'iron-pages'"):
        shop_home = iron_pages.find_element(By.CSS_SELECTOR, "shop-home.iron-selected")

    with allure.step("Access shadow root of 'shop-home'"):
        shop_home_shadow = driver.execute_script("return arguments[0].shadowRoot", shop_home)

    with allure.step("Locate the 'Shop Now' button for Men's T-Shirts"):
        button = shop_home_shadow.find_element(By.CSS_SELECTOR, "a[aria-label=\"Men's T-Shirts Shop Now\"]")

    with allure.step("Verify the button text"):
        assert button.text.strip() == "SHOP NOW", f"Button text mismatch! Expected: 'Shop Now', Found: '{button.text.strip()}'"

    with allure.step("Click the button"):
        button.click()

    time.sleep(5)  # Wait for navigation
    expected_url = "https://shop.polymer-project.org/list/mens_tshirts"
    with allure.step("Verify the redirected URL"):
        assert driver.current_url == expected_url, f"URL mismatch! Expected: '{expected_url}', Found: '{driver.current_url}'"
