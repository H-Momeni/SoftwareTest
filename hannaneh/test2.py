from selenium import webdriver
import time

driver = webdriver.Firefox()
driver.get("https://shop.polymer-project.org/")
time.sleep(3)

# دریافت عنوان واقعی صفحه
actual_title = driver.title
print(f"🔍 عنوان صفحه دریافت شده: '{actual_title}'")

expected_title = "Home - SHOP"  # مقدار صحیح را اینجا قرار بده

if actual_title == expected_title:
    print("✅ عنوان صفحه صحیح است.")
else:
    print(f"❌ خطا: عنوان صفحه '{actual_title}' است، درحالی که باید '{expected_title}' باشد.")

driver.quit()
