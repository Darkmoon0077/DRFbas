from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


@when(u'Я открываюю детали профиля')
def submit_form(context):
    context.browser.find_element(By.NAME, 'taskmaster').click()
    time.sleep(1)

@when(u'Я нажимаю кнопку Редактировать профиль')
def submit_form(context):
    context.browser.find_element(By.NAME, 'proedit').click()
    time.sleep(1)

@when(u'Я удаляю существующие данные')
def enter_text(context):
    context.browser.find_element(By.NAME, 'username').clear()
    context.browser.find_element(By.NAME, 'email').clear()
    context.browser.find_element(By.NAME, 'first_name').clear()
    context.browser.find_element(By.NAME, 'last_name').clear()
    context.browser.find_element(By.NAME, 'slug').clear()
    context.browser.find_element(By.NAME, 'bio').clear()
    time.sleep(2)

@when(u'Я добавляю новые данные')
def enter_text(context):
    context.browser.find_element(By.NAME, 'username').send_keys('morag')
    context.browser.find_element(By.NAME, 'email').send_keys('mac@dugal.ro')
    context.browser.find_element(By.NAME, 'first_name').send_keys('mora')
    context.browser.find_element(By.NAME, 'last_name').send_keys('mac')
    context.browser.find_element(By.NAME, 'slug').send_keys('maccy')
    context.browser.find_element(By.NAME, 'bio').send_keys('i dont know where it come from')
    

@when(u'Я нажимаю кнопку Подтвердить изменение профиля')
def submit_form(context):
    context.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    context.browser.find_element(By.XPATH, '//button[contains(text(), "Подтвердить изменение профиля")]').click()

@then(u'Я должен быть на странице деталей профиля')
def should_be_at_main(context):
    assert context.browser.current_url == 'http://localhost:8000/api/users/maccy/'