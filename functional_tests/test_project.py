from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Firefox()
driver.get('http://127.0.0.1:8000/api/login/')
driver.maximize_window()
username_input = driver.find_element(By.NAME, 'username')
password_input = driver.find_element(By.NAME, 'password')
login_button = driver.find_element(By.XPATH, '//button[contains(text(), "Авторизоваться")]') 
username_input.send_keys('darkmoon0077@gmail.com') 
password_input.send_keys('zergling1')
time.sleep(3) 
login_button.click()
search_input = driver.find_element(By.NAME, 'que') 
search_input.send_keys('madi')
time.sleep(5)   
search_input.submit()
time.sleep(3) 
unsubscribe_button = driver.find_elements(By.XPATH, '//button[contains(text(), "Отписаться")]')
if unsubscribe_button:
    unsubscribe_button[0].click()
else:
    subscribe_button = driver.find_element(By.XPATH, '//button[contains(text(), "Подписаться")]')
    subscribe_button.click()
time.sleep(7)
driver.quit() 