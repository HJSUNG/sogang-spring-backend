import os

# os.system('pip install --upgrade selenium')
# os.system('pip install webdriver-manager')
# os.system('pip install webdriver-manager')

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

def crawl_weather_info():
    # headless option
    ops = webdriver.ChromeOptions()

    ops.add_argument('headless')
    ops.add_argument('window-size=1920x1080')

    with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=ops) as driver:
        wait = WebDriverWait(driver, 15)
        url = "https://search.naver.com/search.naver?query=서울날씨"
        driver.get(url)

        try:

            select_tag = "div.weather_info > div > div._today > div.weather_graphic > div.temperature_text > strong"
            ele1 = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, select_tag))
            )

            # 현재온도
            cur_temp = ele1.text
            cur_temp = cur_temp.split("\n")
            cur_temp = cur_temp[1]
            print(cur_temp)

            select_tag = "div > div.weather_info > div > div._today > div.temperature_info > p"
            ele2 = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, select_tag))
            )
            # 날씨상태
            weather_status = ele2.text
            weather_status = weather_status.split("\n")
            print(weather_status[0] + weather_status[1] + "/" + weather_status[2])

            select_tag = "div.weather_info > div > div.report_card_wrap > ul > li:nth-child(1) > a > span"
            ele3 = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, select_tag))
            )
            # 미세먼지
            dust = ele3.text
            print(dust)

            select_tag = "div.weather_info > div > div.report_card_wrap > ul > li:nth-child(2) > a > span"
            ele4 = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, select_tag))
            )
            # 초미세먼지
            ultra_dust = ele4.text
            print(ultra_dust)
        except Exception as e:
            print("Error")

    return {'weather': weather_status, 'temp': cur_temp, "dust": dust, "ultra_dust": ultra_dust}



