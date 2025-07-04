from tabnanny import check
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException


# =========================
# CONFIG
# =========================

options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36")

driver = webdriver.Chrome(options=options)

URL_LOGIN = "https://dk-sis.hust.edu.vn/Users/Login.aspx"
URL_REGISTER = "https://dk-sis.hust.edu.vn/Default.aspx"
# USERNAME = " "
# PASSWORD = " "

SUBJECT_INPUT_ID = "ctl00_ctl00_ASPxSplitter1_Content_ContentSplitter_MainContent_gvClassList_DXFREditorcol1_I"
REGISTER_INPUT_ID = "ctl00_ctl00_ASPxSplitter1_Content_ContentSplitter_MainContent_ASPxCallbackPanel1_tbDirectClassRegister_I"
REGISTER_BUTTON_ID = "ctl00_ctl00_ASPxSplitter1_Content_ContentSplitter_MainContent_ASPxCallbackPanel1_btDirectClassRegister"
REGISTER_SEND_BUTTON_ID = "ctl00_ctl00_ASPxSplitter1_Content_ContentSplitter_MainContent_ASPxCallbackPanel1_btSendRegister"
DELETE_BUTTON_ID = "ctl00_ctl00_ASPxSplitter1_Content_ContentSplitter_MainContent_ASPxCallbackPanel1_btDeleteClass"
REGISTER_CONFIRM_BUTTON_ID = "ctl00_ctl00_ASPxSplitter1_Content_ContentSplitter_MainContent_ASPxCallbackPanel1_pcYesNo_pcYesNoBody1_ASPxRoundPanel1_btnYes"
LOADING_SCREEN_ID = "ctl00_ctl00_ASPxSplitter1_Content_ContentSplitter_MainContent_ASPxCallbackPanel1_LD"
KEYWORDS = [ "SSH1151" ]
# MP3_PATH = "8qxviyxizu.mp3"

# =========================
# FUNCTIONS
# =========================

# def login(driver, wait):
    # user_input = wait.until(EC.presence_of_element_located((By.ID, "tbUserName")))
    # user_input.clear()
    # user_input.send_keys(USERNAME)

    # password_input = wait.until(EC.presence_of_element_located((By.ID, "tbPassword")))
    # driver.execute_script("arguments[0].click();", password_input)
    # driver.execute_script("arguments[0].value = arguments[1];", password_input, PASSWORD)
    # password_input.send_keys(PASSWORD[-1])

    # print("Đã điền username và password ")
    # time.sleep(30)

def waiting_for_login_ok(driver, event, check_interval=1):
    if event.is_set():
        try:
            driver.find_element(By.ID, "ctl00_ctl00_ASPxSplitter1_LogoImage")
            event.set()
            print(f"Đăng nhập thành công")
        except NoSuchElementException:
            pass
            print("Không tìm thấy logo đâu cả")
        time.sleep(check_interval)

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

def search_and_save(driver, wait):
    driver.get("https://dk-sis.hust.edu.vn/ClassList.aspx")
    time.sleep(2)

    for kw in KEYWORDS:
        driver.get("https://dk-sis.hust.edu.vn/ClassList.aspx")
        time.sleep(2)
        attempt = 0
        while attempt < 2:
            try:
                input_field = wait.until(EC.presence_of_element_located((By.ID, SUBJECT_INPUT_ID)))
                input_field.clear()
                time.sleep(1)
                input_field.send_keys(kw)
                time.sleep(3)
                break 
            except Exception as e:
                attempt += 1
                time.sleep(2) 
        malop = []

        while True:
            try:
                # Xử lý dữ liệu ở trang hiện tại
                malop += process_rows(driver)

                # Kiểm tra xem có nút Next được bật không
                next_button = driver.find_element(By.ID, "ctl00_ctl00_ASPxSplitter1_Content_ContentSplitter_MainContent_gvClassList_DXPagerBottom_PBN")
                tag_name = next_button.tag_name
                class_name = next_button.get_attribute("class")

                # Nếu tag là <b> hoặc class có chứa 'dxp-disabledButton' thì dừng
                if tag_name == "b" or "dxp-disabledButton" in class_name:
                    print("Nút Next đã bị vô hiệu hóa, dừng lại.")
                    break

                # Nếu còn click được thì click và chờ load trang
                next_button.click()
                WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tr.dxgvDataRow_Moderno"))
                )
                time.sleep(1)

            except NoSuchElementException:
                print("Không tìm thấy nút Next, dừng lại.")
                break

            except Exception as e:
                print(f"Lỗi khi xử lý nút Next: {e}")
                break

        if not malop:
            print(f" Không tìm thấy lớp nào cho học phần {kw} với số lượng sinh viên ít hơn 50.")
        else:
            print(f" Đang đăng ký các lớp: {', '.join(malop)}")
            for ma_lop in malop:

                register_class(driver, wait, ma_lop)
                time.sleep(5)
                
        return False
                    

def register_class(driver, wait, class_id):
    try :
        driver.get(URL_REGISTER)
        register_input = wait.until(EC.presence_of_element_located((By.ID, REGISTER_INPUT_ID)))
        register_input.clear()
        register_input.send_keys(class_id)
        register_button = wait.until(EC.element_to_be_clickable((By.ID, REGISTER_BUTTON_ID)))
        register_button.click()
        wait.until(EC.invisibility_of_element_located((By.ID, LOADING_SCREEN_ID)))

        print(f" Đã gửi đăng ký lớp {class_id}.")
        
        try:
                send_register_button = wait.until(EC.element_to_be_clickable((By.ID, REGISTER_SEND_BUTTON_ID)))
                send_register_button.click()
                yes_button = wait.until(EC.element_to_be_clickable((By.ID, REGISTER_CONFIRM_BUTTON_ID)))
                yes_button.click()
        except Exception as e :
                print(f" Lỗi khi ấn nút đăng ký lớp  {class_id} ")
        
    except Exception as e:
        print(f" Lỗi khi đăng ký lớp {class_id}")
        return False

def check_class_status():
    return False

# =========================
# MAIN
# =========================

if __name__ == "__main__":
    wait = WebDriverWait(driver, 10)
    driver.get(URL_LOGIN)

    while True:
        # search_and_save(driver, wait)
        search_and_save(driver, wait)
        time.sleep(10)

        #     try:
        #         ok_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".dxpcLite_Office2010Blue .dxbButton")))
        #         ok_button.click()
        #         print("Đã ấn nút OK.")
        #     except:
        #         pass



