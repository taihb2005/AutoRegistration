from selenium.webdriver.chrome.options import Options

ENABLE_SPAM_MODE = True

URL_LOGIN = "https://dk-sis.hust.edu.vn/Users/Login.aspx"
URL_CLASSLIST = "https://dk-sis.hust.edu.vn/ClassList.aspx"
URL_REGISTER = "https://dk-sis.hust.edu.vn/Default.aspx"

SUBJECT_INPUT_ID = "ctl00_ctl00_ASPxSplitter1_Content_ContentSplitter_MainContent_gvClassList_DXFREditorcol1_I"
REGISTER_INPUT_ID = "ctl00_ctl00_ASPxSplitter1_Content_ContentSplitter_MainContent_ASPxCallbackPanel1_tbDirectClassRegister_I"
REGISTER_BUTTON_ID = "ctl00_ctl00_ASPxSplitter1_Content_ContentSplitter_MainContent_ASPxCallbackPanel1_btDirectClassRegister"
REGISTER_SEND_BUTTON_ID = "ctl00_ctl00_ASPxSplitter1_Content_ContentSplitter_MainContent_ASPxCallbackPanel1_btSendRegister"
REGISTER_CONFIRM_BUTTON_ID = "ctl00_ctl00_ASPxSplitter1_Content_ContentSplitter_MainContent_ASPxCallbackPanel1_pcYesNo_pcYesNoBody1_ASPxRoundPanel1_btnYes"
REGISTER_DELETE_BUTTON_ID = "ctl00_ctl00_ASPxSplitter1_Content_ContentSplitter_MainContent_ASPxCallbackPanel1_btDeleteClass"
LOADING_SCREEN_ID = "ctl00_ctl00_ASPxSplitter1_Content_ContentSplitter_MainContent_ASPxCallbackPanel1_LD"
NEXT_BUTTON = "ctl00_ctl00_ASPxSplitter1_Content_ContentSplitter_MainContent_gvClassList_DXPagerBottom_PBN"
CLASS_REGISTERED_TABLE = "ctl00_ctl00_ASPxSplitter1_Content_ContentSplitter_MainContent_ASPxCallbackPanel1_gvRegisteredList"

# Course registration keywords (for auto-search mode)
KEYWORDS = []

# Direct class registration (for specific class IDs)
CLASS_LIST = []  # Add specific class IDs here, e.g., ["165236"]

# Site monitoring settings
SITE_CHECK_INTERVAL = 30  # Seconds between site availability checks
LOGIN_WAIT_TIME = 40  # Seconds to wait for manual login

DEFAULT_STATE = "Hết chỗ"

def get_options():
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("user-agent=Mozilla/5.0 ... Chrome/137.0.0.0 Safari/537.36")
    return options
