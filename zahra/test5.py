from selenium import webdriver
from selenium.webdriver.common.by import By
import time


driver = webdriver.Firefox()
driver.get("https://shop.polymer-project.org/")
time.sleep(3)

# بررسی مقدار description
try:
    meta_description = driver.find_element(By.CSS_SELECTOR, "meta[name='description']")
    content = meta_description.get_attribute("content")

    expected_content = "Polymer Shop Demo"
    if content == expected_content:
        print("✅ مقدار meta description صحیح است.")
    else:
        print(f"❌ خطا: مقدار meta description '{content}' است، درحالی که باید '{expected_content}' باشد.")

except:
    print("❌ خطا: meta description یافت نشد!")

driver.quit()
