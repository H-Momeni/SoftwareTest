from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.get("https://shop.polymer-project.org/detail/mens_tshirts/Inbox+-+Subtle+Actions+T-Shirt")
time.sleep(3) 

title = driver.title
print(f"title: {title}")

driver.quit()