from datetime import datetime
import time 
import sys
import warnings
import configparser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service

s=Service('./dependencies/chromedriver.exe')
options = Options()
options.add_argument("window-size=1920,1060")
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.headless = True
driver = webdriver.Chrome(service=s, options=options)
driver.get("https://www.cotps.com/#/pages/transaction/transaction")
warnings.filterwarnings("ignore", category=DeprecationWarning) 
act = ActionChains(driver)

print("Initializing COTPS trading bot...")

def readconfig_login():
    config = configparser.ConfigParser()
    config.read_file(open(r'config.txt'))
    num = config.get('bot config', 'num')
    pw = config.get('bot config', 'pw')
    time.sleep(5)
    state_number_field_click = driver.find_element_by_xpath("/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[5]/uni-text")
    state_number_field_click.click()
    time.sleep(1)
    state_number_field_UK = driver.find_element_by_xpath("/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[2]/uni-view[214]")
    state_number_field_UK.click() 
    time.sleep(1)
    num_field = driver.find_element_by_xpath("/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[5]/uni-input/div/input")
    num_field.send_keys(num)
    print("Populating number from config file.")
    pw_field = driver.find_element_by_xpath("/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[7]/uni-input/div/input")
    pw_field.send_keys(pw)
    print("Populating password from config file.")
    time.sleep(1)
    login_btn = driver.find_element_by_xpath("/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-button")
    login_btn.click()
    print("Logging in...")
    time.sleep(3)
    transaction_hall_btn = driver.find_element_by_xpath("/html/body/uni-app/uni-tabbar/div[1]/div[3]/div")
    transaction_hall_btn.click()
    print("Navigating to transaction hall...")
###
readconfig_login()
def get_wallet_balance():
    time.sleep(2)
    wallet = driver.find_element_by_class_name("division-right")
    wallet_bal = wallet.find_element_by_class_name("division-num").text
    return wallet_bal
###
def get_wallet_balance_float():
    time.sleep(2)
    wallet = driver.find_element_by_class_name("division-right")
    wallet_bal = wallet.find_element_by_class_name("division-num")
    wallet_bal_float = int(float(wallet_bal.text)) 
    return wallet_bal_float
###
wallet_bal = get_wallet_balance()
wallet_bal_float = get_wallet_balance_float()
###
def transactions(wallet_bal, wallet_bal_float):
    while True:
        wallet_bal_float = get_wallet_balance_float()
        wallet_bal = get_wallet_balance()
        while wallet_bal_float > 4:
            now = datetime.now()
            current_time = now.strftime(("%H:%M:%S"))
            print(f'Wallet Balance is: {wallet_bal} USDT')
            print("Searching for new trade...")
            WebDriverWait(driver, 6).until(EC.element_to_be_clickable((By.XPATH, "/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[4]/uni-button"))).click()
            time.sleep(6)
            order_amount = WebDriverWait(driver, 7).until(EC.visibility_of_element_located((By.XPATH, "/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[7]/uni-view/uni-view/uni-view[5]/uni-text[2]/span"))).text
            print(f"Confirming trade @{order_amount}\nTime of trade: {current_time}")
            WebDriverWait(driver, 6).until(EC.element_to_be_clickable((By.XPATH, "/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[7]/uni-view/uni-view/uni-view[6]/uni-button[2]"))).click()
            time.sleep(8)
            WebDriverWait(driver, 8).until(EC.element_to_be_clickable((By.XPATH, "//*[text()='Confirm']"))).click()
            time.sleep(3)
            wallet_bal_float = get_wallet_balance_float()
            wallet_bal = get_wallet_balance()
        else:
            print(f'Wallet Balance is: {wallet_bal} USDT')
            for remaining in range(7800, 0, -1):
                sys.stdout.write("\r")
                countdown = time.strftime('%H:%M:%S', time.gmtime(remaining))
                sys.stdout.write(f"Time till next trade: {countdown}")
                sys.stdout.flush()
                time.sleep(1)
                if remaining == 1:
                    driver.refresh()
                    print("\r")
                    print("Refreshing Page...\r")
                    time.sleep(5)
                    break
transactions(wallet_bal, wallet_bal_float)

