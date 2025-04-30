import sys
import pandas as pd
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QListWidget, QGraphicsView, 
    QGraphicsScene, QPushButton, QVBoxLayout, QHBoxLayout, 
    QWidget, QFileDialog, QMessageBox
)
from PyQt6.QtCore import Qt, QRectF, QMimeData
from PyQt6.QtGui import QBrush, QColor, QDrag

class WagonApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RailSeat Pro")
        self.setGeometry(100, 100, 1000, 700)
        
        # Данные
        self.passengers = []
        self.wagon_type = "плацкарт"  # или "купе"
        
        # GUI
        self.setup_ui()
        
    def setup_ui(self):
        # Главный виджет и лейауты
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Левая панель (пассажиры)
        left_panel = QVBoxLayout()
        
        self.passenger_list = QListWidget()
        self.passenger_list.setDragEnabled(True)
        left_panel.addWidget(self.passenger_list)
        
        # Кнопки
        self.btn_load = QPushButton("Загрузить пассажиров (CSV)")
        self.btn_load.clicked.connect(self.load_passengers)
        left_panel.addWidget(self.btn_load)
        
        self.btn_auto = QPushButton("Авторассадка")
        self.btn_auto.clicked.connect(self.auto_assign)
        left_panel.addWidget(self.btn_auto)
        
        self.btn_save = QPushButton("Сохранить схему (Excel)")
        self.btn_save.clicked.connect(self.save_to_excel)
        left_panel.addWidget(self.btn_save)
        
        # Правая панель (вагон)
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setAcceptDrops(True)
        
        # Генерация схемы вагона
        self.generate_wagon()
        
        # Добавляем панели в главный лейаут
        main_layout.addLayout(left_panel, 30)
        main_layout.addWidget(self.view, 70)
    
    def generate_wagon(self):
        """Создает схему вагона в зависимости от типа."""
        self.scene.clear()
        self.seats = []
        
        if self.wagon_type == "плацкарт":
            seats_count = 54
            rows = 9
        else:  # купе
            seats_count = 36
            rows = 6
            
        for i in range(1, seats_count + 1):
            row = (i - 1) // (seats_count // rows)
            col = (i - 1) % (seats_count // rows)
            
            seat = self.scene.addRect(
                col * 60 + 10, row * 60 + 10, 50, 50,
                brush=QBrush(QColor("lightblue")))
            seat.setData(0, i)  # Номер места
            seat.setData(1, "нижнее" if i % 2 == 1 else "верхнее")  # Тип
            seat.setData(2, None)  # Пассажир
            
            self.scene.addSimpleText(f"{i}").setPos(col * 60 + 30, row * 60 + 30)
            self.seats.append(seat)
    
    def load_passengers(self):
        """Загружает список пассажиров из CSV."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите файл", "", "CSV (*.csv);;Excel (*.xlsx)")
        
        if file_path:
            try:
                df = pd.read_csv(file_path) if file_path.endswith('.csv') else pd.read_excel(file_path)
                self.passengers = df.iloc[:, 0].tolist()  # Первый столбец = ФИО
                self.passenger_list.clear()
                self.passenger_list.addItems(self.passengers)
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить файл:\n{str(e)}")
    
    def auto_assign(self):
        """Автоматическая рассадка по правилам."""
        if not self.passengers:
            QMessageBox.warning(self, "Ошибка", "Сначала загрузите пассажиров!")
            return
            
        # Сначала нижние места
        lower_seats = [s for s in self.seats if s.data(1) == "нижнее"]
        upper_seats = [s for s in self.seats if s.data(1) == "верхнее"]
        
        for i, passenger in enumerate(self.passengers):
            seat = None
            if i < len(lower_seats):
                seat = lower_seats[i]
            elif i < len(lower_seats) + len(upper_seats):
                seat = upper_seats[i - len(lower_seats)]
                
            if seat:
                seat.setBrush(QBrush(QColor("pink")))
                seat.setData(2, passenger)
                seat.setToolTip(f"{seat.data(0)}: {passenger}")
    
    def save_to_excel(self):
        """Сохраняет схему в Excel."""
        data = []
        for seat in self.seats:
            data.append({
                "Место": seat.data(0),
                "Тип": seat.data(1),
                "Пассажир": seat.data(2) or "Свободно"
            })
            
        df = pd.DataFrame(data)
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Сохранить как", "рассадка.xlsx", "Excel (*.xlsx)")
        
        if file_path:
            df.to_excel(file_path, index=False)
            QMessageBox.information(self, "Успех", "Файл сохранен!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WagonApp()
    window.show()
    sys.exit(app.exec())