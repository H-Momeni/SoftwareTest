from selenium import webdriver
from selenium.webdriver.common.by import By
import time


driver = webdriver.Firefox()
driver.get("https://shop.polymer-project.org/")
time.sleep(3)

# بررسی وجود لینک فایل manifest.json
try:
    manifest = driver.find_element(By.CSS_SELECTOR, "link[rel='manifest']")
    print("✅ فایل manifest.json در صفحه وجود دارد.")
except:
    print("❌ خطا: فایل manifest.json یافت نشد!")

driver.quit()
