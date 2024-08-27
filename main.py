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
# login(driver, username, password)

url = "https://www.favbet.ua/uk/live/soccer/"
driver.get(url)
# time.sleep(2)
# driver.refresh()
time.sleep(9)



def get_event_id() -> List[str]:
    """
    Получает список всех ID событий на странице.

    :return: Список строк с ID событий
    """
    event_id = []
    elements = driver.find_elements(By.XPATH, '//div[starts-with(@data-role, "event-id-")]')
    for element in elements:
        data_role = element.get_attribute('data-role')
        number = data_role.split('-')[-1]
        event_id.append(number)
    return event_id


def get_name_player(event_id: List[str]) -> dict:
    """
    Создает словарь имен игроков для заданных событий.

    :param event_id: ID событий
    :return: Словарь с именами игроков, сгруппированными по событию
    """
    name_players_dict = {}
    for id in event_id:
        players_in_event = []
        name_playr = driver.find_elements(By.XPATH, f'//div[starts-with(@data-role, "event-id-{id}")]')
        for game_person in name_playr:
            player_elements = game_person.find_elements(By.XPATH,
                                                        './/span[contains(@class, "Participant_participantName--zIC")]')
            for player in player_elements:
                player_name = player.get_attribute('title')
                players_in_event.append(player_name)
        name_players_dict[id] = players_in_event

    return name_players_dict




event_id = get_event_id()
print(event_id)
name_players= get_name_player(event_id)
print(name_players)
print(name_players['41248708'])