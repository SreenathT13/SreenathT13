import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import JP158_B
import NEW_config
from New_UI_Automation import Board_Automation, print_log, print_error, print_warning
from selenium.common.exceptions import NoSuchElementException, TimeoutException


import time
board = Board_Automation("chrome")
board.open_browser()
#board.list_boards()
time.sleep(10)
board.click_cookies_ok()
#board.connect_to_board('CN251')
#start = time.time()
time.sleep(15)
live = board.browser.find_element(By.XPATH, NEW_config.LIVE)
live.click()
print_log("Start Evaluation")


time.sleep(5)
Connect = board.browser.find_element(By.XPATH, NEW_config.CONNECT_BUTTON1)
Connect.click()

print_log("Connected to Board")
time.sleep(15)

#print_log("Disconnected From Board")
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

time.sleep(20)
board.browser.find_element(By.XPATH, '//*[@id="stepformcontainer"]/tx-elements[1]/div[2]/div/div/div/span[1]/label').click()

time.sleep(5)
print_log("capacitor charged with 3w")
time.sleep(2)
board.browser.find_element(By.XPATH, '//*[@id="stepformcontainer"]/tx-elements[4]/div[2]/div/div/div/button').click()

time.sleep(5)
print_log("pressed next on Jp158(remote function)")
time.sleep(2)
board.browser.find_element(By.XPATH, JP158_B.PREVIOUS_Button).click()

time.sleep(5)
print_log("pressed Prev on Jp158(remote function)")
time.sleep(2)
board.browser.find_element(By.XPATH, JP158_B.PLAY_OR_PAUSE_Button).click()

time.sleep(5)
print_log("pressed Play/pause on Jp158(remote function)")
time.sleep(2)
board.browser.find_element(By.XPATH, JP158_B.STOP_Button).click()

time.sleep(5)
print_log("pressed Stop on Jp158(remote function)")
time.sleep(2)
board.read_progress()

Connect.click()
time.sleep(5)
print_log("Disconnected From Board")
time.sleep(7)
print(f"[{datetime.datetime.now().replace(microsecond=0)}] at this time last automation done for jp158")


