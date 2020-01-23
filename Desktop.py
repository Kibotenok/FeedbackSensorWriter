# Created by Antropov N.A.
# Основной скрипт с интерфейсом и логикой программы.
import sys
import threading
from PyQt5.QtWidgets import (QApplication, QPushButton, QMessageBox, QGridLayout,
                             QLabel, QLineEdit, QWidget, QComboBox)
from PyQt5 import QtGui
import xlwt

import DataCharacter
import DataFormat
import WifiConnection
import ExcelWriter


class ThirdWindow(QWidget):
    """
    Окно записи данных в таблицу Excel.
    Прием и запись происходят в отдельном потоке
    """
    
    def __init__(self, system, test_number, delay, conn, characters_list):
        super().__init__()
        self.system = system  # Название исследуемой системы
        self.test_number = test_number  # Номер теста
        self.delay = delay  # Время задержки передачи данных в секундах
        self.conn = conn  # Активный сокет
        self.headline_write = True  # Флаг записи заголовков в файл
        self.characters_list = characters_list  # Список названий характеристик выбранной системы
        self.line_count = 0  # Счетчик строк таблицы для записи в Excel
        self.initUI()

    def initUI(self):
        # Выбор иконки программы
        self.setWindowIcon(QtGui.QIcon('C:/Users/Kiten/Desktop/Praktika/icon/hand.jpg'))

        # Получение директории для сохранения
        self.dir = DataCharacter.getDir(self.system)

        # Кнопка остановки записи
        stop_button = QPushButton("Стоп", self)
        stop_button.setMinimumSize(1, 30)

        # Кнопки для выбора результатов работы
        yes_button = QPushButton("Да", self)
        no_button = QPushButton("Нет", self)

        # Разметка окна
        grid = QGridLayout()
        grid.setSpacing(4)
        grid.addWidget(stop_button, 1, 0, 1, 1)
        grid.addWidget(yes_button, 2, 0)
        grid.addWidget(no_button, 2, 1)

        self.setLayout(grid)

        # Создание объекта таблицы Excel
        self.workbook = xlwt.Workbook()
        self.worksheet = self.workbook.add_sheet("Data")

        # Создание объекта данных
        self.data = DataFormat.DataFormat()
        self.data.test_number = self.test_number  # Номер теста
        self.data.delay = self.delay  # Время задержки передачи данных в секундах
        self.data.file_name = self.directory + "/test" + self.test_number + ".xls"  # Путь для сохранения файла
        self.data.characters_list = self.characters_list  # Список названий характеристик

        # Слушатели событий для кнопок
        yes_button.clicked.connect(self.onClickYes)
        no_button.clicked.connect(self.onClickNo)
        stop_button.clicked.connect(self.onClick)

        # Запись заголовков
        if self.headline_write:
            self.line_count = ExcelWriter.headlineWriter(self.data.test_number, self.data.date, self.data.time,
                                                           self.line_count, self.data.characters_list, self.worksheet,
                                                           self.data.delay)
            self.headline_write = False

        # Старт потока с приемом и записью данных
        self.startWriter()

        # Настройки окна
        self.setWindowTitle("Запись")
        self.setFixedSize(300, 300)

    def startWriter(self):
        """Инициализация потока приема и передачи данных"""
        
        self.timer_started = True

        # Создаем и запускаем отдельный поток
        self.th1 = threading.Thread(target=self.WriteLoop)
        self.th1.start()

    def WriteLoop(self):
        """Прием и передача данных"""
        
        while (self.timer_started == True):

            # Получение данных
            self.charecters_data = WifiConnection.getData(self.conn)
            self.charecters_data.append(self.data.sensitivity)

            # Запись полученных данных
            self.line_count = ExcelWriter.oneStringWriter(self.charecters_data, self.line_count, self.worksheet)

    def StopWrite(self):
        """Остановка потока записи"""
        
        self.timer_started = False

    def onClick(self):
        """Обработчик нажатия кнопки СТОП"""
        
        self.StopWrite()
        # Разблокировка второго окна
        second_window.setEnabled(True)
        # Сохранение данных
        ExcelWriter.saveData(self.workbook, self.data.file_name)
        # Закрытие текущего окна
        third_window.close()

    def onClickYes(self):
        """Обработчик нажатия кнопки ДА"""
        
        self.data.sensitivity = '1'

    def onClickNo(self):
        """Обработчик нажатия кнопки НЕТ"""
        
        self.data.sensitivity = '0'


class SecondWindow(QWidget):
    """
    Окно настройки параметров для записи данных.
    """
    
    def __init__(self, system):
        super().__init__()
        self.system = system  # Название выбранной системы
        self.number_input = False  # Флаг заполнения строки с номером теста
        self.delay_input = False  # Флаг заполнения строки с периодичностью приема сигнала
        self.initUI()

    def initUI(self):
        # Выбор иконки программы
        self.setWindowIcon(QtGui.QIcon('C:/Users/Kiten/Desktop/Praktika/icon/hand.jpg'))

        # Заголовки для настраиваемых параметров
        system = QLabel(self.system, self)
        text_number = QLabel("Номер теста", self)
        delay = QLabel("Время задержки передачи данных, сек", self)
        character = QLabel("Характеристики:", self)

        # Получение списка названий характеристик для выбранной системы
        self.characters_list = DataCharacter.charactersPrint(self.system)

        # Создание списка для вывода названий характеристик
        character_text = []

        for characters in self.characters_list:
            character_line = QLineEdit(self)
            character_line.setText(characters)
            character_line.setEnabled(False)
            character_text.append(character_line)

        # Создание редактируемых строк
        number = QLineEdit(self)
        delay_text = QLineEdit(self)

        # Кнопка старта записи
        self.start_button = QPushButton("Старт", self)

        # Разметка окна
        i = 2
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(system, 1, 0)
        grid.addWidget(text_number, 2, 0)
        grid.addWidget(number, 3, 0)
        grid.addWidget(step, 4, 0)
        grid.addWidget(step_text, 5, 0)
        grid.addWidget(character, 1, 1)
        
        for ch in character_text:
            grid.addWidget(ch, i, 1)
            i += 1
        grid.addWidget(self.start_button, i, 1)

        self.setLayout(grid)

        # Слушатели событий для редактируемых строк
        number.textChanged[str].connect(self.onChanged1)
        delay_text.textChanged[str].connect(self.onChanged2)

        # Активация кнопки старта записи
        # if self.number_input and self.step_input:
        #    start_button.setEnabled(True)

        # Слушатель событий для кнопки старта записи
        self.start_button.clicked.connect(self.onClick)

        # Настройки окна
        self.setWindowTitle("Настройки")
        self.setFixedSize(500, 500)

    def onChanged1(self, text):
        """Обработчик событий для строки с номером теста"""
        
        self.test_number = text

    def onChanged2(self, text):
        """Обработчик событий для строки с временем задержки передачи данных"""
        
        self.delay = text

    def onClick(self):
        """Обработчик событий при нажатии кнопки старта записи"""
        
        # Создание сокета и подключение к модулю Wi-Fi
        self.conn = WifiConnection.getConnection()

        # Отправка на модуль времени задержки передачи данных
        WifiConnection.sendDelay(self.conn, self.delay)

        # Блокировка текущего окна
        second_window.setEnabled(False)

        # Вызов окна записи
        global third_window
        third_window = ThirdWindow(self.system, self.test_number, self.delay, self.conn, self.characters_list)
        third_window.show()

    def closeEvent(self, event):
        """Обраотчик событий при закрытии окна"""
        
        reply = QMessageBox.question(self, 'Выход',
                                     "Закрыть программу?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


class MainWindow(QWidget):
    """
    Основное окно выбора исследуемой системы
    """
    
    def __init__(self):
        super().__init__()
        self.show_window = False  # Флаг активации кнопки перехода к следующему окну
        self.initUI()

    def initUI(self):
        # Выбор иконки программы
        self.setWindowIcon(QtGui.QIcon('C:/Users/Kiten/Desktop/Praktika/icon/hand.jpg'))

        # Заголовок
        label = QLabel("Выбор системы", self)

        # Выпадающие списки с вариантами систем
        list = QComboBox(self)
        self.list2 = QComboBox(self)
        self.list3 = QComboBox(self)

        # Выбор минимального размера окон со списками
        list.setMinimumSize(1, 30)
        self.list2.setMinimumSize(1, 30)
        self.list3.setMinimumSize(1, 30)

        # Оглашение первого списка
        list.addItems([DataСharacter.TEMPERATURE_SYSTEM, DataCharacter.TOUCH_SYSTEM,
                       DataCharacter.PLACE_SYSTEM])

        # Слушатели событий для списков
        list.activated[str].connect(self.firstlistActivate)
        self.list2.activated[str].connect(self.secondlistActivate)
        self.list3.activated[str].connect(self.thirdlistActivate)

        # Создание кнопки перехода в другое окно
        self.ok_button = QPushButton("Ок", self)
        self.ok_button.setEnabled(False)
        self.ok_button.clicked.connect(self.onClick)

        # Разметка окна
        grid = QGridLayout()
        grid.setSpacing(5)
        grid.addWidget(label, 1, 0)
        grid.addWidget(list, 2, 0)
        grid.addWidget(self.list2, 3, 0)
        grid.addWidget(self.list3, 4, 0)
        grid.addWidget(self.ok_button, 5, 0)

        self.setLayout(grid)

        # Настройки окна
        self.setWindowTitle("Системы")
        self.setFixedSize(300, 300)
        self.show()

    def firstlistActivate(self, text):
        """Обработчик событий для первого списка.
           Происходит оглашение второго списка
        """
        
        if text == DataCharacter.TEMPERATURE_SYSTEM:
            self.list2.addItems([DataCharacter.PELTYE_SYSTEM])
        elif text == DataCharacter.TOUCH_SYSTEM:
            self.list2.addItems([DataCharacter.TOUCH_SYSTEM_POWER, DataCharacter.TOUCH_SYSTEM_MOVE])
        elif text == DataCharacter.PLACE_SYSTEM:
            self.list2.addItems([DataCharacter.AKSELEROMETR_SYSTEM_FOR_PLACE])

    def onClick(self):
        """Обработчик событий для кнопки OK"""
        
        # Вызов ворого окна. В качестве аргумента передаается название системы
        global second_window
        second_window = SecondWindow(self.system)
        second_window.show()

        # Закрытие текущего окна
        main_window.close()
        
    def secondlistActivate(self, text):
        """
        Обработчик событий для второго списка.
        Происходит оглашение третьего списка
        """
        
        if text == DataCharacter.PELTYE_SYSTEM:
            self.list3.addItems(['-'])
        elif text == DataCharacter.TOUCH_SYSTEM_POWER:
            self.list3.addItems([DataCharacter.POWER_SYSTEM])
        elif text == DataCharacter.TOUCH_SYSTEM_MOVE:
            self.list3.addItems([DataCharacter.AKSELEROMETR_SYSTEM_FOR_TOUCH, DataCharacter.VIBRATION_SYSTEM])
        elif text == DataCharacter.AKSELEROMETR_SYSTEM_FOR_PLACE:
            self.list3.addItems(['-'])

        self.system = text

    def thirdlistActivate(self, text):
        """
        Обработчик событий для второго списка.
        Происходит активация кнопки
        """
        
        if not(text == '-'):
            self.system = text
        self.ok_button.setEnabled(True)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())
