import random
import sys
from PyQt5 import QtGui, QtWidgets
from GoLalgorithm import board
from turing_ant import turing_ant


class cell_grid(QtWidgets.QWidget):  # ,QtWidgets.QMainWindow):
    def __init__(self, x, y, array):
        super(cell_grid, self).__init__()
        self.array = array
        self.size = len(self.array[0])
        self.x = x
        self.y = y

        self._stop = 1  # you can only start when _stop=1
        self._editmode = 0  # 0= start/stop activated
        self._rule = "2G3"
        self._ant = 0
        self.antsteps = 1

        self.initUi_gol()

    def mod_update(self):
        self.update()
        self.cellwidth = (self.x - 2 * self.border) // self.size

    def initUi_gol(self):
        self.myQMenuBar = QtWidgets.QMenuBar(self)
        ag = QtWidgets.QActionGroup(self)#, exclusive=True)
        Menu = self.myQMenuBar.addMenu('Rules')

        self.rule_2G3 = QtWidgets.QAction('2G3', self, checkable=True)
        self.rule_2G3.triggered.connect(self.rules)
        self.rule_2G3.setChecked(True)
        a = ag.addAction(self.rule_2G3)
        Menu.addAction(a)
        self.rule_G1357 = QtWidgets.QAction('G1357', self, checkable=True)
        self.rule_G1357.triggered.connect(self.rules)
        a = ag.addAction(self.rule_G1357)
        Menu.addAction(a)
        self.rule_26G3 = QtWidgets.QAction('26G3', self, checkable=True)
        self.rule_26G3.triggered.connect(self.rules)
        a = ag.addAction(self.rule_26G3)
        Menu.addAction(a)
        self.Menu = Menu

        self.l_info = QtWidgets.QLabel("Edit-Mode: Off", self)
        self.l_info.setStyleSheet('color: red')
        self.l_info.move(190, 27)

        self.l_antmode = QtWidgets.QLabel("Ant-Mode: Off", self)
        self.l_antmode.setStyleSheet('color: red')
        self.l_antmode.move(620, 27)

        self.b_start = QtWidgets.QPushButton("Start", self)
        # self.b_start.setCheckable(True)
        self.b_start.clicked.connect(self.start)
        self.b_start.move(10, 25)

        self.b_stop = QtWidgets.QPushButton("Stop", self)
        # self.b_stop.setCheckable(True)
        self.b_stop.clicked.connect(self.stop)
        self.b_stop.move(100, 25)

        self.b_editmode = QtWidgets.QPushButton("Set new", self)
        # self.b_editmode.setCheckable(True)
        self.b_editmode.clicked.connect(self.setcustom)
        self.b_editmode.move(10, 60)

        self.tb_size = QtWidgets.QLineEdit(self)
        self.tb_size.setGeometry(120, 60, 60, 35)
        self.tb_size.setText("10")
        self.tb_size.setEnabled(False)

        self.b_setsize = QtWidgets.QPushButton("Set size", self)
        self.b_setsize.clicked.connect(self.setsize)
        self.b_setsize.move(200, 60)
        self.b_setsize.setEnabled(False)

        self.b_random = QtWidgets.QPushButton("Random Field", self)
        self.b_random.clicked.connect(self.random)
        self.b_random.move(300, 60)
        self.b_random.setEnabled(False)

        # verticalLine = QtGui.QFrame(self)
        # verticalLine.move(20,10)

        self.b_ant = QtWidgets.QPushButton("Turing Ant", self)
        self.b_ant.clicked.connect(self.turing_ant)
        self.b_ant.move(470, 25)

        self.l_antinfo = QtWidgets.QLabel("steps: 0", self)
        self.l_antinfo.setGeometry(470, 60, 150, 36)

        self.setGeometry(300, 300, self.x, self.y)
        self.setWindowTitle("Game of life")
        self.show()

    def turing_ant(self):
        if self._editmode == 0:
            if self._ant == 0:
                self.anti = self.antjj = self.size // 2
                self.antdir = None
                self.antsteps = 1

                self.l_antmode.setStyleSheet('color: green')
                self.l_antmode.setText("Ant-Mode: On")
                self._ant = 1
                self.b_editmode.setEnabled(False)
                self.array = [[0 for i in range(self.size)] for j in range(self.size)]
                i0 = self.size // 2
                # self.array[i0][i0]=1
                self.update()

            else:
                self.l_antmode.setStyleSheet('color: red')
                self.l_antmode.setText("Ant-Mode: Off")
                self._ant = 0
                self.b_editmode.setEnabled(True)

    def oneorzero(self, percent):
        if random.randrange(0, 100) <= percent:
            return 1
        else:
            return 0

    def random(self):
        self.array = [[self.oneorzero(15) for i in range(self.size)] for j in range(self.size)]
        self.update()

    def rules(self):
        if self._stop == 1:
            if self.rule_2G3.isChecked():  # Standart GoL
                self._rule = "2G3"

            elif self.rule_26G3.isChecked():  # Expanding GoL
                self._rule = "26G3"

            elif self.rule_G1357.isChecked():  # Copyworld
                self._rule = "G1357"
        else:
            print("You need to 'stop'!")

    def mousePressEvent(self, QMouseEvent):
        if self._editmode == 1:
            pos = QMouseEvent.pos()
            x = pos.x()
            y = pos.y()
            if self.border < x < self.x - self.border2 and self.y - self.x + self.border < y < self.y - self.border2:
                x -= self.border
                y = y - self.border - (self.y - self.x)
                i = x // self.cellwidth
                j = y // self.cellwidth
                if self.array[j][i] == 0:
                    self.array[j][i] = 1
                else:
                    self.array[j][i] = 0
                self.update()

    def setsize(self):
        try:
            x = int(self.tb_size.text())
            self.array = [[0 for i in range(x)] for j in range(x)]  # [[0]*x]*x
            self.size = len(self.array[0])
            self.mod_update()
        except:
            print("wrong input")

    def setcustom(self):
        if self._editmode == 0:
            self._editmode = 1
            self.b_ant.setEnabled(False)
            self.b_start.setEnabled(False)
            self.b_stop.setEnabled(False)
            self.tb_size.setEnabled(True)
            self.b_setsize.setEnabled(True)
            self.b_random.setEnabled(True)

            self.l_info.setText("Edit-Mode: On")
            self.l_info.setStyleSheet('color: green')
            self.array = [[0 for i in range(self.size)] for j in range(self.size)]  # [[0]*self.size]*self.size
            self.update()

        else:
            self._editmode = 0
            self.b_ant.setEnabled(True)
            self.b_start.setEnabled(True)
            self.b_stop.setEnabled(True)
            self.tb_size.setEnabled(False)
            self.b_setsize.setEnabled(False)
            self.b_random.setEnabled(False)

            self.l_info.setText("Edit-Mode: Off")
            self.l_info.setStyleSheet('color: red')

    def stop(self):
        self._stop = 1
        if self._ant == 0:
            self.b_editmode.setEnabled(True)
            self.Menu.setEnabled(True)
        self.b_start.setEnabled(True)

    def start(self):
        self.b_editmode.setEnabled(False)
        self.Menu.setEnabled(False)
        self.b_start.setEnabled(False)
        if self._stop == 1:
            self._stop = 0
            if self._ant == 0:
                while True:
                    GoL = board(self.array, self._rule)
                    self.array = GoL.algorithm()
                    self.mod_update()
                    QtWidgets.QApplication.processEvents()
                    time.sleep(0.1)
                    if self._stop == 1:
                        break

                    cnt = 0
                    for i in self.array:
                        cnt += i.count(1)
                        if cnt != 0:
                            break
                    if cnt == 0:
                        self.stop()
                        break
            else:

                ant = turing_ant(self.array, self.anti, self.antjj, self.antdir)

                while True:
                    self.l_antinfo.setText("steps: " + str(self.antsteps))
                    try:
                        self.array, self.anti, self.antj, self.antdir = ant.algorithm()
                    except IndexError:
                        self.stop()
                        break
                    self.mod_update()
                    QtWidgets.QApplication.processEvents()
                    # time.sleep(2)
                    self.antsteps += 1
                    if self._stop == 1:
                        break

    def paintEvent(self, e):

        qp = QtGui.QPainter()
        qp.begin(self)
        self.qp = qp
        self.drawRectangles()
        qp.end()

    def drawRectangles(self):

        # pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)

        self.qp.setBrush(QtGui.QColor(220, 220, 220))
        self.border = 10
        y1 = self.y - self.x + self.border
        x2 = self.x - 2 * self.border
        # m=self.size
        self.cellwidth = x2 // self.size
        x2 = self.cellwidth * self.size
        y2 = x2
        self.qp.drawRect(self.border, y1, x2, y2)

        self.border2 = self.x - (x2 + self.border)
        ygrid2 = self.y - self.border2
        xgrid2 = self.x - self.border2
        for i in range(self.size):
            self.qp.drawLine(self.border + self.cellwidth * i, y1, self.border + self.cellwidth * i, ygrid2)
            self.qp.drawLine(self.border, y1 + self.cellwidth * i, xgrid2, y1 + self.cellwidth * i)

        # self.drawcircles()
        self.drawrects()

    def drawcircles(self):
        array = self.array
        self.qp.setBrush(QtGui.QColor(0, 0, 240))
        for i in range(self.size):
            for j in range(self.size):
                if array[j][i] == 1:
                    x = self.border + self.cellwidth * i + (self.cellwidth * 0.2)
                    y = self.y - self.x + self.border + self.cellwidth * j + (self.cellwidth * 0.2)
                    self.qp.drawEllipse(x, y, self.cellwidth * 0.6, self.cellwidth * 0.6)

    def drawrects(self):
        array = self.array
        self.qp.setBrush(QtGui.QColor(0, 0, 0))
        for i in range(self.size):
            for j in range(self.size):
                if array[j][i] == 1:
                    x = self.border + self.cellwidth * i
                    y = self.y - self.x + self.border + self.cellwidth * j
                    self.qp.drawRect(x, y, self.cellwidth, self.cellwidth)


import time




def main():
    # x=350
    # y=450
    x = 850
    y = 950
    """
    a=[[0,1,0,0,0],
       [0,0,1,0,0],
       [1,1,1,0,0],
       [0,0,0,0,0],
       [0,0,0,0,0]]
    """
    a = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
         [0, 0, 1, 0, 1, 1, 0, 1, 0, 0],
         [0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
         [0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
         [0, 0, 1, 0, 1, 1, 0, 1, 0, 0],
         [0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         ]

    app = QtWidgets.QApplication(sys.argv)
    ex = cell_grid(x, y, a)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
