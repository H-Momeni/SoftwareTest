from selenium import webdriver
from selenium.webdriver.common.by import By
import time


driver = webdriver.Firefox()
driver.get("https://shop.polymer-project.org/")
time.sleep(3)

# بررسی مقدار theme-color
try:
    meta_theme = driver.find_element(By.CSS_SELECTOR, "meta[name='theme-color']")
    color = meta_theme.get_attribute("content")

    expected_color = "#fff"
    if color == expected_color:
        print("✅ مقدار theme-color صحیح است.")
    else:
        print(f"❌ خطا: مقدار theme-color '{color}' است، درحالی که باید '{expected_color}' باشد.")

except:
    print("❌ خطا: meta theme-color یافت نشد!")

driver.quit()
