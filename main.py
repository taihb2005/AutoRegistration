from selenium.webdriver.support.ui import WebDriverWait
from threading import Event, Thread
from tool.config import *
from tool.utils import *
from tool.auto_register import *

event_logged_in = Event()
stop_event = Event()
register_event = Event()

def monitor_login(driver):
    while not stop_event.is_set():
        try:
            if "Users/Login.aspx" in driver.current_url:
                print("Vui lòng đăng nhâp")
                event_logged_in.clear()
            else:
                if not event_logged_in.is_set():
                    print("Đăng nhập thành công!")
                    event_logged_in.set()
            time.sleep(5)
        except Exception:
            pass
        

def auto_register_loop(driver, wait):
    while not stop_event.is_set():
        try:
            if event_logged_in.wait(timeout=600):
                search_and_save(driver, wait)
                time.sleep(1)
            else: 
                break
        except Exception:
            pass

if __name__ == "__main__":
    try:
        options = get_options()
        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, 10)
        driver.get(URL_LOGIN)

        login_thread = Thread(target=monitor_login, args=(driver,))
        auto_register_thread = Thread(target=auto_register_loop, args=(driver, wait))

        login_thread.start()
        auto_register_thread.start()

        while login_thread.is_alive() and auto_register_thread.is_alive():
            time.sleep(1)

    except (KeyboardInterrupt, Exception):
        pass

    finally:
        stop_event.set()           
        event_logged_in.set()    
        register_event.set() 
        login_thread.join()
        auto_register_thread.join()
        driver.quit()
