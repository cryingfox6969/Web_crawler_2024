import time
import random
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 可選的 Chrome 選項
#options = uc.ChromeOptions()
#options.add_argument('--no-sandbox')
#options.add_argument('--disable-dev-shm-usage')
#options.add_argument('--start-maximized')

# 啟動 undetected-chromedriver
driver = uc.Chrome()
#driver = uc.Chrome(options=options)

#initial
#url="https://www.dcard.tw/f/travel/p/257187749"
url="https://www.dcard.tw/f/travel/p/257188806"
driver.get(url)
username = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME,"query"))
)  #wait for web be prepared

#get_text_info
try:
    title = driver.find_element(By.CLASS_NAME,"d_xm_2v")
    author = driver.find_element(By.CLASS_NAME, "avvspio")
    article = driver.find_element(By.CLASS_NAME,"c1ehvwc9")
    tags = driver.find_elements(By.CLASS_NAME,"c18kb6hg")
    print(title.text)
    print(author.text)
    print(article.text)
    count=0
    for tag in tags:
        print(tag.text)
        count+=1
    print(count)
#terminate
finally:
    time.sleep(3)
    driver.quit
#class="d_d8_1hcvtr6 d_cn_2h d_gk_10yn01e d_7v_gdpa86 d_1938jqx_2k d_2zt8x3_1y d_grwvqw_gknzbh d_1ymp90q_1s d_89ifzh_1s d_1hh4tvs_1r d_1054lsl_1r t1gihpsa"
#class="d_xm_2v d_7v_5 d_hh_29 d_jm_1r d_d8_2s d_cn_31 d_gk_2n d_f6vyfi_2s d_178gzt7_23 d_8viy46_14e6m10 t17vlqzd">
#class="d_xa_2b d_tx_2c d_lc_1u d_7v_5 avvspio">