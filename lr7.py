import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel
from PyQt5.QtGui import QPixmap, QImage
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QHBoxLayout
import math
from PIL import Image
from PIL import Image, ImageDraw
import numpy as np

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setStyleSheet("background-color: white;")

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Лабораторная 7')
        
        self.left_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()
        
        self.open_button = QPushButton('Открыть изображение')
        self.open_button.clicked.connect(self.open_image)
        
        self.image_label = QLabel()
        
        self.plot_button = QPushButton('Создать график')
        self.plot_button.clicked.connect(self.create_plot)
        
        self.save_button = QPushButton('Сохранить график')
        self.save_button.clicked.connect(self.save_plot)
        
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        
        self.left_layout.addWidget(self.open_button)
        self.left_layout.addWidget(self.image_label)
        
        self.right_layout.addWidget(self.plot_button)
        self.right_layout.addWidget(self.save_button)
        self.right_layout.addWidget(self.canvas)
        
        main_layout = QHBoxLayout()
        main_layout.addLayout(self.left_layout)
        main_layout.addLayout(self.right_layout)

        self.open_button.setStyleSheet("background-color: gray;")
        self.plot_button.setStyleSheet("background-color: gray;")
        self.save_button.setStyleSheet("background-color: gray;")
        
        self.setLayout(main_layout)
    
    def save_plot(self):
        file_name, _ = QFileDialog.getSaveFileName(self, 'Сохранить график', 
                                                   '', 
                                                   'Images (*.png *.jpg *.bmp)')
        if file_name:
            self.figure.savefig(file_name)

    def open_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Открыть изображение', 
                                                   '', 
                                                   'Images (*.png *.xpm *.jpg *.bmp)')
        if file_name:
            pixmap = QPixmap(file_name)
            self.image_label.setPixmap(pixmap)

    def create_plot(self):
        x = range(-10, 10)
        y = [i**2 for i in x]
    
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(x, y)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.grid(True)
        image_path = self.image_label.pixmap().toImage().save('image.png')
        img = Image.open('image.png')
        width, height = img.size

        mask = Image.new('L', (width, height), 0)
        draw = ImageDraw.Draw(mask)
        
        draw.ellipse((width // 2, height // 3, width // 2 + width // 3, height // 2 + height // 3), fill=255)   
    
        img = img.convert('RGBA')
        img.putalpha(mask)
        img = img.crop((width // 2, height // 3, width // 2 + width // 3, height // 2 + height // 3))
        
        arr = np.array(img)
        image = OffsetImage(arr, zoom=0.5)
        ab = AnnotationBbox(image, (7.5, 50), frameon=False)
        ax.add_artist(ab)
        
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())