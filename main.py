import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from typing import List
from selenium.webdriver.remote.webelement import WebElement
import os



# Запуск драйвера Chrome
driver = webdriver.Chrome()

# логин пароль
username = 'mail@gmail.com'
password = 'pass'


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


def get_time(event_id: List[str]) -> dict:
    """
    Создает словарь ид событий и время.

    :param event_id: ID событий
    :return: время
    """
    id_time = {}
    for id in event_id:
        id_game = driver.find_elements(By.XPATH, f'//div[starts-with(@data-role, "event-id-{id}")]')
        for game_person in id_game:
            player_elements = game_person.find_element(By.XPATH, './/span[contains(@class, "Text_base--RfU") and contains(@class, "Text_general--tM6") and contains(@class, "Text_f_xs--DFC") and contains(@class, "Text_center--H1r")]')
            id_time[id] = player_elements.text
    return id_time


def get_linc(event_id: List[str]) -> dict:
    linc = {}

    for id in event_id:
        id_game = driver.find_elements(By.XPATH, f'//div[starts-with(@data-role, "event-id-{id}")]')
        for game_linc in id_game:
            linc_game = game_linc.find_element(By.XPATH, './/div[contains(@class, "Box_box--BuJ") and contains(@class, "EventParticipants_event--M6q") and contains(@class, "EventParticipants_table--ZqR")]')
            linc[id] = linc_game
    return linc


def split_find_elem(find_class, begin):
    text_find = ''
    if begin == 'span':
        text_find = './/span['
    elif begin == 'div':
        text_find = './/div['
    find_class = find_class.split(" ")

    for i in range(len(find_class)):
        if i == len(find_class) - 1:
            text_find += f'contains(@class, "{find_class[i]}")]'
        else:
            text_find += f'contains(@class, "{find_class[i]}") and '
    return text_find


def get_total(url):
    """
    Создает словарь имен игроков для заданных событий.

    :param event_id: ID событий
    :return: Словарь с именами игроков, сгруппированными по событию  """

    driver.get(url)
    time.sleep(4)
    id_total = []
    total_list = []
    text_class1 = 'Box_box--BuJ Box_wrap--DIP'
    text_class2 = "OutcomeButton_coef--ZyE Text_base--RfU Text_general--tM6 Text_f_m--u3O Text_right--YmC Text_bold--b7X Text_l_normal--AeR"

    ferst_find = driver.find_element(By.XPATH,
                                     f'.//span[contains(@class, "Text_base--RfU") and contains(@class, "Text_general--tM6") and contains(@class, "Text_f_l--erO") and contains(@class, "Text_left--lRL") and contains(@class, "Text_l_normal--AeR") and text()="Тотал"]/../..')

    second_find = ferst_find.find_element(By.XPATH, f'{split_find_elem(text_class1, "div")}')

    finish = second_find.find_elements(By.XPATH, f'{split_find_elem(text_class2, "span")}')

    for i in finish:
        id_total.append(i)
        total_list.append(i.text)
    return total_list[-1], id_total[-1]

def time_to_seconds(time_str: str) -> int:
    """
    Преобразует строку времени в секунды.

    :param time_str: Время в формате 'MM:SS'
    :return: Время в секундах
    """
    minutes, seconds = map(int, time_str.split(':'))
    return minutes * 60 + seconds


def is_time_in_range(time_str: str, min_time: str, max_time: str) -> bool:
    """
    Проверяет, находится ли время в заданном диапазоне.

    # Пример использования
    # time_str = '8:09'
    # min_time = '65:00'
    # max_time = '70:00'

    :param time_str: Время для проверки в формате 'MM:SS'
    :param min_time: Минимальное время в формате 'MM:SS'
    :param max_time: Максимальное время в формате 'MM:SS'
    :return: True, если время в диапазоне, иначе False
    """
    time_sec = time_to_seconds(time_str)
    min_sec = time_to_seconds(min_time)
    max_sec = time_to_seconds(max_time)
    return min_sec <= time_sec <= max_sec

event_id = get_event_id() 
print(event_id)
# name_players= get_name_player(event_id)
# print(name_players)
time_id = get_time(event_id)
print(time_id)
# param = get_linc(event_id)
# param['41259167'].click()

sort_id = []
for key, value in time_id.items():
    if value[0] == '(':
        print(" ")
    elif is_time_in_range(value, '75:00', '85:00') == True:
        sort_id.append(key)


summ = 0
for pop in sort_id:
    time.sleep(5)
    # print(f"https://www.favbet.ua/uk/sports/event/soccer/{pop}/")
    finish = get_total(f"https://www.favbet.ua/uk/sports/event/soccer/{pop}/")
    print(finish)
    summ += float(finish[0]) * 20

print(summ)
