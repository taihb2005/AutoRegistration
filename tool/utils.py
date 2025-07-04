import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException

def safe_find_elements(element, by, value, retries=3):
    for _ in range(retries):
        try:
            return element.find_elements(by, value)
        except StaleElementReferenceException:
            time.sleep(1)
    return []

def process_rows(driver):
    rows = driver.find_elements(By.CSS_SELECTOR, "tr.dxgvDataRow_Moderno")
    malop = []

    for row in rows:
        cells = safe_find_elements(row, By.TAG_NAME, "td")
        if len(cells) < 8:
            continue

        ma_lop = cells[0].text
        try:
            so_sv = int(cells[7].text)
            max_sv = int(cells[6].text)
        except ValueError:
            continue

        print(f" Lớp {ma_lop} | Số SV: {so_sv}/{max_sv}")

        if  so_sv< max_sv and max_sv < 150:
            print(f" Slot còn trống ({so_sv}/{max_sv}) trong lớp {ma_lop}")
            malop.append(ma_lop)

    return malop
