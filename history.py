# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\isser\results.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(632, 470)
        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setGeometry(QtCore.QRect(10, 10, 611, 401))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        self.closeButton = QtWidgets.QPushButton(Form)
        self.closeButton.setGeometry(QtCore.QRect(320, 420, 171, 31))
        self.closeButton.setObjectName("closeButton")
        self.clear = QtWidgets.QPushButton(Form)
        self.clear.setGeometry(QtCore.QRect(140, 420, 171, 31))
        self.clear.setObjectName("clear")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "история"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Тест"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Кто"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Form", "Дата"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Form", "Время начала"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Form", "Время"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("Form", "Результат"))
        self.closeButton.setText(_translate("Form", "Закрыть"))
        self.clear.setText(_translate("Form", "очистить"))


class HWidget(QWidget, Ui_Form):
    def __init__(self, mW):
        super().__init__()
        self.setupUi(self)
        self.mW = mW
        self.setFixedSize(self.size())
        self.closeButton.clicked.connect(self.close)

    def closeEvent(self, event):
        if self.mW:
            self.mW.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = HWidget(None)
    ex.show()
    sys.exit(app.exec_())