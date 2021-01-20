import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from numpy import *


class GUI(QWidget):

    def __init__(self):
        super().__init__()

        self.btn = QPushButton('Draw plot', self)
        self.rbtn = QRadioButton("draw in 3d", self)
        self.picture = QPixmap('plot.png')
        self.label = QLabel('Input expression:', self)
        self.input = QLineEdit('', self)

        self.initui()

    def initui(self):

        self.btn.move(50, 100)
        self.btn.clicked.connect(self.onclick)

        self.rbtn.move(50, 140)

        self.label.move(50, 30)

        self.input.resize(100, 30)
        self.input.move(50, 50)

        self.setGeometry(100, 100, 200, 200)
        self.setWindowTitle('Plotdrawer')
        self.show()

    def onclick(self):
        formula = self.input.text()
        if self.rbtn.isChecked():
            x = linspace(-2*pi, 2*pi, 1000)
            y = x
            x, y = meshgrid(x, y)
            print(eval(formula))
            z = eval(formula)
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            ax.plot_wireframe(x, y, z)
            ax.set_xlim3d(-2*pi, 2*pi)
            ax.set_ylim3d(-2*pi, 2*pi)
            #should set zlim when plot has break points
            ax.set_zlim(-5, 5)

        else:
            x = linspace(-2*pi, 2*pi, 1000)
            print(eval(formula))
            y = eval(formula)
            fig = plt.figure()
            plt.plot(x, y)
            plt.ylim(-5, 5)

        plt.grid()
        plt.show()
        plt.savefig('plot.png')


if __name__ == '__main__':

    app = QApplication(sys.argv)
    gui = GUI()
    sys.exit(app.exec_())