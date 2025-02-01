from selenium import webdriver
from selenium.webdriver.common.by import By
import time


driver = webdriver.Firefox()
driver.get("https://shop.polymer-project.org/")
time.sleep(3)

# پیدا کردن favicon در صفحه
try:
    favicon = driver.find_element(By.CSS_SELECTOR, "link[rel='shortcut icon']")
    print("✅ favicon به درستی تنظیم شده است.")
except:
    print("❌ خطا: favicon یافت نشد!")

driver.quit()
