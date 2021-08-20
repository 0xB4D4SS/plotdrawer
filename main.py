import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QRadioButton, QLabel, QLineEdit
from PyQt5.QtGui import QPixmap
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from numpy import *
from sympy import limit, sympify, symbols


class GUI(QWidget):

    def __init__(self):
        # инициализация элементов интерфейса
        super().__init__()

        self.btn = QPushButton('Draw plot', self)
        self.rbtn = QRadioButton("draw in 3d", self)
        self.picture = QPixmap('plot.png')
        self.label = QLabel('Input expression:', self)
        self.infolabel = QLabel('** - возведение в степень', self)
        self.finput = QLineEdit('', self)

        self.initui()

    def initui(self):
        # отрисовка элементов интерфейса
        self.btn.move(50, 100)
        self.btn.clicked.connect(self.onclick)

        self.rbtn.move(50, 140)

        self.label.move(50, 30)
        self.infolabel.move(20, 170)

        self.finput.resize(100, 30)
        self.finput.move(50, 50)

        self.setGeometry(100, 100, 200, 200)
        self.setWindowTitle('Plotdrawer')
        self.show()

    def onclick(self):
        # шаг значений
        step = 0.1
        # получаем текст функции для отрисовки
        formula = self.finput.text()
        # 3d случай
        if self.rbtn.isChecked():
            # задаем диапазоны x и y
            xval = arange(-6.0, 6.0, step)
            yval = arange(-6.0, 6.0, step)
            x, y = meshgrid(xval, yval)
            # задаем функцию неявно (z = f(x,y)) с помощью лямбда-выражения
            f = lambda x, y: eval(formula)
            z = f(x, y)
            # дебажный вывод в консоль
            # print(eval(formula))
            # собсна создаем график
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            ax.plot_surface(x, y, z, cstride=10, rstride=10)
            # границы отрисовки графика
            # ((y^2)/x до сих пор странно рисуется, в остальном работает)
            ax.set_zlim(-30, 30)
        # 2d случай
        else:
            # задаем диапазон x
            xval = arange(-6.0, 6.0, step)
            # выражаем y как функцию от x с помощью лямбда-выражения
            y = lambda x: eval(formula)
            # проверяем функцию на точки разрыва:
            # проверяем равенство пределов и значения функции в точке и проверяем нет ли скачка предела в точке
            # если пределы равны или скачка нет - точки разрыва нет, иначе есть
            try:
                k = -1
                for val in xval:
                    k = k+1
                    x = symbols('x')
                    lim1 = limit(sympify(formula), x, val, dir='-').evalf()
                    lim2 = limit(sympify(formula), x, val, dir='+').evalf()
                    limnext = limit(sympify(formula), x, val-step, dir='+').evalf()
                    if not(lim1-lim2 < step) or not(lim1 - y(val) < step) or not(lim2 - y(val) < step):
                        xval[k] = nan
                    elif diff([lim2, limnext]) > 20.0:
                        xval[k] = nan
            except:
                pass
            # дебажный вывод в консоль
            # print(eval(formula))
            # собсна создаем график
            fig = plt.figure()
            plt.plot(xval, y(xval))
            # пределы отрисовки оси y
            plt.ylim(-5, 5)
        # показываем график юзеру
        plt.grid()
        plt.show()
        # сохраняем картинку графика
        plt.savefig('plot.png')


if __name__ == '__main__':
    # здесь запускается приложение
    app = QApplication(sys.argv)
    gui = GUI()
    sys.exit(app.exec_())
