from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import EU036_B
import time
import NEW_config
from New_UI_Automation import Board_Automation, print_log, print_error, print_warning


import datetime
board = Board_Automation("chrome")
board.browser.get(EU036_B.URL)
print_log(f"{EU036_B.URL} URl is opened in browser")
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
Connect = board.browser.find_element(By.XPATH, NEW_config.CONNECT_BUTTON1)
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

TS = board.browser.find_element(By.XPATH, EU036_B.TS_Control)
TS.click()
time.sleep(40)
board.read_progress()
board.browser.find_element(By.XPATH, EU036_B.Sim_W_B).click()
time.sleep(10)
board.read_progress()
TS.click()
LV_Max = board.browser.find_element(By.XPATH, EU036_B.Live_Setup_Video_Max)
LV_Max.click()
print_log("Video Maximized")
time.sleep(10)
LV_Max.click()
print_log("Video Minimized")
board.read_progress()
p2_c = board.browser.find_element(By.XPATH, EU036_B.P2_Sensor_Control)
ActionChains(board.browser).move_to_element(p2_c).pause(2).click_and_hold(p2_c).move_by_offset(100, 0).release().perform()
board.read_progress()
time.sleep(15)
board.read_progress()
Connect.click()
time.sleep(5)
print_log("Disconnected From Board")
time.sleep(7)
board.close()
print(f"[{datetime.datetime.now().replace(microsecond=0)}] at this time last automation done for EU036")
