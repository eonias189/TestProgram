# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\isser\createTest.ui'
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
        Form.resize(570, 292)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(80, 80, 71, 16))
        self.label.setObjectName("label")
        self.title = QtWidgets.QLineEdit(Form)
        self.title.setGeometry(QtCore.QRect(150, 80, 341, 20))
        self.title.setObjectName("title")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(10, 120, 131, 21))
        self.label_2.setObjectName("label_2")
        self.nvopr = QtWidgets.QLineEdit(Form)
        self.nvopr.setGeometry(QtCore.QRect(150, 120, 341, 20))
        self.nvopr.setObjectName("nvopr")
        self.cr = QtWidgets.QPushButton(Form)
        self.cr.setGeometry(QtCore.QRect(190, 220, 171, 41))
        self.cr.setObjectName("cr")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Создать тест"))
        self.label.setText(_translate("Form",
                                      "<html><head/><body><p><span style=\" font-size:10pt;\">Название</span></p></body></html>"))
        self.label_2.setText(_translate("Form",
                                        "<html><head/><body><p><span style=\" font-size:10pt;\">Количество вопросов</span></p></body></html>"))
        self.cr.setText(_translate("Form", "Создать"))


class CreateTest(QWidget, Ui_Form):
    def __init__(self, mW):
        super().__init__()
        self.setupUi(self)
        self.mW = mW
        self.setFixedSize(self.size())

    def closeEvent(self, event):
        if self.mW:
            self.mW.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CreateTest(None)
    ex.show()
    sys.exit(app.exec_())
