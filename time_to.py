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
