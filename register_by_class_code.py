import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Import from tool directory
from tool.config import *

def is_site_up(url, timeout=20):
    """Check if the website is accessible"""
    try:
        response = requests.get(url, timeout=timeout)
        return response.status_code == 200
    except requests.RequestException:
        return False

def register_class(driver, wait, class_id):
    """Register for a specific class by class ID"""
    try:
        print(f"Dang thu dang ky lop {class_id}...")
        
        # Navigate to registration page
        driver.get(URL_REGISTER)
        time.sleep(1)
        
        # Fill in class ID
        register_input = wait.until(EC.presence_of_element_located((By.ID, REGISTER_INPUT_ID)))
        register_input.clear()
        register_input.send_keys(class_id)
        
        # Click register button
        register_button = wait.until(EC.element_to_be_clickable((By.ID, REGISTER_BUTTON_ID)))
        register_button.click()
        time.sleep(2)
        
        # Wait for loading to complete
        wait.until(EC.invisibility_of_element_located((By.ID, LOADING_SCREEN_ID)))

        print(f"Da gui dang ky lop {class_id}.")
        
        # Confirm registration
        try:
            send_register_button = wait.until(EC.element_to_be_clickable((By.ID, REGISTER_SEND_BUTTON_ID)))
            send_register_button.click()
            time.sleep(1)
            
            yes_button = wait.until(EC.element_to_be_clickable((By.ID, REGISTER_CONFIRM_BUTTON_ID)))
            yes_button.click()
            
            print(f"Dang ky thanh cong lop {class_id}!")
            return True
            
        except Exception as e:
            print(f"Loi khi xac nhan dang ky lop {class_id}: {e}")
            return False
        
    except Exception as e:
        print(f"Loi khi dang ky lop {class_id}: {e}")
        return False

def main():
    """Main function for direct class registration"""
    print("Khoi dong Direct Class Registration Tool")
    print("=" * 50)
    
    if not CLASS_LIST:
        print("Vui long them ma lop vao CLASS_LIST trong tool/config.py!")
        return
    
    print(f"Danh sach lop can dang ky: {CLASS_LIST}")
    print("Vui long dang nhap thu cong khi trinh duyet mo!")
    print("=" * 50)
    
    # Setup Chrome driver using config function
    options = get_options()
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)
    
    try:
        while True:
            if is_site_up(URL_LOGIN):
                print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Website hoat dong")
                
                # Navigate to login page
                driver.get(URL_LOGIN)
                print(f"Doi {LOGIN_WAIT_TIME} giay de dang nhap thu cong...")
                time.sleep(LOGIN_WAIT_TIME)  # Use config value
                
                # Try to register for each class
                count =  len(CLASS_LIST)
                for class_id in CLASS_LIST:
                    if register_class(driver, wait, class_id):
                        count -= 1
                
                if count == 0:
                    print("Dang ky thanh cong! Nhan Enter de thoat.")
                    input()
                    break
                else:
                    print(f"Khong dang ky duoc lop. Thu lai sau {SITE_CHECK_INTERVAL} giay...")
                    time.sleep(SITE_CHECK_INTERVAL)  # Use config value
            else:
                print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Website khong hoat dong")
                time.sleep(SITE_CHECK_INTERVAL)  # Use config value
                
    except KeyboardInterrupt:
        print("\nDung chuong trinh...")
    except Exception as e:
        print(f"Loi: {e}")
    finally:
        driver.quit()
        print("Tam biet!")

if __name__ == "__main__":
    main() 