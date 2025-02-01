from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# تنظیم WebDriver برای فایرفاکس
driver = webdriver.Firefox()

# باز کردن سایت موردنظر
driver.get("https://shop.polymer-project.org/")
time.sleep(3)  # ۳ ثانیه صبر کن تا صفحه لود شود

# بررسی اینکه سایت باز شده است
title = driver.title
print(f"صفحه باز شده: {title}")

# بستن مرورگر
driver.quit()
