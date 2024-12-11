import sys
import io
from traceback import print_tb

from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt6.QtGui import QPixmap, QPainter, QColor, QPen, QMouseEvent
from PyQt6 import uic
from PyQt6.QtCore import Qt
from calculations import distance_calculation


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('dg.ui', self)  # загружаем дизайн
        #
        self.load_map.clicked.connect(self.loading_map)
        #
        self.lenght_map.textChanged.connect(self.update_line_map)
        # кнопки для записывания результатов попаданий
        self.button_target_destroyed.clicked.connect(self.record_hit)
        self.button_hit.clicked.connect(self.record_hit)
        self.button_miss.clicked.connect(self.record_hit)
        # кнопки рисований линий
        self.set_length_map.clicked.connect(self.create_lenght_map)
        self.set_line_map.clicked.connect(self.create_line_map)

        # флаги для рисования
        self.flag_map_picture = False
        self.flag_create_lenght_map = False
        self.flag_create_line_map = False

        self.status_click_lenght = False
        self.status_click_line = False

        self.flag_mousemove = True

    def loading_map(self):  # загрузка изображения
        fname = QFileDialog.getOpenFileName(self, "Выбрать изображение", "",
                                            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif);;Все файлы (*)",
                                            )[0]
        self.pixmap_fname = QPixmap(fname)
        self.pixmap_fname = self.pixmap_fname.scaled(931, 621, Qt.AspectRatioMode.KeepAspectRatio)
        self.flag_map_picture = True

    def create_lenght_map(self):
        self.status_click_lenght = True

    def create_line_map(self):
        self.status_click_line = True

    def paintEvent(self, event):
        if self.flag_map_picture:  # рисование изображения
            self.qp_map = QPainter(self)
            self.qp_map.drawPixmap(0, 0, self.pixmap_fname)
            self.qp_map.end()

        if self.flag_create_lenght_map:  # вызов рисования линии размера карты
            self.qp_lenght = QPainter(self)
            self.qp_lenght.begin(self)
            self.draw_lenght()
            self.qp_lenght.end()

        if self.flag_create_line_map:  # вызов рисования дистанции
            self.qp_line = QPainter(self)
            self.qp_line.begin(self)
            self.draw_line()
            self.qp_line.end()

    def drawf(self):
        if self.status_click_lenght:
            self.flag_create_lenght_map = True
        if self.status_click_line:
            self.flag_create_line_map = True

    def draw_lenght(self):  # рисование линии размера карты
        x1, y1 = self.lenght_map_coord1
        x2, y2 = self.lenght_map_coord2
        pen = QPen(Qt.GlobalColor.black, 4)
        self.qp_lenght.setPen(pen)
        self.qp_lenght.drawLine(x1, y1, x2, y2)

    def draw_line(self):  # рисование дистанции
        x1, y1 = self.line_map_coord1
        x2, y2 = self.line_map_coord2
        pen = QPen(Qt.GlobalColor.red, 4)
        self.qp_line.setPen(pen)
        self.qp_line.drawLine(x1, y1, x2, y2)

    def mouseReleaseEvent(self, event):
        if self.status_click_lenght and event.button() == Qt.MouseButton.LeftButton:  # для линии размера карты
            self.lenght_map_coord2 = [event.pos().x(), event.pos().y()]
            self.drawf()
            self.update()
            self.status_click_lenght = False
            self.flag_mousemove = True

        if self.status_click_line and event.button() == Qt.MouseButton.LeftButton:  # для дистанции
            self.line_map_coord2 = [event.pos().x(), event.pos().y()]
            self.drawf()
            self.update()
            self.status_click_line = False
            self.flag_mousemove = True

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.status_click_lenght and self.flag_mousemove:
            self.lenght_map_coord1 = [event.pos().x(), event.pos().y()]
            self.flag_mousemove = False

        if self.status_click_lenght:
            self.lenght_map_coord2 = [event.pos().x(), event.pos().y()]
            self.update()
            self.drawf()

        if self.status_click_line and self.flag_mousemove:
            self.line_map_coord1 = [event.pos().x(), event.pos().y()]
            self.flag_mousemove = False

        if self.status_click_line:
            self.line_map_coord2 = [event.pos().x(), event.pos().y()]
            self.update()
            self.drawf()
            self.update_line_map()

    def update_line_map(self):  # вывод расстояние до цели
        try:
            self.lenght_map_distance = int(self.lenght_map.toPlainText())
            self.line_map_distance = int(distance_calculation(self.lenght_map_coord1,
                                                              self.lenght_map_coord2, self.line_map_coord1,
                                                              self.line_map_coord2, self.lenght_map_distance))
            self.line_map.setText(f'{self.line_map_distance}')
        except Exception:
            self.line_map.setText('')

    def record_hit(self):  # добавление результатов выстрелов
        if self.sender() == self.button_target_destroyed:
            pass
        if self.sender() == self.button_miss:
            pass
        if self.sender() == self.button_hit:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
