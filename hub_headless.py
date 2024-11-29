import csv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 設定 Chrome 無視窗模式
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # 啟用無視窗模式
options.add_argument("--disable-gpu")  # 避免某些環境下 GPU 相關的問題
options.add_argument("--window-size=1920,1080")  # 設定視窗大小以模擬完整的瀏覽器
options.add_argument("--no-sandbox")  # 避免沙箱問題
options.add_argument("--disable-dev-shm-usage")  # 避免資源不足問題

# 初始化瀏覽器
driver = webdriver.Chrome(options=options)
driver.get("https://nckuhub.com")  # 替換為你的目標網址

time.sleep(5)

# 設定 CSV 檔案儲存目錄
output_folder = "hub_article"
os.makedirs(output_folder, exist_ok=True)  # 如果資料夾不存在，則創建

# 定位滾動區塊
scrollable_block = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, ".courseList__sideList__itemBox"))
)

# 設定目標座標
target_x = 100  # 替換為你的 X 座標
target_y = 100  # 替換為你的 Y 座標

# 定義選擇器和儲存已點擊的物件
clickable_items_selector = ".list_course_item_mid"
clicked_items = set()  # 用於記錄已點擊的物件

while True:
    # 獲取目前滾動區塊內的所有可點擊物件
    clickable_items = driver.find_elements(By.CSS_SELECTOR, clickable_items_selector)

    # 遍歷抓取到的物件並點擊
    new_clickable_found = False  # 標記是否有新物件需要處理
    for item in clickable_items:
        if item not in clicked_items:  # 檢查是否已處理過
            try:
                # 獲取課程名稱
                classinfo = item.text.strip()
                print(f"處理課程：{classinfo}\n")
                item.click()
                clicked_items.add(item)  # 記錄已點擊的物件
            except Exception as e:
                print(f"無法點擊物件: {e}")
            
            time.sleep(5)  # 等待頁面載入

            # 抓取展開頁面的訊息
            rows = [["Info", classinfo]]  # 儲存要寫入 CSV 的資料，將 `classinfo` 放在第一行
            try:
                content_block = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "courseContentBody"))
                )
                try:
                    tags = content_block.find_elements(By.CSS_SELECTOR, ".score-btn")
                    for tag in tags:
                        rows.append(["Tag", tag.text.strip()])
                except:
                    print("無法獲取標籤")

                try:
                    comments = content_block.find_elements(By.CSS_SELECTOR, ".courseFeedback__single")
                    for comment in comments:
                        rows.append(["Comment", comment.text.strip()])
                except:
                    print("無法獲取評論")

                # 將資料寫入 CSV 檔案
                if rows:
                    # 提取 classinfo 的第一個空格前的內容作為檔案名稱
                    filename_title = classinfo.split(' ')[0]
                    filename = f"{filename_title}.csv"
                    # 確保檔名合法
                    filename = "".join([c for c in filename if c.isalnum() or c in " ._-"]).rstrip()
                    filepath = os.path.join(output_folder, filename)  # 拼接完整路徑
                    with open(filepath, mode='w', newline='', encoding='utf-8') as file:
                        writer = csv.writer(file)
                        writer.writerow(["Type", "Content"])  # 寫入表頭
                        writer.writerows(rows)  # 寫入內容
                    print(f"已儲存至檔案: {filepath}\n")
                else:
                    print(f"課程 {classinfo} 無資料可寫入。\n")
            except:
                print("無法獲取內容")

            try:
                # 使用 ActionChains 模擬點擊返回
                actions = ActionChains(driver)
                actions.move_by_offset(target_x, target_y).click().perform()

                # 重置滑鼠位置（可選，防止後續操作干擾）
                actions.move_by_offset(-target_x, -target_y).perform()
            except:
                print("無法返回頁面")

            try:
                # 重新定位滾動區塊
                scrollable_block = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".courseList__sideList__itemBox"))
                )
                new_clickable_found = True  # 標記有新物件被處理
            except Exception as e:
                print(f"無法點擊物件: {e}")

    # 如果已處理完當前可見物件，滾動以獲取更多內容
    if not new_clickable_found:
        last_scroll_position = driver.execute_script("return arguments[0].scrollTop;", scrollable_block)
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", scrollable_block)
        time.sleep(2)  # 等待新內容載入
        new_scroll_position = driver.execute_script("return arguments[0].scrollTop;", scrollable_block)

        # 如果滾動位置未改變，說明已到達底部，退出循環
        if new_scroll_position == last_scroll_position:
            print("已滾動至頁面底部，無更多內容。")
            break

# 關閉瀏覽器
driver.quit()
