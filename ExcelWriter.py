# Created by Antropov N.A.
# Константы и функции для записи полученных данных в таблицу Excel для последующего анализа
import xlwt

# Константы для работы с Excel
DATA_FONT = "Times New Roman"  # Стиль шрифта записываемых данных

# Заголовки справочных данных
TEST_NUMBER = "Номер теста"
TIME = "Время начала теста"
DATE = "Дата"
DELAY = "Время задержки передачи данных"


def chooseFontSettings(headline):
    """
    Функция настройки шрифта
    
    :param headline: флаг заголовка
    
    Возвращает формат шрифта
    """
    
    font = xlwt.Font()
    font.name = DATA_FONT  # Выбор стиля шрифта
    font.bold = headline

    return font


def chooseStyleSettings(headline=False):
    """
    Функция настройки стиля ячейки
    
    :param headline: флаг заголовка
    
    Возвращает стиль ячейки
    """
    
    style = xlwt.XFStyle()

    # Позиционирование данных в ячейке
    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_CENTER
    style.alignment = alignment

    style.font = chooseFontSettings(headline)

    return style


def headlineWriter(num, date, time, line_count, character_list, worksheet, delay, headline=True):
    """
    Функция записи заголовков
    
    :param num: номер теста
    :param date: дата проведения теста
    :param time: время начала теста
    :param line_count: счетчик строк таблицы
    :param character_list: список измеряемых характеристик
    :param worksheet: объект для записи данных
    :param delay: время задержки передачи данных в секундах
    :param headline: флаг заголовка
    
    Возвращает счетчик строк таблицы
    """
    
    char_count = 4 # кол-во столбцов со справочной информацией
    i = 0

    # Задание стилей ячеек
    style = chooseStyleSettings(headline)
    style1 = chooseStyleSettings(headline=False)

    # Запись заголовков
    worksheet.write(line_count, 0, TEST_NUMBER, style)
    worksheet.write(line_count, 1, DATE, style)
    worksheet.write(line_count, 2, TIME, style)
    worksheet.write(line_count, 3, DELAY, style)

    for character in character_list:
        worksheet.write(line_count, char_count+i, character, style)
        i += 1

    line_count += 1

    # Запись справочных данных
    worksheet.write(line_count, 0, num, style1)
    worksheet.write(line_count, 1, date, style1)
    worksheet.write(line_count, 2, time, style1)
    worksheet.write(line_count, 3, delay, style1)

    return line_count


def oneStringWriter(data, line_count, worksheet):
    """
    Функция записи строки данных
    
    :param data: полученные данные
    :param line_count: счетчик строк таблицы
    :param worksheet: объект для записи данных
    
    Возвращает номер текущей строки таблицы
    """
    
    # Задание стиля ячеек
    style = chooseStyleSettings()

    i = 0
    char_count = 4

    # Запись полученных данных
    for character in data:
        worksheet.write(line_count, char_count+i, character, style)
        i += 1

    line_count += 1

    return line_count


def saveData(workbook, dir):
    """
    Функция сохранения данных
    
    :param workbook: объект таблицы Excel с записанными данными
    :param dir: директория сохранения файла
    """
    
    workbook.save(dir)
