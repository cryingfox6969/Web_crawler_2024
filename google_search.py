import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
#from selenium.webdriver.chrome.options import Options

url="https://www.google.com"

#chrome_options = Options()
#chrome_options.add_argument('--headless')  # 啟用 headless 模式

#driver = webdriver.Chrome(options=chrome_options)
driver = webdriver.Chrome( )
driver.get(url)
time.sleep(3)
elem = driver.find_element(By.NAME, "q")
elem.send_keys("台南晚餐")
time.sleep(2)
#elem.clear()
elem.send_keys(Keys.RETURN)
time.sleep(5)
#前往上一項瀏覽紀錄
#driver.back()
#前往下一項瀏覽紀錄
# #driver.forward()
search_result = driver.find_element(By.ID, "search").text
print("搜索結果：", search_result)
driver.quit()