import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#initialize_headless
#chrome_options = Options()
#chrome_options.add_argument('--headless')  # 啟用 headless 模式
#driver = webdriver.Chrome(options=chrome_options)

#initialize
driver = webdriver.Chrome( )

#get_title
url="https://nckuhub.com"
driver.get(url)

username = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME,"list_course_item_title"))
)

for i in range(5):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)

class_names = driver.find_elements(By.CLASS_NAME,"list_course_item_title")
count=0
for class_name in class_names:
    print(class_name.text)
    count+=1
print(count)
time.sleep(5)
driver.quit