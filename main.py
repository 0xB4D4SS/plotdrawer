import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from numpy import *


class GUI(QWidget):

    def __init__(self):
        # инициализация элементов интерфейса
        super().__init__()

        self.btn = QPushButton('Draw plot', self)
        self.rbtn = QRadioButton("draw in 3d", self)
        self.picture = QPixmap('plot.png')
        self.label = QLabel('Input expression:', self)
        self.finput = QLineEdit('', self)

        self.initui()

    def initui(self):
        # отрисовка элементов интерфейса
        self.btn.move(50, 100)
        self.btn.clicked.connect(self.onclick)

        self.rbtn.move(50, 140)

        self.label.move(50, 30)

        self.finput.resize(100, 30)
        self.finput.move(50, 50)

        self.setGeometry(100, 100, 200, 200)
        self.setWindowTitle('Plotdrawer')
        self.show()

    def onclick(self):
        # получаем текст функции для отрисовки
        formula = self.finput.text()
        # 3d случай
        if self.rbtn.isChecked():
            # задаем функцию неявно (z = f(x,y)) с помощью лямбда выражения
            f = lambda x, y: eval(formula)
            # задаем диапазоны x и y
            xval = linspace(-2*pi, 2*pi, 500)
            yval = linspace(-2*pi, 2*pi, 500)
            x, y = meshgrid(xval, yval)
            # дебажный вывод в консоль
            print(eval(formula))
            z = f(x, y)
            # собсна создаем график
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            ax.plot_surface(x, y, z, cmap=cm.coolwarm, cstride=30, rstride=30)
            # границы отрисовки графика
            # ((y^2)/x до сих пор странно рисуется, в остальном работает)
            ax.set_zlim(-30, 30)
        # 2d случай
        else:
            # выражаем y как функцию от x с помощью лямбда-выражения
            y = lambda x: eval(formula)
            # задаем диапазон x
            x = linspace(-2*pi, 2*pi, 1000)
            # дебажный вывод в консоль
            print(eval(formula))
            # собсна создаем график
            fig = plt.figure()
            plt.plot(x, y(x))
            plt.ylim(-5, 5)

        plt.grid()
        plt.show()
        plt.savefig('plot.png')


if __name__ == '__main__':
    # здесь запускается приложение
    app = QApplication(sys.argv)
    gui = GUI()
    sys.exit(app.exec_())