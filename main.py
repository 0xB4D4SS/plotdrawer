import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from numpy import *


class Example(QWidget):

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
        self.setWindowTitle('Lab1')
        self.show()

    def onclick(self):
        formula = self.input.text()
        if (self.rbtn.isChecked()):
            x = linspace(-10.0, 10.0)
            y = x
            z = eval(formula)
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            ax.plot(x, y, z)

        else:
            step = 0.1
            x = arange(-10.0, 10.0, step)
            print(eval(formula))
            y = eval(formula)
            fig = plt.figure()
            plt.plot(x, y)

        plt.savefig('plot.png')
        plt.show()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())