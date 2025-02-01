import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time

# Fixture برای مدیریت WebDriver
@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

# تابع کمکی برای دسترسی به Shadow DOM
def get_shadow_element(driver, root_element, selector):
    shadow_root = driver.execute_script("return arguments[0].shadowRoot", root_element)
    return shadow_root.find_element(By.CSS_SELECTOR, selector)

# تست‌ها

@allure.feature("Product Page Tests")
@allure.story("Get page title")
def test_get_page_title(driver):
    driver.get("https://shop.polymer-project.org/detail/mens_tshirts/Inbox+-+Subtle+Actions+T-Shirt")
    time.sleep(3)  # Allow time for the page to load
    title = driver.title
    allure.attach(title, "Page Title", allure.attachment_type.TEXT)
    print(f"title: {title}")
    assert title != "", "Page title should not be empty"

@allure.feature("Product Page Tests")
@allure.story("Select product size")
def test_select_size(driver):
    driver.get("https://shop.polymer-project.org/detail/mens_tshirts/Inbox+-+Subtle+Actions+T-Shirt")
    time.sleep(2)  # Allow time for the page to load

    try:
        shop_app = driver.find_element(By.CSS_SELECTOR, "shop-app")
        iron_pages = get_shadow_element(driver, shop_app, "iron-pages")
        shop_detail = iron_pages.find_element(By.CSS_SELECTOR, "shop-detail")
        pickers = get_shadow_element(driver, shop_detail, "div.pickers")
        size_select = pickers.find_element(By.CSS_SELECTOR, "shop-select select#sizeSelect")

        select = Select(size_select)
        select.select_by_value("L")  # Change this to the desired size
        print("Successfully selected size: L")
        allure.attach("L", "Selected Size", allure.attachment_type.TEXT)

    except Exception as e:
        print("Error:", e)
        allure.attach(str(e), "Error Message", allure.attachment_type.TEXT)
        pytest.fail(f"Test failed due to: {e}")

@allure.feature("Product Page Tests")
@allure.story("Select product quantity")
def test_select_quantity(driver):
    driver.get("https://shop.polymer-project.org/detail/mens_tshirts/Inbox+-+Subtle+Actions+T-Shirt")
    time.sleep(2)  # Allow time for the page to load

    try:
        shop_app = driver.find_element(By.CSS_SELECTOR, "shop-app")
        iron_pages = get_shadow_element(driver, shop_app, "iron-pages")
        shop_detail = iron_pages.find_element(By.CSS_SELECTOR, "shop-detail")
        pickers = get_shadow_element(driver, shop_detail, "div.pickers")
        quantity_select = pickers.find_element(By.CSS_SELECTOR, "shop-select select#quantitySelect")

        select = Select(quantity_select)
        select.select_by_value("3")  # Change this to the desired quantity
        print("Successfully selected quantity to 3")
        allure.attach("3", "Selected Quantity", allure.attachment_type.TEXT)

    except Exception as e:
        print("Error:", e)
        allure.attach(str(e), "Error Message", allure.attachment_type.TEXT)
        pytest.fail(f"Test failed due to: {e}")

@allure.feature("Product Page Tests")
@allure.story("Select quantity to 10")
def test_select_quantity_10(driver):
    driver.get("https://shop.polymer-project.org/detail/mens_tshirts/Inbox+-+Subtle+Actions+T-Shirt")
    time.sleep(2)  # Allow time for the page to load

    try:
        shop_app = driver.find_element(By.CSS_SELECTOR, "shop-app")
        iron_pages = get_shadow_element(driver, shop_app, "iron-pages")
        shop_detail = iron_pages.find_element(By.CSS_SELECTOR, "shop-detail")
        pickers = get_shadow_element(driver, shop_detail, "div.pickers")
        quantity_select = pickers.find_element(By.CSS_SELECTOR, "shop-select select#quantitySelect")

        select = Select(quantity_select)

        # Try selecting a value of "10", and catch errors if the value is invalid
        try:
            select.select_by_value("10")  
            print("Successfully selected quantity to 10")
            allure.attach("10", "Selected Quantity", allure.attachment_type.TEXT)
        except Exception as e:
            print("Error: Invalid quantity value. Valid values are between 1 and 5.")
            allure.attach(str(e), "Error Message", allure.attachment_type.TEXT)
            pytest.fail(f"Test failed due to: {e}")

    except Exception as e:
        print("Error:", e)
        allure.attach(str(e), "Error Message", allure.attachment_type.TEXT)
        pytest.fail(f"Test failed due to: {e}")

@allure.feature("Product Page Tests")
@allure.story("Get product price")
def test_get_product_price(driver):
    driver.get("https://shop.polymer-project.org/detail/mens_tshirts/Inbox+-+Subtle+Actions+T-Shirt")
    time.sleep(2)  # Allow time for the page to load

    try:
        shop_app = driver.find_element(By.CSS_SELECTOR, "shop-app")
        iron_pages = get_shadow_element(driver, shop_app, "iron-pages")
        shop_detail = iron_pages.find_element(By.CSS_SELECTOR, "shop-detail")
        price = get_shadow_element(driver, shop_detail, "div.price")

        price_text = price.text
        print("Product Price:", price_text)
        allure.attach(price_text, "Product Price", allure.attachment_type.TEXT)

    except Exception as e:
        print("Error:", e)
        allure.attach(str(e), "Error Message", allure.attachment_type.TEXT)
        pytest.fail(f"Test failed due to: {e}")

@allure.feature("Product Page Tests")
@allure.story("Scroll page")
def test_scroll_page(driver):
    driver.get("https://shop.polymer-project.org/detail/mens_tshirts/Inbox+-+Subtle+Actions+T-Shirt")
    time.sleep(2)  # Allow time for the page to load

    # Scroll down to the bottom
    driver.execute_script("window.scrollBy(0, 500);")
    print("Scrolled to bottom of the page")
    allure.attach("Scrolled 500px", "Scroll Action", allure.attachment_type.TEXT)

    time.sleep(2)  # Give time to load more content if needed
