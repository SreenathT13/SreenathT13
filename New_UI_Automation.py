
import NEW_config
import JP158_B
import datetime
import time
import pytest
from selenium import webdriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_log(*content):
    print(f"{bcolors.OKGREEN}[{datetime.datetime.now().replace(microsecond=0)}] {' '.join(content)}{bcolors.ENDC}")


def print_warning(*content):
    print(f"{bcolors.WARNING}[{datetime.datetime.now().replace(microsecond=0)}] {' '.join(content)}{bcolors.ENDC}")


def print_error(*content):
    print(f"{bcolors.FAIL}[{datetime.datetime.now().replace(microsecond=0)}] {' '.join(content)}{bcolors.ENDC}")


class Board_Automation:
    def __init__(self, browser_name: str = 'chrome', download_path: str = r'D:\Tenxer\Projects\Automation'):
        self.progress = []
        self.live = None
        self.connect = None
        self.disconnect_button = None
        self.ready = None
        if browser_name.lower() == 'chrome':
            chrome_options = webdriver.ChromeOptions()
            prefs = {
                "profile.default_content_settings.popups": 0,
                "download.default_directory": download_path
            }
            chrome_options.add_experimental_option("prefs", prefs)
            #chrome_options.a(disable-infobars)
            self.browser = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=chrome_options)
            self.wait = WebDriverWait(self.browser, 30)
            self.actions = ActionChains(self.browser)
        else:
            print_error(f"{browser_name} Browser is not supported")
            return

    def open_browser(self):
        self.browser.get(NEW_config.JP158)
        print_log(f"{NEW_config.JP158} URL is opened in browser")

        self.browser.maximize_window()
        print_log("browser window is maximized")

        #self.wait.until(EC.visibility_of_all_elements_located((By.XPATH, NEW_config.FIRST_BOARD)))

    def list_boards(self):
        table = self.browser.find_elements_by_xpath(NEW_config.LIST_OF_BOARDS)
        rows = table[0].find_elements(By.TAG_NAME, "tr")
        boards = []
        for row in rows:
            # print(row)
            board = row.find_elements(By.TAG_NAME, "td")
            code = board[1].text
            boards.append(code)
        print(boards)
        return boards

    def click_cookies_ok(self):
        buttons = self.browser.find_elements_by_xpath("//*[contains(text(), 'I agree')]")
        for btn in buttons:
            btn.click()

    def connect_to_board(self, BOARD: str):
        table = self.browser.find_elements_by_xpath(NEW_config.LIST_OF_BOARDS)
        rows = table[0].find_elements(By.TAG_NAME, "tr")
        entered_board = False
        for row in rows:
            # print(row)
            board = row.find_elements(By.TAG_NAME, "td")
            code = board[1].text
            if BOARD in code:
                print_log(f"Sr.N        :{board[0].text}")
                print_log(f"Code        :{board[1].text}")
                print_log("Board Name  :", board[2].text)
                print_log("Description :", board[3].text)
                print_log("Action      :", board[4].text)
                self.browser.execute_script("arguments[0].scrollIntoView();", board[4])
                board[4].click()
                print_log("Entering board " + str(code))
                entered_board = True
                break
        if not entered_board:
            print_error(f"{BOARD} Board not found")
            return

        self.browser.execute_script("window.scrollBy(0,document.body.scrollHeight)")
        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="default-dashboard"]/div[1]/nav/div[2]/form/span')))
        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="render-main"]/div/div[1]/div/ul/li[2]')))
        self.live = self.browser.find_element_by_xpath(NEW_config.LIVE)
        self.live.click()
        self.connect = self.browser.find_elements_by_xpath(NEW_config.CONNECT_BUTTON1)[0]
        self.connect.click()
        time.sleep(5)
        try:
            self.ready = self.browser.find_element_by_xpath(NEW_config.READY)
            if "ready" in str(self.ready.text).lower():
                print_log("Device connected")
            else:
                print_log("Device is busy")
                self.browser.close()
                exit(0)
        except NoSuchElementException:
            print_error("Device is Busy")
            self.browser.close()
            exit(0)

    def read_progress(self):
        progress_log = '//*[@id="console_status"]/div/tx-elements/div[2]/div/ul'
        self.wait.until(EC.visibility_of_all_elements_located((By.XPATH, progress_log)))
        progress_data = self.browser.find_elements_by_xpath(progress_log)
        latest_progress = []
        temp = progress_data[0].find_elements(By.TAG_NAME, "li")
        for i in temp[len(self.progress):]:
            if i.text not in self.progress:
                self.progress.append(i.text)
                print_warning(i.text)
                latest_progress.append(i.text)
        return latest_progress

    def stream_check(self):
        iframes = self.browser.find_elements_by_xpath("//iframe")
        for index, iframe in enumerate(iframes):
            self.browser.switch_to.frame(iframe)
            print_log("Switched to iframe ")
            try:
#                continue_btn = self.browser.find_element_by_id("register")
#                self.browser.execute_script("arguments[0].click();", continue_btn)
                self.wait.until(EC.presence_of_element_located((By.ID, "curbitrate1")))
                for _ in range(60):
                    stream_rate = str(self.browser.find_element_by_id("curbitrate1").text).strip()
                    print_warning("Stream Rate ", stream_rate)
                    if stream_rate and int(stream_rate.split()[0]) > 0:
                        print_log("Stream Working")
                        break
                    time.sleep(1)
            except (NoSuchElementException, TimeoutException):
                print_error("Stream is not working")
            self.browser.switch_to.parent_frame()

    def download_graph(self, prahp_xpath):
        graph = '//*[@id="modebar-8795b9"]/div[1]/a/svg'
        # gra = '//*[@id="c8cadd6c-9093-54e0-2d14-26ea01cb4178"]/ng-content/tx-elements/div[2]/div/div[3]/plotly/div/div/div/svg[1]/g[2]/g[1]/rect[1]'
        # graph = '//*[@id="c8cadd6c-9093-54e0-2d14-26ea01cb4178"]/ng-content/tx-elements/div[2]/div/div[3]/plotly/div/div/div/svg[1]/g[2]/g[1]/rect[1]'
        self.wait.until(EC.visibility_of_element_located((By.XPATH, graph)))
        temp = self.browser.find_element_by_xpath(graph)
        print(temp.size)

    def disconnect(self):
        self.diconnect_button =self.browser.find_element_by_xpath(NEW_config.DISCONNECT_BUTTON1)
        if self.disconnect_button:
            self.disconnect_button.click()
            self.disconnect_button = None

    def close(self):
        if self.disconnect_button:
            self.disconnect_button.click()
            self.browser.implicitly_wait(3)
        self.browser.close()


if __name__ == "__main__":
    pass
