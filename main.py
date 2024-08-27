import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from typing import List
from selenium.webdriver.remote.webelement import WebElement
import os

# Запуск драйвера Chrome
driver = webdriver.Chrome()

# логин пароль
username = 'san40dndz1@gmail.com'
password = '9rzgx7uEU9'


# вход в аккаунт
def login(driver, username, password):

    driver.get("https://www.favbet.ua/uk/login/?from=header-desktop")
    time.sleep(5)
    login_field = driver.find_element(By.XPATH, '//*[@id="email"]')
    login_field.clear()  # Очистка поля перед вводом
    login_field.send_keys(username)  # Ввод имени пользователя

    # Поиск и ввод пароля
    password_field = driver.find_element(By.XPATH, '//*[@id="password"]')
    password_field.clear()  # Очистка поля перед вводом
    password_field.send_keys(password)  # Ввод пароля

    # Поиск и клик по кнопке входа
    login_button = driver.find_element(By.XPATH, '//button[starts-with(@data-role, "login-page-submit-btn")]')
    login_button.click()  # Клик по кнопке входа

    print(1)
    # Добавление задержки для ожидания загрузки страницы
    time.sleep(5)
login(driver, username, password)
driver.get("https://www.favbet.ua/uk/live/table-tennis/")
time.sleep(2)
driver.refresh()
time.sleep(9)
