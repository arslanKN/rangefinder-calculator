import sys
import io


from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QGraphicsPixmapItem, QGraphicsView, QGraphicsScene
from PyQt6.QtWidgets import QGraphicsLineItem
from PyQt6.QtGui import QPixmap, QPainter, QColor
from PyQt6 import uic
from PyQt6.QtCore import Qt, QPointF


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('dg.ui', self)
        self.scene = QGraphicsScene()
        self.qp = QPainter()
        self.load_map.clicked.connect(self.loading_map)
        self.set_length_map.clicked.connect(self.create_lenght_map)
        self.set_line_map.clicked.connect(self.loading_map)
        self.setMouseTracking(True)
        self.flag_map_picture = False

        self.flag_lenght_map = False
        self.flag_create_lenght_map = False
        self.flag_click_lenght = False

        self.lenght_map_coord1 = []
        self.lenght_map_coord2 = []

    def loading_map(self):
        try:
            if self.flag_map_picture:
                self.scene.removeItem(self.picture_map_item)
            self.fname = QFileDialog.getOpenFileName(self, 'Выбрать изображение', '')[0]
            self.picture_map_item = QGraphicsPixmapItem(QPixmap(self.fname))
            self.scene.addItem(self.picture_map_item)
            self.picture_Map.setScene(self.scene)
            self.flag_map_picture = True
        except Exception:
            pass

    def create_lenght_map(self):
        self.flag_click_lenght = True

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.flag_click_lenght :
            self.lenght_map_coord1 = [event.pos().x(), event.pos().y()]
            self.draw()
            self.flag_click_lenght = True


    def draw(self):
        x1, y1 = self.lenght_map_coord1
        self.lenght_map_coord_point1 = QPointF(x1, y1)
        x2, y2 = self.lenght_map_coord2
        self.lenght_map_coord_point2 = QPointF(x2, y2)
        self.line = QGraphicsLineItem(self.lenght_map_coord_point1, self.lenght_map_coord_point2)
        self.line.setPen(Qt.GlobalColor.black)


    def mouseMoveEvent(self, event):
        if self.flag_click_lenght:
            self.lenght_map_coord2 = [event.pos().x(), event.pos().y()]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())

