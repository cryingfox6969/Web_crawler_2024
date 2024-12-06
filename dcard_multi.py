import time
import random
import os
import undetected_chromedriver as uc
import csv
import re
from datetime import datetime, timedelta
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# 定義檔案夾名稱
output_folder = "dcard_articles"

# 檢查並創建檔案夾
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 定義爬取函數
def scrape_url(url):
    # 提取文章編號
    match = re.search(r'/p/(\d+)', url)
    article_id = match.group(1) if match else "unknown"

    # 啟動 undetected-chromedriver
    driver = uc.Chrome()
    driver.get(url)

    # 用來儲存爬取的資訊
    data = {
        "title": "",
        "author": "",
        "time": "",
        "article": "",
        "pictures": [],
        "tags": [],
        "url": url  # 新增文章連結欄位
    }

    # 等待頁面加載完成
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".d_d8_2s time"))
    )

    # 取得文章標題
    try:
        title = driver.find_element(By.CLASS_NAME, "d_xm_2v")
        data["title"] = title.text
    except:
        print("Failed to get title")

    # 取得作者
    try:
        author = driver.find_element(By.CLASS_NAME, "avvspio")
        data["author"] = author.text
    except:
        print("Failed to get author")

    # 取得發文時間
    try:
        article_time = driver.find_element(By.CSS_SELECTOR, ".d_d8_2s time")
        data["time"] = article_time.text
    except:
        print("Failed to get article time")

    # 取得文章內容
    try:
        article = driver.find_element(By.CLASS_NAME, "c1ehvwc9")
        data["article"] = "\n" + article.text
    except:
        print("Failed to get article content")

    # 取得文章圖片
    try:
        art_pics = driver.find_elements(By.CSS_SELECTOR, '.c1golu5u img[decoding*="async"]')
        data["pictures"] = [art_pic.get_attribute("src") for art_pic in art_pics]
    except:
        print("Failed to get art_pic url")

    # 取得標籤
    try:
        tags = driver.find_elements(By.CSS_SELECTOR, ".wdl7s0r .c18kb6hg")
        data["tags"] = [tag.text for tag in tags]
    except:
        print("Failed to get tags")

    # 設定儲存留言的集合以避免重複
    comments = set()
    comment_data = []  # 用來儲存留言的資料

    # 滾動設定
    scroll_step = 200  # 每次滾動的像素數
    scroll_pause_time = 0.5  # 每次滾動後的暫停時間
    current_position = 0

    # 開始滾動並提取留言
    try:
        while True:
            # 展開留言
            try:
                extend_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), '查看其他')]")
                for extend_button in extend_buttons:
                    driver.execute_script("arguments[0].click();", extend_button)
            except:
                pass

            # 找出所有留言元素
            comment_elements = driver.find_elements(By.CSS_SELECTOR, "[data-key^='comment-']")
            
            # 提取並儲存新留言
            for comment_element in comment_elements:
                try:
                    # 提取留言內容
                    main_text_element = comment_element.find_element(By.CSS_SELECTOR, ".d_xa_34.d_xj_2v.c1ehvwc9")
                    comment_text = main_text_element.text
                    if comment_text not in comments:
                        comments.add(comment_text)  # 避免重複加入相同留言
                        
                        # 提取留言編號和時間
                        try:
                            picture_elements = comment_element.find_elements(By.CSS_SELECTOR, '.d_7v_5.d_cn_1t img[decoding*="async"]')
                            comment_picture = [picture_element.get_attribute("src") for picture_element in picture_elements]

                            comment_id_element = comment_element.find_element(By.CSS_SELECTOR, ".d_1938jqx_42phs0.dl7cym2")
                            comment_id = comment_id_element.text
                            
                            time_element = comment_element.find_element(By.CSS_SELECTOR, ".d_a5_1p.d_h7_9dpyb6 a span time")
                            comment_time_utc = time_element.get_attribute("datetime")
                            
                            # 將 UTC 時間轉換為本地時間（假設為 UTC+8）
                            utc_time = datetime.strptime(comment_time_utc, "%Y-%m-%dT%H:%M:%S.%fZ")
                            local_time = utc_time + timedelta(hours=8)
                            formatted_time = local_time.strftime("%m 月 %d 日 %H:%M")
                        except:
                            comment_id = "無法找到留言編號"
                            formatted_time = "無法找到留言時間"
                        
                        # 將留言資料存入 comment_data 列表
                        comment_data.append([comment_text, comment_picture, comment_id, formatted_time])
                        
                except:
                    continue  # 若任何元素不存在，則跳過該留言
                
            # 滾動頁面
            current_position += scroll_step
            driver.execute_script(f"window.scrollTo(0, {current_position});")
            time.sleep(scroll_pause_time)
            
            # 檢查是否已到達頁面底部
            new_height = driver.execute_script("return document.body.scrollHeight")
            if current_position >= new_height:
                print("已滾動到頁面底部，停止滾動。")
                break

    finally:
        driver.quit()

    # 清理標題，移除無法作為檔名的特殊字元
    cleaned_title = re.sub(r'[\\/*?:"<>|]', "", data["title"])
    
    # 將文章編號加入檔案標題
    if cleaned_title:
        cleaned_title = f"{article_id}_{cleaned_title}"
    else:
        cleaned_title = f"default_title_{article_id}"

    # 使用清理後的標題生成完整檔案路徑
    csv_file = os.path.join(output_folder, f"{cleaned_title}.csv")
    with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        
        # 寫入文章資訊，新增 URL 欄位
        writer.writerow(["Title", "Author", "Time", "Article", "Pictures", "Tags", "URL"])
        writer.writerow([data["title"], data["author"], data["time"], data["article"], "\n".join(data["pictures"]), "; ".join(data["tags"]), data["url"]])
        
        # 寫入留言資訊標題
        writer.writerow([])
        writer.writerow(["Comment Text", "Comment Picture", "Comment ID", "Comment Time"])
        
        # 寫入所有留言的資料
        for comment in comment_data:
            writer.writerow(comment)

    print(f"資料已成功寫入 {csv_file}")


# 讀取連結檔案
try:
    with open("links.txt", "r", encoding="utf-8") as file:
        urls = [line.strip() for line in file.readlines() if line.strip()]
except FileNotFoundError:
    print("Error: 找不到 links.txt 文件，請確認文件是否存在於正確目錄！")
    exit()
except Exception as e:
    print(f"Error: 無法讀取 links.txt 文件，錯誤原因：{e}")
    exit()

# 對每個連結執行爬取
if not urls:
    print("Error: links.txt 是空的，請填入有效連結！")
else:
    for url in urls:
        scrape_url(url)
