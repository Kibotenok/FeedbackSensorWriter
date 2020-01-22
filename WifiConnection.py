# Created by Antropov N.A.
# Константы и функции для взаимодействия с Wi-Fi модулем.
# Данные принимаются в виде цепочки байтов, декодируемых в строку значений характеристик,
# разделенных специальным флагом
import socket

# Константы для работы с Wi-Fi
PERIOD = 5  # Дефолтное значение периода задержки передачи данных в секундах
PORT = 88  # Номер порта
IP_ADDRESS = "192.168.4.1"
DATA_FLAG = "/"  # Флаг начала значения следующей характеристики


def getConnection():
    """
    Функция получения связи с модулем
    
    Возвращает активный сокет
    """
    
    conn = socket.socket()
    conn.connect((IP_ADDRESS, PORT))

    return conn


def sendDelay(conn, delay=PERIOD):
    """
    Функция отправки модулю периода задержки передачи данных
    
    :param conn: активный сокет
    :param delay: время задержки передачи данных в секундах
    """
    
    delay = str(delay)
    conn.send(delay.encode('utf8'))


def getData(conn):
    """
    Функция получения данных с модуля Wi-Fi
    
    :param conn: активный сокет
    
    Возвращает список значений исследуемых характеристик
    """
    
    data_list = conn.recv(1024).decode('utf8')

    # Преобразование строки данных в список
    data_list = data_list.split(DATA_FLAG)

    return data_list
