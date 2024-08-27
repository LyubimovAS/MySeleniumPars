import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from typing import List
from selenium.webdriver.remote.webelement import WebElement
import os
# Запуск драйвера Chrome
driver = webdriver.Chrome()

username = 'san40dndz1@gmail.com'
password = '9rzgx7uEU9'


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



class Player:
    """
    Класс представляет игрока с соответствующими данными.

    :param name: Имя игрока
    :param event_id: ID события, в котором участвует игрок
    :param score: Основной счет игрока
    :param in_game_score: Текущий счет в игре
    :param coefficient: Коэффициент на игрока
    """
    def __init__(self, name: str, event_id: str, score: int, in_game_score: int, coefficient: float, coeff_obj):
        self.name = name
        self.event_id = event_id
        self.score = score
        self.in_game_score = in_game_score
        self.coefficient = coefficient
        self.coeff_obj = coeff_obj

    def __repr__(self):
        return f"Player({self.name}, Event: {self.event_id}, Score: {self.score}, In-game Score: {self.in_game_score}, Coefficient: {self.coefficient}), Coeff_obj: {self.coeff_obj})"


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


def get_name_player(event_id: List[str]) -> List[str]:
    """
    Создает список имен игроков для заданных событий.

    :param event_id: ID событий
    :return: Список имен игроков
    """
    name_players_list = []
    for id in event_id:
        name_playr = driver.find_elements(By.XPATH, f'//div[starts-with(@data-role, "event-id-{id}")]')
        for game_person in name_playr:
            player_elements = game_person.find_elements(By.XPATH, './/span[contains(@class, "Participant_participantName--zIC")]')
            for player in player_elements:
                player_name = player.get_attribute('title')
                name_players_list.append(player_name)
    return name_players_list

def get_score_by_game(event_id: List[str]) -> List[int]:
    """
    Получает основной счет для каждого игрока.

    :param event_id: ID событий
    :return: Список основных счетов
    """
    score_list = []
    for id in event_id:
        score_by_game = driver.find_elements(By.XPATH, f'//div[starts-with(@data-role, "event-id-{id}")]')
        for scop_by_players in score_by_game:
            player_elements = scop_by_players.find_elements(By.XPATH, './/span[contains(@class, "Column_scoreCell--c8_") and contains(@class, "Text_bold--b7X")]')
            for scope_player in player_elements:
                player_score = scope_player.text
                score_list.append(int(player_score))
    return score_list

def get_score_in_game(event_id: List[str]) -> List[int]:
    """
    Получает текущий счет в игре для каждого игрока.

    :param event_id: ID событий
    :return: Список текущих счетов в игре
    """
    score_list_game = []
    for id in event_id:
        score_by_game = driver.find_elements(By.XPATH, f'//div[starts-with(@data-role, "event-id-{id}")]')
        for scop_by_players in score_by_game:
            player_elements = scop_by_players.find_elements(By.XPATH, './/span[contains(@class, "Column_scoreCell--c8_") and not(contains(@class, "Text_bold--b7X"))]')
            for scope_player in player_elements:
                player_score = scope_player.text
                score_list_game.append(int(player_score))
    return score_list_game

def get_coefficient(event_id: List[str]):
    """
    Получает коэффициенты для каждого игрока.

    :param event_id: ID событий
    :return: Список коэффициентов
    """
    coefficient_player = []
    coeff_obj = []
    for id in event_id:
        score_by_game = driver.find_elements(By.XPATH, f'//div[starts-with(@data-role, "event-id-{id}")]')
        for scop_by_players in score_by_game:
            try:
                player_elements = scop_by_players.find_elements(By.XPATH,
                                                                f'.//div[starts-with(@data-role, "outcome-btn-table-{id}-")]')
                if not player_elements:  # Если список пуст
                    player_elements = scop_by_players.find_elements(By.XPATH,
                                                                    f'.//div[starts-with(@data-role, "outcome-btn-table")]')

                coeff_obj.append(player_elements[0])
                coeff_obj.append(player_elements[1])
                for i in player_elements:
                    coefficient_player.append(float(i.text))


            except:
                coefficient_player.append(0.1)
                coefficient_player.append(0.1)
    return coefficient_player, coeff_obj

def get_coefficient_player(id: int) -> List[float]:
    """
    Получает коэффициенты для конкретного события.

    :param id: ID события
    :return: Список коэффициентов
    """
    coeff = []
    score_by_game = driver.find_elements(By.XPATH, f'//div[starts-with(@data-role, "event-id-{id}")]')
    for scop_by_players in score_by_game:
        player_elements = scop_by_players.find_elements(By.XPATH, f'.//div[starts-with(@data-role, "outcome-btn-table-{id}-")]')
        for i in player_elements:
            coeff.append(float(i.text))
    return coeff
# фильтр score и in_game_score

def create_pairs(player_dict):
    """
    Создает пары игроков из словаря.

    :param player_dict: Словарь игроков
    :return: Список кортежей с парами игроков
    """
    players = list(player_dict.values())
    pairs = []
    for i in range(0, len(players) - 1, 2):
        pairs.append((players[i], players[i + 1]))
    return pairs

def filter_pairs(pairs):
    """
    Фильтрует пары игроков, оставляя только те пары, где оба игрока удовлетворяют условиям.

    :param pairs: Список пар игроков
    :return: Список отфильтрованных пар
    """
    filtered_pairs = []
    for player1, player2 in pairs:
        if player1.score == 0 and player1.in_game_score <= 3 and player2.score == 0 and player2.in_game_score <= 3:
            filtered_pairs.append((player1, player2))
    return filtered_pairs


def save_event_id_to_file(event_id, filename="event_ids.txt"):
    """
    Сохраняет event_id в файл, если его там еще нет.

    :param event_id: Список event_id для сохранения.
    :param filename: Имя файла для сохранения.
    """
    # Проверяем, существует ли файл
    if os.path.exists(filename):
        with open(filename, "r") as file:
            existing_ids = file.read().splitlines()
    else:
        existing_ids = []

    # Открываем файл для добавления новых уникальных ID
    with open(filename, "a") as file:
        for id in event_id:
            file.write(id + "\n")

def load_event_id_from_file(filename="event_ids.txt"):
    """
    Загружает event_id из файла.

    :param filename: Имя файла для загрузки.
    :return: Список уникальных event_id.
    """
    if os.path.exists(filename):
        with open(filename, "r") as file:
            return file.read().splitlines()
    return []



if __name__ == '__main__':
    def start():
        event_id = get_event_id()
        name_player = get_name_player(event_id)
        scope_list = get_score_by_game(event_id)
        scope_list_game = get_score_in_game(event_id)
        coefficient_list,  coeff_obj = get_coefficient(event_id)
        return event_id, name_player, scope_list, scope_list_game, coefficient_list, coeff_obj



    def gogo():
        time.sleep(5)
        driver.refresh()
        time.sleep(5)
        event_id, name_player, scope_list, scope_list_game, coefficient_list, coeff_obj = start()

        new_event_id = []
        for i in event_id:
            new_event_id.append(i)
            new_event_id.append(i)


        # Создаем словарь для хранения объектов Player
        players = {}

        # Создаем объекты Player и добавляем их в словарь
        for i in range(len(name_player)):
            # Преобразуем имя игрока в строку
            player_name = str(name_player[i])
            player = Player(player_name, new_event_id[i], scope_list[i], scope_list_game[i], coefficient_list[i], coeff_obj[i])
            players[f'player_{i+1}'] = player



        # Пример вывода информации о созданных игроках
        # for key, player in players.items():
            # print({key}, {player})
        pairs = create_pairs(players)
        filter_p = filter_pairs(pairs)

        for pair in filter_p:
            print(f"Pair: {pair[0]} vs {pair[1]}")
            if pair[0].coefficient < pair[1].coefficient:
                pair[0].coeff_obj.click()
                print(f"Clicked on button for player: {pair[0].name}")
            else:
                pair[1].coeff_obj.click()
                print(f"Clicked on button for player: {pair[1].name}")
            time.sleep(5)
            break
        time.sleep(360)
        print(100)

    for _ in range(10):
        gogo()