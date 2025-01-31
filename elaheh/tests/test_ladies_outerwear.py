import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def setup():
    driver = webdriver.Firefox()  # یا فایرفاکس یا مرورگر دیگر
    driver.get("https://shop.polymer-project.org/list/ladies_outerwear")  # مسیر فایل HTML شما
    yield driver
    driver.quit()

@allure.feature("Page Title")
@allure.story("Check if the page title is correct")
def test_page_title(setup):
    driver = setup
    with allure.step("Verify the page title"):
        assert driver.title == "Ladies Outerwear - SHOP", f"Expected title to be 'Ladies Outerwear - SHOP', but got {driver.title}"

@allure.feature("Meta Tags")
@allure.story("Check if the meta description is present")
def test_meta_description(setup):
    driver = setup
    with allure.step("Find meta description tag"):
        meta_description = driver.find_element(By.CSS_SELECTOR, "meta[name='description']")
        assert meta_description, "Meta description tag is missing!"
        assert meta_description.get_attribute("content") == "Polymer Shop Demo", "Meta description content is incorrect!"

@allure.feature("Favicon")
@allure.story("Check if the favicon is present")
def test_favicon_exists(setup):
    driver = setup
    with allure.step("Check for favicon link"):
        favicon = driver.find_element(By.CSS_SELECTOR, "link[rel='shortcut icon']")
        assert favicon, "Favicon link is missing!"
        assert favicon.get_attribute("href").endswith("images/shop-icon-32.png"), "Favicon path is incorrect!"



@allure.feature("Shop App Element")
@allure.story("Verify shop-app element is present and visible")
def test_shop_app_presence(setup):
    driver = setup
    with allure.step("Check if shop-app element is present and visible"):
        # Wait for the shop-app element to be present and visible
        shop_app = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "shop-app"))
        )
        assert shop_app.is_displayed(), "shop-app element is not visible!"
        
@allure.feature("JavaScript Files")
@allure.story("Check if the main JavaScript file is loaded")
def test_main_js_file(setup):
    driver = setup
    with allure.step("Verify the main JavaScript file"):
        script_tags = driver.find_elements(By.TAG_NAME, "script")
        main_js = any("src/shop-app.js" in script.get_attribute("src") for script in script_tags)
        assert main_js, "Main JavaScript file (shop-app.js) is missing!"

@allure.feature("Performance Metrics")
@allure.story("Check if performance mark is executed")
def test_performance_mark(setup):
    driver = setup
    with allure.step("Execute JavaScript to check performance mark"):
        result = driver.execute_script("return !!window.performance.mark")
        assert result, "Performance mark is not executed!"
