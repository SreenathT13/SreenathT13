from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import RZ_A2M_B
import NEW_config
import time
from New_UI_Automation import Board_Automation, print_log, print_error, print_warning


import datetime

board = Board_Automation("chrome")
board.browser.get(RZ_A2M_B.URL)
print_log(f"{RZ_A2M_B.URL} URl is opened in browser")
board.browser.maximize_window()
print_log("Browser Maximized")
#board.list_boards()
time.sleep(10)
board.click_cookies_ok()
time.sleep(15)
live = board.browser.find_element(By.XPATH, NEW_config.LIVE)
live.click()
print_log("Start Evaluation")


time.sleep(5)
Connect = board.browser.find_elemen(By.XPATH, NEW_config.CONNECT_BUTTON1)
Connect.click()


time.sleep(15)
print_log("Connected to Board")
flag = 1
while flag:
    progress = board.read_progress()
    if progress:
        start = time.time()
    for i in progress:
        if "SYSTEM READY" in i:
            print_log("System is Ready")
            flag = 0
    if time.time() - start > 120:
        print_error("progress is not active for 2 min")
        board.close()
        exit(0)
board.browser.implicitly_wait(3)

board.stream_check()
time.sleep(15)
board.browser.find_element(By.XPATH, RZ_A2M_B.Start).click()
print_log("Fast demo video started")
time.sleep(20)
board.read_progress()
board.browser.find_element(By.XPATH, RZ_A2M_B.Stop).click()
time.sleep(5)
board.read_progress()

board.browser.find_element(By.XPATH, RZ_A2M_B.LS_Max).click()
print_log("Setup Stream Video Maximized")
time.sleep(8)
board.browser.find_element(By.XPATH, RZ_A2M_B.LS_Max).click()
print_log("Setup Stream Video Minimized")
time.sleep(5)
board.browser.find_element(By.XPATH, RZ_A2M_B.MS_Max).click()
print_log("Monitor Stream Video Maximized")
time.sleep(5)
board.browser.find_element(By.XPATH, RZ_A2M_B.MS_Max).click()
print_log("Monitor Stream Video Minimized")
time.sleep(4)
board.read_progress()
Connect.click()
time.sleep(5)
print_log("Disconnected From Board")
time.sleep(7)
board.close()
print(f"[{datetime.datetime.now().replace(microsecond=0)}] at this time last automation done for RZ_A2M")