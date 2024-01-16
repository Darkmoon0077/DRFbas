from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

@when(u'Я открываю созданную статью')
def submit_form(context):
    context.browser.find_element(By.NAME, 'grez').click()

@when(u'Я нажимаю кнопку "Удалить Пост"')
def submit_s(context):
    context.browser.find_element(By.NAME, 'pdelete').click()

@when(u'Я нажимаю кнопку "Удалить статью"')
def submit_form(context):
    context.browser.find_element(By.XPATH, '//button[contains(text(), "Удалить статью")]').click()