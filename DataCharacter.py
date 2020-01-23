# Created by Antropov N.A.
# Основные константы и функции для настройки программы перед записью данных
import os

# Объекты исследования
TEMPERATURE_SYSTEM = "Температура"
TOUCH_SYSTEM = "Осязание"
PLACE_SYSTEM = "Положение"
TOUCH_SYSTEM_POWER = "Твердость/Мягкость"
TOUCH_SYSTEM_MOVE = "Гладкость/Шероховатость"

# Варианты исследуемых систем
PELTYE_SYSTEM = "Система с элементом Пельтье"
AKSELEROMETR_SYSTEM_FOR_TOUCH = "Система акселерометр/вибромотор"
VIBRATION_SYSTEM = "Система виброметр/вибромотор"
POWER_SYSTEM = "Система датчик давления/сервопривод"
AKSELEROMETR_SYSTEM_FOR_PLACE = "Система акселерометр/сервопривод"

# Характеристики для исследуемых систем
TIME_DELAY = "Время задержки"
VOLTAGE = "Напряжение с датчика"
RESISTANCE = "Сопротивление датчика"
WORK = "Работоспособность системы"
TIME_RATE = "Время нагрева элемента Пельтье"
TIME_RATE_1 = "Время охлаждения элемента Пельтье"
AKSELEROMETR_FOR_TOUCH = "Скорость скольжения"
AKSELEROMETR_FOR_PLACE = "Ускорение"
VIBROMOTOR = "Частота вращения мотора"
VIBROMETR = "Показание вибрации"
TOUCH_SENSOR = "Нагрузка"
SERVO = "Угол поворота на сервоприводе"

# Константы для сохранения данных
SAVE_DIR_FOR_DATA = "C:/Users/Kiten/Desktop/Praktika/results/"
FILE_NAME = "test"


# Список первоначальных систем
system_list = [TEMPERATURE_SYSTEM, TOUCH_SYSTEM, PLACE_SYSTEM]


def charactersPrint(final_system):
    """
    Функция выбора характеристик исследуемой системы
    
    :param final_sysytem: исследуемая система
    
    Возращает список характеристик
    """
    
    if final_system == PELTYE_SYSTEM:
        return [TIME_DELAY, TIME_RATE, TIME_RATE_1, WORK]
    elif final_system == AKSELEROMETR_SYSTEM_FOR_TOUCH:
        return [TIME_DELAY, AKSELEROMETR_SYSTEM_FOR_TOUCH, VIBROMOTOR, WORK]
    elif final_system == AKSELEROMETR_SYSTEM_FOR_PLACE:
        return [TIME_DELAY, AKSELEROMETR_FOR_PLACE, SERVO, WORK]
    elif final_system == VIBRATION_SYSTEM:
        return [TIME_DELAY, VIBROMOTOR, VIBROMETR, WORK]
    elif final_system == POWER_SYSTEM:
        return [TIME_DELAY, VOLTAGE, RESISTANCE, SERVO, WORK]


def getDir(folder, dir=SAVE_DIR_FOR_DATA):
    """
    Функция получения и создания директории для сохранения файлов
    
    :param folder: название папки,
    :param dir: директория сохранения
    
    Возвращает созданную директорию
    """
    
    created_dir = os.path.join(dir, folder)

    if not (os.path.isdir(created_dir)):
        os.makedirs(created_dir)

    return created_dir
