from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Firefox()
driver.get("https://shop.polymer-project.org/")

try:
    # صبر کن تا دکمه منو قابل کلیک باشد
    menu_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "shop-icon-button[icon='menu']"))
    )
    menu_button.click()

    # صبر کن تا آیتم‌های منو لود شوند
    menu_items = WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "shop-menu-item"))
    )

    if len(menu_items) > 0:
        print(f"✅ Navigation menu opened! Found {len(menu_items)} items.")
    else:
        print("❌ Navigation menu did not open.")

except Exception as e:
    print(f"❌ Test failed: {e}")

driver.quit()
