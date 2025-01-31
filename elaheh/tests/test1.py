# این تست جز تستهای سایت نیست و صرفا برای بررسی کاکردنه 

from selenium import webdriver

# راه‌اندازی WebDriver برای Firefox
driver = webdriver.Firefox()

# باز کردن یک سایت
driver.get("https://www.google.com")

# نمایش عنوان صفحه
print("Page title is:", driver.title)

# بستن مرورگر
driver.quit()


