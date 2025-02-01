from selenium import webdriver
import time

driver = webdriver.Chrome()
driver.get("https://shop.polymer-project.org/detail/mens_tshirts/Inbox+-+Subtle+Actions+T-Shirt")

# Scroll down to the bottom
driver.execute_script("window.scrollBy(0, 500);")
print("Scrolled to bottom of the page")

time.sleep(2)  # Give time to load more content if needed

driver.quit()
