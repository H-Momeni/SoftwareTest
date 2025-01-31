from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Firefox()

# باز کردن صفحه
driver.get("https://shop.polymer-project.org/")
time.sleep(3)

# بررسی اینکه صفحه اصلی لود شده است
try:
    element = driver.find_element(By.TAG_NAME, "shop-app")
    print("✅ صفحه با موفقیت بارگذاری شد.")
except:
    print("❌ خطا: shop-app پیدا نشد!")

driver.quit()
