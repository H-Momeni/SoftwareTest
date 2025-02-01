from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://shop.polymer-project.org/detail/mens_tshirts/Inbox+-+Subtle+Actions+T-Shirt")

shop_app = driver.find_element(By.CSS_SELECTOR, "shop-app")

page_value = shop_app.get_attribute("page")
print("Page attribute value:", page_value)

driver.quit()
