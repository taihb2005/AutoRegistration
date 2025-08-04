from encodings.punycode import insertion_unsort
from tabnanny import check
import time
from threading import Event
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import requests

from tool.check_web import DELETE_BUTTON_ID

from .utils import *
from .config import *

def is_site_up(url, timeout=20):
    """Check if the website is accessible"""
    try:
        response = requests.get(url, timeout=timeout)
        return response.status_code == 200
    except requests.RequestException:
        return False

def search_and_save(driver, wait):
    # Check if site is accessible before proceeding
    if not is_site_up(URL_CLASSLIST):
        print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Website khong hoat dong")
        return False
        
    driver.get(URL_CLASSLIST)
    time.sleep(2)

    for kw in KEYWORDS:
        driver.get(URL_CLASSLIST)
        time.sleep(2)
        attempt = 0
        while attempt < 2:
            try:
                fill_input(wait, SUBJECT_INPUT_ID, kw, delay=3)
                break 
            except Exception as e:
                attempt += 1
                time.sleep(2) 

        malop = []

        while True:
            try:
                malop += process_rows(driver)

                next_button = driver.find_element(By.ID, NEXT_BUTTON)
                tag_name = next_button.tag_name
                class_name = next_button.get_attribute("class")

                if tag_name == "b" or "dxp-disabledButton" in class_name:
                    print("Trang cuoi cung!")
                    break

                next_button.click()
                WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tr.dxgvDataRow_Moderno"))
                )
                time.sleep(1)

            except NoSuchElementException:
                print("Khong tim thay nut Next, dung lai.")
                break

            except Exception as e:
                print(f"Loi khi xu ly nut Next: {e}")
                break

        if not malop:
            print(f" Khong tim thay lop nao cho hoc phan {kw} voi so luong sinh vien it hon 50.")
        else:
            for ma_lop in malop:

                register_class(driver, wait, ma_lop)

                time.sleep(0.5)

                class_state = find_registered_class(driver, subject_id=kw, state="Hết chỗ")

                if class_state is not None:
                    print(f"Lop het cho mat roi!")
                    delete_registered_class(driver, wait, class_state)
                    time.sleep(1)
                    continue
                else:
                    print(f"Dang ky thanh cong lop {ma_lop}!")
                    break
    
    
def register_class(driver, wait, class_id):
    try :
        driver.get(URL_REGISTER)

        time.sleep(1)

        fill_input(wait, REGISTER_INPUT_ID, class_id, delay=1)

        register_button = wait.until(EC.element_to_be_clickable((By.ID, REGISTER_BUTTON_ID)))
        register_button.click()

        wait.until(EC.invisibility_of_element_located((By.ID, LOADING_SCREEN_ID)))

        time.sleep(0.5)

        print(f" Da gui dang ky lop {class_id}.")
        
        try:
                send_register_button = wait.until(EC.element_to_be_clickable((By.ID, REGISTER_SEND_BUTTON_ID)))
                send_register_button.click()
                time.sleep(0.5)
                yes_button = wait.until(EC.element_to_be_clickable((By.ID, REGISTER_CONFIRM_BUTTON_ID)))
                yes_button.click()
        except Exception as e :
                print(f" Loi khi an nut dang ky lop  {class_id} ")
        
    except Exception as e:
        print(f" Loi khi dang ky lop {class_id}")
        return False
    
def fill_input(wait, element_id="", input_key="", delay=0):
    try:
        input_field = wait.until(EC.presence_of_element_located((By.ID, element_id)))
        input_field.clear()
        time.sleep(1)
        input_field.send_keys(input_key)
        if delay > 0:
            time.sleep(delay)
    except Exception:
        pass

def find_registered_class(driver, class_id="", class_name="", subject_id = "", class_type="", state=""):
    driver.get(URL_REGISTER)
    time.sleep(1)
    
    registered_table = driver.find_element(By.ID, CLASS_REGISTERED_TABLE)

    registered_classes = registered_table.find_elements(By.CSS_SELECTOR, "tr.dxgvDataRow_Moderno")

    for pos, registered_class in enumerate(registered_classes):
        cells = safe_find_elements(registered_class, By.TAG_NAME, "td")
        if len(cells) < 12:
            continue

        satisfied_conditions = True

        if(class_id != ""):
            _class_id = cells[0].text
            satisfied_conditions = satisfied_conditions and (_class_id == class_id)

        if(class_name != ""):
            _class_name = cells[2].text
            satisfied_conditions = satisfied_conditions and (_class_name == class_name)

        if(subject_id != ""):
            _subject_id = cells[3].text
            satisfied_conditions = satisfied_conditions and (_subject_id == subject_id)

        if(class_type != ""):
            _class_type = cells[4].text
            satisfied_conditions = satisfied_conditions and (_class_type == class_type)

        _state = cells[7].text
        satisfied_conditions = satisfied_conditions and (_state == state)

        if satisfied_conditions:
            print(f"Tim thay lop cua sep o vi tri {pos} het cho")
            return {
                "class": registered_class,
                "position": pos
            }

    return None

def delete_registered_class(driver, wait, source_class_info):
    if source_class_info is None:
        print(f"Co lop nao dau ma xoa")
        return False
    
    source_class = source_class_info.get("class")
    position = source_class_info.get("position")

    checkbox_td = source_class.find_element(By.CSS_SELECTOR, "td.dxgvCommandColumn_Moderno.dxgv.dx-ac")
    time.sleep(0.5)
    checkbox_td.click()

    delete_register_button = wait.until(EC.element_to_be_clickable((By.ID, REGISTER_DELETE_BUTTON_ID)))
    delete_register_button.click()
    time.sleep(0.5)

    try:
        send_register_button = wait.until(EC.element_to_be_clickable((By.ID, REGISTER_SEND_BUTTON_ID)))
        send_register_button.click()
        time.sleep(0.5)
        yes_button = wait.until(EC.element_to_be_clickable((By.ID, REGISTER_CONFIRM_BUTTON_ID)))
        yes_button.click()
    except Exception as e :
            print(f" Loi khi huy lop")
            return False

    return True

        
