

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from typing import List
from selenium.webdriver.remote.webelement import WebElement
import os

# Запуск драйвера Chrome
driver = webdriver.Chrome()


url = "https://www.favbet.ua/uk/sports/event/soccer/41226125/"
driver.get(url)
# time.sleep(2)
# driver.refresh()
time.sleep(9)


def get_time(event_id: List[str]) -> dict:
    """
    Создает словарь тотала.

    :param event_id: ID событий
    :return: тотал
    """
    id_time = {}
    for id in event_id:
        id_game = driver.find_elements(By.XPATH, f'//div[starts-with(@data-role, "event-id-{id}")]')
        for game_person in id_game:
            player_elements = game_person.find_element(By.XPATH, './/span[contains(@class, "Text_base--RfU") and contains(@class, "Text_general--tM6") and contains(@class, "Text_f_xs--DFC") and contains(@class, "Text_center--H1r")]')
            id_time[id] = player_elements.text
    return id_time
