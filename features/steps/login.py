from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

@given(u'Я открыл страницу "Входа"')
def open_login_page(context):
    context.browser.get('http://localhost:8000/api/login/')
    context.browser.maximize_window()

@when(u'Я ввожу текст "{text}" в поле "{name}"')
def enter_text(context, text, name):
    context.browser.find_element(By.NAME, name).send_keys(text)

@when(u'Я ввожу пароль "{text1}" в поле "{name1}"')
def enter_text(context, text1, name1):
    context.browser.find_element(By.NAME, name1).send_keys(text1)



@when(u'Я отправляю форму')
def submit_form(context):
    context.browser.find_element(By.XPATH, '//button[contains(text(), "Авторизоваться")]').click()

@then(u'Я должен быть на главной странице')
def should_be_at_main(context):
    assert context.browser.current_url == 'http://localhost:8000/api/posta/'

@when(u'Я ввожу данные для авторизации')
def enter_text(context):
    context.browser.find_element(By.NAME, 'username').send_keys('task@gmail.com')
    context.browser.find_element(By.NAME, 'password').send_keys('taskmaster1')

@when(u'Я ввожу "{text2}" в поле для поиска')
def enter_text(context, text2):
    context.browser.find_element(By.NAME, "que").send_keys(text2)

@when(u'Я отправляю поисковую форму')
def submit_form(context):
    context.browser.find_element(By.NAME, 'que').submit()

@when(u'Я жду сек 7')
def ww(context):
    time.sleep(7)

@then(u'Я должен быть на странице пользователя')
def should_be_at(context):
    assert context.browser.current_url == 'http://localhost:8000/api/users/asd/'

