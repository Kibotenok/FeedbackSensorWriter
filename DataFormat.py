# Created by Antropov N.A.
from PyQt5 import QtCore


class DataFormat:
    """Задает формат данных, получаемых от исследуемой системы"""
    
    def __init__(self, test_number=0, file_name="test0.xls", sensitivity='2',
                 **kwargs):
        
        self.test_number = test_number  # Номер теста
        self.file_name = file_name  # Имя файла
        self.sensitivity = sensitivity  # Проверка работоспособности исследуемого метода
        self.getDateTime()
        super().__init__(**kwargs)  # Инициализация дополнительных аргументов

    def getDateTime(self):
        """Получение даты и времени начала теста"""
        
        # Получение даты
        self.date = QtCore.QDate.currentDate()
        self.date = self.date.toString(QtCore.Qt.ISODate)

        # Получение времени
        self.time = QtCore.QTime.currentTime()
        self.time = self.time.toString(QtCore.Qt.DefaultLocaleLongDate)
