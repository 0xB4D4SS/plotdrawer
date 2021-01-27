import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
import matplotlib.pyplot as plt
from matplotlib import cm
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
        step = 0.1
        # получаем текст функции для отрисовки
        formula = self.finput.text()
        # 3d случай
        if self.rbtn.isChecked():
            # задаем диапазоны x и y
            xval = arange(-6.0, 6.0, step)
            yval = arange(-6.0, 6.0, step)
            x, y = meshgrid(xval, yval)
            # задаем функцию неявно (z = f(x,y)) с помощью лямбда выражения
            f = lambda x=0, y=0: eval(formula)
            # if formula.find('x') != -1:
            #     i = -1
            #     for valx in xval:
            #         i = i + 1
            #         xs = symbols('x')
            #         lim1 = limit(sympify(formula), xs, valx, dir='-').evalf()
            #         lim2 = limit(sympify(formula), xs, valx, dir='+').evalf()
            #         limnext = limit(sympify(formula), xs, valx - step, dir='+').evalf()
            #         currz = f(valx, yval[i])
            #         if not(lim1 - lim2 < step) or not(lim1 - currz < step) or not(lim2 - currz < step):
            #             xval[i] = nan
            #         elif diff([lim2, limnext]) > 20.0:
            #             xval[i] = nan
            # if formula.find('y') != -1:
            #     k = -1
            #     for valy in yval:
            #         k = k + 1
            #         ys = symbols('y')
            #         lim3 = limit(sympify(formula), ys, valy, dir='-').evalf()
            #         lim4 = limit(sympify(formula), ys, valy, dir='+').evalf()
            #         limnext2 = limit(sympify(formula), ys, valy - step, dir='+').evalf()
            #         currz = f(xval[k], valy)
            #         if not(lim3 - lim4 < step) or not(lim3 - currz < step) or not(lim4 - currz < step):
            #             yval[k] = nan
            #         elif diff([lim4, limnext2]) > 20.0:
            #             yval[k] = nan
            # print('x')
            # print(xval)
            # print('y')
            # print(yval)
            # print(eval(formula))
            z = f(x, y)
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
            # проверяем функцию на точки разрыва
            # проверяем равенство пределов и значения функции в точке и проверяем нету ли скачка предела в точке
            # если пределы равны или скачка нет - точки разрыва нет, иначе есть
            # до сих пор не рисует sqrt, log и abs
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
            print(xval)
            # дебажный вывод в консоль
            # print(eval(formula))
            # собсна создаем график
            fig = plt.figure()
            plt.plot(xval, y(xval))
            # пределы отрисовки оси y
            plt.ylim(-5, 5)

        plt.grid()
        plt.show()
        plt.savefig('plot.png')


if __name__ == '__main__':
    # здесь запускается приложение
    app = QApplication(sys.argv)
    gui = GUI()
    sys.exit(app.exec_())
