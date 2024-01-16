from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


@when(u'Я открываю детали статьи')
def submit_form(context):
    context.browser.find_element(By.NAME, 'zergy').click()

@when(u'Я нажимаю кнопку "Редактировать Пост"')
def submit_s(context):
    context.browser.find_element(By.NAME, 'pupdate').click()

@when(u'Я заполняю новые данные')
def enter_text(context):
    time.sleep(2)
    context.browser.find_element(By.NAME, 'title').clear()
    time.sleep(2)
    context.browser.find_element(By.NAME, 'slug').clear()
    time.sleep(2)
    context.browser.find_element(By.NAME, 'body').clear()
    time.sleep(2)
    context.browser.find_element(By.NAME, 'title').send_keys('Emoclew')
    context.browser.find_element(By.NAME, 'slug').send_keys('grez')
    context.browser.find_element(By.NAME, 'body').send_keys('txe tse si sit')

@when(u'Я отправляю новые данные')
def submit_form(context):
    context.browser.find_element(By.XPATH, '//button[contains(text(), "Обновить статью")]').click()

@then(u'Я должен быть н отредактированной странице деталей поста')
def should_be_at_main(context):
    assert context.browser.current_url == 'http://localhost:8000/api/posta/grez/'