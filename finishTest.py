# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\isser\finishTest.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import sys

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(570, 470)
        self.res = QtWidgets.QLabel(Form)
        self.res.setGeometry(QtCore.QRect(130, 80, 301, 171))
        self.res.setObjectName("res")
        self.closeBut = QtWidgets.QPushButton(Form)
        self.closeBut.setGeometry(QtCore.QRect(190, 280, 191, 41))
        self.closeBut.setObjectName("closeBut")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Результат"))
        self.closeBut.setText(_translate("Form", "Закрыть"))


class FinishTest(QWidget, Ui_Form):
    def __init__(self, mW):
        super().__init__()
        self.mW = mW
        self.setupUi(self)
        self.setFixedSize(self.size())

    def closeEvent(self, event):
        if self.mW:
            self.mW.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FinishTest(None)
    ex.show()
    sys.exit(app.exec_())