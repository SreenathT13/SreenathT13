from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import time
import US069_B
import NEW_config
from New_UI_Automation import Board_Automation, print_log, print_error, print_warning


import datetime

board = Board_Automation("chrome")
board.browser.get(US069_B.Board_URL)
print_log(f"{US069_B.Board_URL} URl is opened in browser")
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

#board.browser.wait.until(EC.visibility_of_element_located((By.XPATH, US069_B.REFRESH)))
#board.browser.find_element_by_xpath(US069_B.REFRESH).click()
time.sleep(15)
board.browser.find_element(By.XPATH, US069_B.Ignition_ON).click()
time.sleep(3)
print_log("Ignition Turned ON")
#RPM = board.browser.find_element(By.XPATH, US069_B.RPM_Slider)
#ActionChains(board.browser).move_to_element(RPM).click_and_hold(RPM).pause(2).move_by_offset(80, 0).release().perform()


#print_log("Changed RPM value")
time.sleep(10)
board.browser.find_element(By.XPATH, US069_B.RPM_Graph).click()
time.sleep(5)
print_log("Showing RPM Graph")
board.browser.find_element(By.XPATH, US069_B.Video_Max).click()
print_log("Video Maximized")
time.sleep(10)
board.browser.find_element(By.XPATH, US069_B.Video_Max).click()
print_log("Video Minimized")
time.sleep(5)
board.browser.find_element(By.XPATH, US069_B.Ignition_OFF).click()
time.sleep(5)
print_log("Ignition Turned OFF")
print_log("Reducing Motor Speed")
time.sleep(5)
board.read_progress()
Connect.click()
time.sleep(5)
print_log("Disconnected From Board")
time.sleep(7)
board.close()
print(f"[{datetime.datetime.now().replace(microsecond=0)}] at this time last automation done for US069")
