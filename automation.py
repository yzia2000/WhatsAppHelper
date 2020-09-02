from time import sleep
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
import socket

options = webdriver.ChromeOptions()
# options.add_argument("--no-sandbox")
# options.add_argument("--headless")
options.add_argument(r"user-data-dir=/home/yushi/Documents/WhatsAppHelper/.chrome_cache")

driver = webdriver.Chrome(options=options)

driver.get('https://web.whatsapp.com')

def sendMessage(target, message):
    user = driver.find_element_by_xpath("//span[@title='{}']".format(target))
    user.click()

    txt_box=driver.find_element(By.XPATH , '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
    txt_box.send_keys(message)
    txt_box.send_keys("\n")
