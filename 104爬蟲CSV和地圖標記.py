import csv
import time
import folium
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim

# 啟動 Selenium 瀏覽器
driver = webdriver.Chrome()
base_url = "https://www.104.com.tw/jobs/search/?indcat=1001000000&isJobList=1&jobsource=joblist_search&page"
page_count = 1  # 起始頁數
tale_url= "&keyword=python&area=6001008000"
fina_url = f"{base_url}{page_count}{tale_url}"
driver.get(fina_url)

# 設定最多抓取的職缺數量
max_jobs = 40
collected_jobs = 0
max_pages = 3 # 限制翻頁次數


wait = WebDriverWait(driver, 10)

# 存放職缺資訊的列表
job_list = []

# 建立地圖
job_map = folium.Map(location=[23.6978, 120.9605], zoom_start=7)  # 台灣中心點
geolocator = Nominatim(user_agent="job_locator")

# **抓取資料並翻頁**  
while collected_jobs < max_jobs and page_count <= max_pages:
    time.sleep(3)  # 等待頁面載入
    
    # 解析 HTML
    soup = BeautifulSoup(driver.page_source, "lxml")
    job_blocks = soup.select("div.info")  # 找到所有職缺區塊

    for job in job_blocks[:20]:  # 每頁最多 20 筆
        title_element = job.select_one("a[data-gtm-joblist='職缺-職缺名稱']")
        title = title_element.get("title", "未提供職缺名稱").strip() if title_element else "未提供職缺名稱"
        link = title_element.get("href", "#") if title_element else "#"

        location_element = job.select_one("a[data-gtm-joblist^='職缺-地區-']")
        location = location_element.get_text(strip=True) if location_element else "未提供地區"

        salary_element = job.select_one("a[data-gtm-joblist^='職缺-薪資-']")
        salary = salary_element.get_text(strip=True) if salary_element else "未提供薪資"

        if "/job/" in link and title:  # 確保有標題和連結
            print(f"職缺名稱: {title}")
            print(f"職缺網址: {link}")
            print(f"地點: {location}")
            print(f"薪資: {salary}")
            print("-" * 50)

            job_list.append([title, link, location, salary])
            collected_jobs += 1
            print(f"🔍 已收集 {collected_jobs} 筆 / 目標 {max_jobs} 筆")

            # **轉換地點為經緯度**
            try:
                location_data = geolocator.geocode(location)
                if location_data:
                    lat, lon = location_data.latitude, location_data.longitude
                    folium.Marker(
                        [lat, lon],
                        popup=f"{title}<br>{location}<br>{salary}<br><a href='{link}' target='_blank'>職缺連結</a>",
                        tooltip=title,
                        icon=folium.Icon(color="blue", icon="briefcase"),
                    ).add_to(job_map)
                else:
                    print(f"⚠️ 找不到地點: {location}")
            except Exception as e:
                print(f"⚠️ 地理編碼錯誤: {e}")

        if collected_jobs >= max_jobs:
            break

    # 只在資料抓取完畢後進行翻頁
    if collected_jobs < max_jobs:
        page_count += 1
        

# 關閉瀏覽器
driver.quit()

# **儲存 CSV 檔案**
csv_filename = "job_list.csv"
df = pd.DataFrame(job_list, columns=["職缺名稱", "職缺網址", "地點", "薪資"])
df.to_csv(csv_filename, index=False, encoding="utf-8-sig")
print(f"✅ CSV 檔案已儲存為 {csv_filename}")

# **儲存地圖**
job_map.save("job_map.html")
print("✅ 地圖已儲存為 job_map.html")
