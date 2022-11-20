import sys

from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit


class InfWidget(QWidget):
    def __init__(self, mainWindow):
        super().__init__()
        self.mW = mainWindow
        self.setWindowTitle('Документация')
        self.resize(740, 510)
        self.setFixedSize(self.size())
        self.text = QTextEdit(self)
        self.text.move(1, 1)
        with open('inf.txt', 'r', encoding='UTF-8') as f:
            text = f.read()
            self.text.setPlainText(text)
        self.text.resize(738, 508)
        self.text.setDisabled(True)

    def closeEvent(self, event):
        if self.mW:
            self.mW.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = InfWidget(None)
    ex.show()
    sys.exit(app.exec_())
