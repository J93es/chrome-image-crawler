from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import csv
import numpy as np


# 구글 검색창에서 targetName을 검색해주는 함수
def searchTarget(driver, targetName):
    elem = driver.find_element("name", "q")
    elem.send_keys(targetName)
    elem.send_keys(Keys.RETURN)

# 창을 아래로 스크롤 해주는 함수
def scrollDown(driver):
    SCROLL_PAUSE_TIME = 10
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

# 이미지의 url을 수집하는 함수
def getImgsUrl(driver, maxLen, imgsUrl):
    images = driver.find_elements(By.CSS_SELECTOR, ".rg_i.Q4LuWd")

    """ Xpath """
    imgXpath = '/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div[3]/div[1]/a/img[1]'
    count = 1
    IMG_LOAD_TIME = 0.5

    for image in images:
        try:
            tmp = None
            image.click()
            time.sleep(IMG_LOAD_TIME)

            # 먼저 큰 이미지를 수집하는 것을 시도하고 실패했다면, 작은 이미지를 수집함
            try:
                tmp = driver.find_element(By.XPATH, imgXpath).get_attribute("src")
            except:
                tmp = None
            if tmp == None:
                try:
                    tmp = driver.find_element(By.XPATH, imgXpath).get_attribute("data-src")
                except:
                    tmp = None
            if tmp == None:
                try:
                    tmp = image.get_attribute("src")
                except:
                    tmp = None
            if tmp == None:
                try:
                    tmp = image.get_attribute("data-src")
                except:
                    tmp = None

            if tmp != None:
                imgsUrl.append(tmp)
                print(count)
                count += 1
            else:
                print("missing img url : ", count)

            if count > maxLen:
                break
        
        except Exception as e:
            print(f'error {count}th :', e)
            pass
    
    return imgsUrl

# csv를 열고 해당 값들을 불러오는 함수
def openCsv(path, fileName):
    imgsUrl = []
    try:
        f = open(f"{path}{fileName}.csv", 'r')
        csvReader = csv.reader(f)
        for l in csvReader:
            if l:
                imgsUrl.append(l[0])
    except Exception as e:
        print('error :', e)
        try:
            f = open(f"{fileName}.csv", 'r')
            csvReader = csv.reader(f)
            for l in csvReader:
                if l:
                    imgsUrl.append(l[0])
            print(f"notice : because of error, ./{fileName}.csv is opened")
        except Exception as e:
            print('error :', e)

    return imgsUrl

# csv에 값들을 덮어쓰는 함수
def writeCsvRows(targetData, path, fileName):
    try:
        f = open(f"{path}{fileName}.csv", 'w')
        write = csv.writer(f)
        write.writerows(targetData)
    except Exception as e:
        print('error :', e)
        f = open(f"./{fileName}.csv", 'w')
        write = csv.writer(f)
        write.writerows(targetData)
        print(f"notice : because of error, CSV file saved ./{fileName}.csv")


""" custom this place """
targetName = "눈없는 산"
fileName = "겨울"
maxLen = 2

""" path setting """
path = f"./img_urls/{fileName}/"

# 기존에 저장되었던 csv 파일을 열고 백업본을 만듦
imgsUrl = openCsv(path, fileName)
writeCsvRows(np.array(imgsUrl).reshape(len(imgsUrl), 1), path, f"{fileName}_bak")

# 브라우저 준비
baseUrl = "http://www.google.co.kr/imghp?hl=ko"
chromeOptions = webdriver.ChromeOptions()
""" browser header setting """
header = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36'
chromeOptions.add_argument(header)
chromeOptions.add_argument("lang=ko_KR")
chromeOptions.add_argument("window-size=1920x1080")
driver = webdriver.Chrome(chromeOptions)
driver.get(baseUrl)

# 브라우저를 통하여 url 수집
searchTarget(driver, targetName)                # 구글 검색창에서 targetName을 검색해주는 함수
scrollDown(driver)                              # 창을 아래로 스크롤 해주는 함수
imgsUrl = getImgsUrl(driver, maxLen, imgsUrl)   # 이미지의 url을 수집하는 함수
driver.close()

# 수집한 url을 csv파일에 저장
imgsUrl = np.unique(imgsUrl)
writeCsvRows(imgsUrl.reshape(len(imgsUrl), 1), path, fileName)
