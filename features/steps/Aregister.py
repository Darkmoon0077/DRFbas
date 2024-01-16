from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

@given(u'Я открыл страницу "Регистрации"')
def open_login_page(context):
    context.browser.get('http://127.0.0.1:8000/api/register')

@when(u'Я ввожу логин "{text1}" в поле "{name1}"')
def enter_text(context, text1, name1):
    context.browser.find_element(By.NAME, name1).send_keys(text1)

@when(u'Я жму кнопку Зарегистрироваться')
def submit_form(context):
    context.browser.find_element(By.XPATH, '//button[contains(text(), "Зарегистрироваться")]').click()

@then(u'Я должен вернутся главную страницу')
def should_be_at_main1(context):
    assert context.browser.current_url == 'http://127.0.0.1:8000/api/posta/'