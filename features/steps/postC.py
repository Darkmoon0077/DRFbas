from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

@when(u'Я нажимаю кнопку Добавить статью')
def submit_form(context):
    context.browser.find_element(By.NAME, 'add').click()

@when(u'Я заполняю форму создания поста')
def enter_text(context):
    context.browser.find_element(By.NAME, 'title').send_keys('Welcome')
    context.browser.find_element(By.NAME, 'slug').send_keys('zergy')
    context.browser.find_element(By.NAME, 'body').send_keys('Tis is est ext')

@when(u'Я отправляю форму создания статьи')
def submit_form(context):
    context.browser.find_element(By.XPATH, '//button[contains(text(), "Добавить статью")]').click()

@then(u'Я должен быть на странице деталей поста')
def should_be_at_main(context):
    assert context.browser.current_url == 'http://localhost:8000/api/posta/zergy/'