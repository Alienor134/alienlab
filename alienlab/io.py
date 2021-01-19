
import os
import sys
from PyQt5 import QtWidgets, QtGui, QtCore

from PyQt5.QtCore import QPoint, QRect, QSize, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QRubberBand, QDialog
from PyQt5.QtGui import QIcon, QPixmap, QColor, QPainter, QPolygon, QImage

import numpy as np

cwd = os.getcwd()

def catch_file(direc = cwd ):
    """Opens a dialog window to select a file. Default directory: current directory
    direc [str]: directory to open (default: current directory)
    """
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QFileDialog
    fname = widget.getOpenFileName(None, directory=direc, caption = "Select a video file...",
                                                  filter="All files (*)")
    return fname[0]



class Window(QLabel):

    def __init__(self, parent = None):
    
        QLabel.__init__(self, parent)
        self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
        self.origin = QPoint()
        self.end = QPoint()
        self.title = 'Select the region of interest and close the window'
        self.setWindowTitle(self.title)
        
    def mousePressEvent(self, event):
    
        if event.button() == Qt.LeftButton:
        
            self.origin = QPoint(event.pos())
            self.rubberBand.setGeometry(QRect(self.origin, QSize()))
            self.rubberBand.show()
    
    def mouseMoveEvent(self, event):
    
        if not self.origin.isNull():
            self.rubberBand.setGeometry(QRect(self.origin, event.pos()).normalized())
    
    def mouseReleaseEvent(self, event):
    
        if event.button() == Qt.LeftButton:
            #self.rubberBand.hide()
            self.end = QPoint(event.pos())

def get_qimage(image: np.ndarray):
    assert (np.max(image) <= 255)
    image8 = image.astype(np.uint8, order='C', casting='unsafe')
    height, width, colors = image8.shape
    bytesPerLine = 3 * width

    image = QImage(image8.data, width, height, bytesPerLine,
                       QImage.Format_RGB888)

    image = image.rgbSwapped()
    return image

def select_roi(im):
    app = QApplication(sys.argv)

    window = Window()
    window.setGeometry(0,0, 50, 50)
    pixmap = QPixmap.fromImage(get_qimage(im))
    window.setPixmap(pixmap)
    window.resize(pixmap.width(), pixmap.height())
    window.show()

    app.exec_()
    return [(window.origin.x(), window.end.x()),(window.origin.y(), window.end.y())]

