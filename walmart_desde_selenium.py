from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from time import sleep

IP = '103.216.82.50'        # Host o ip
PORT = '53281'              # Puerto
PROXY = IP + ':' + PORT     # Formato proxie

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server=%s' % PROXY)
chrome = webdriver.Chrome(options=chrome_options)
chrome.get("https://www.walmart.com.mx/envio-sin-costo")

sleep(20)
chrome.quit()