import sys
import sqlite3
import datetime as dt

from PIL import Image
from random import sample
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QCheckBox, QRadioButton, QMessageBox, \
    QWidget, QTextEdit

from inf import InfWidget
from image import ImWidget
from history import HWidget
from answerType0 import AnsType0
from createTest import CreateTest
from finishTest import FinishTest
from chooseTest import ChooseTest
from answerType12 import AnsType12
from mainWindow import Ui_MainWindow
from editingTest import EdititngQuestion
from ChooseTO import ChooseTestAndOption
from errors import TPErrors, TitleError, VarsError, AnsError, AnsFormError, PointError, PointFormError, \
    CrTestFormError, TitleNotNewError, QCountError


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.connection = sqlite3.connect('TestProgram_db.sqlite')
        self.setFixedSize(self.size())
        self.test.clicked.connect(self.testFunc)
        self.history.clicked.connect(self.historyFunc)
        self.redact.clicked.connect(self.redactFunc)
        self.inf.clicked.connect(self.infShow)

    def testFunc(self):
        self.hide()
        cur = self.connection.cursor()
        self.CTWidget = ChooseTest(self)
        self.CTWidget.show()
        testList = cur.execute("SELECT title FROM data").fetchall()
        self.CTWidget.testList.addItems([i[0] for i in testList])
        self.CTWidget.startTest.clicked.connect(self.startTest)

    def startTest(self):
        cur = self.connection.cursor()
        self.test = self.CTWidget.testList.currentText()
        self.name = self.CTWidget.name.text() if self.CTWidget.name.text() else 'Без Имени'
        self.maxpoint = cur.execute(f"SELECT maxpoint FROM data WHERE title='{self.test}'").fetchall()[0][0]
        self.CTWidget.close()
        self.date = dt.datetime.now().date().strftime('%d.%m.%Y')
        stTime = dt.datetime.now().time()
        self.startTime = dt.timedelta(hours=stTime.hour, minutes=stTime.minute, seconds=stTime.second)
        self.questions = cur.execute(f'SELECT * FROM questions WHERE testid=(SELECT id FROM data'
                                     f' WHERE title="{self.test}")').fetchall()
        d = {0: (AnsType0, None), 1: (AnsType12, QRadioButton), 2: (AnsType12, QCheckBox)}
        self.qWidgetsDict = {}
        self.point = 0
        for n, i in enumerate(sample(self.questions, len(self.questions))):
            n = len(self.questions) - n
            questionWidget = d[i[2]][0](self.getPoint)
            questionWidget.maxpoint = i[5]
            questionWidget.ansType = i[2]
            questionWidget.rightAns = i[4].split(';') if questionWidget.ansType else i[4]
            questionWidget.vars = i[3].split(';') if i[3] else []
            questionWidget.picture = i[6]
            if i[6]:
                self.pictureIsShowing = False
                questionWidget.im.clicked.connect(self.showIm)
            else:
                questionWidget.im.hide()
            questionWidget.varsDict = {}
            for nj, j in enumerate(questionWidget.vars):
                questionWidget.varsDict[j] = nj + 1
            questionWidget.numb.setText(questionWidget.numb.text() + str(n))
            questionWidget.setWindowTitle('Вопрос')
            questionWidget.text.setText(i[1])
            if questionWidget.ansType:
                for nj, j in enumerate(questionWidget.vars):
                    questionWidget.ansvar = d[i[2]][1]()
                    questionWidget.ansvar.setText(j)
                    questionWidget.userAns[j] = 0
                    if questionWidget.ansType == 1:
                        questionWidget.ansvar.toggled.connect(questionWidget.button_clicked)
                    else:
                        questionWidget.ansvar.stateChanged.connect(questionWidget.button_clicked)
                    questionWidget.verticalLayout.addWidget(questionWidget.ansvar)
            self.qWidgetsDict[f'question_{n}'] = questionWidget
        self.curquestion = 1
        self.hide()
        self.qWidgetsDict['question_1'].show()

    def showIm(self):
        if not self.pictureIsShowing:
            self.pictureIsShowing = True
            widget = self.qWidgetsDict[f'question_{self.curquestion}']
            widget.imageWidget = ImWidget(widget.picture, self)
            widget.imageWidget.show()

    def getPoint(self):
        widget = self.qWidgetsDict[f'question_{self.curquestion}']
        if not widget.ansType:
            widget.point = widget.maxpoint if widget.ans.text() == widget.rightAns else 0
        else:
            userAns = {}
            for i in widget.userAns:
                userAns[widget.varsDict[i]] = widget.userAns[i]
            rightAns = {}
            for i in range(1, len(widget.vars) + 1):
                rightAns[i] = 1 if str(i) in widget.rightAns else 0
            if widget.ansType == 1 and userAns == rightAns:
                widget.point = widget.maxpoint
            elif widget.ansType == 2:
                widget.point = widget.maxpoint * max(len([i for i in range(1, len(widget.vars) + 1)
                                                          if userAns[i] == rightAns[i]]) -
                                                     len([i for i in range(1, len(widget.vars) + 1)
                                                          if userAns[i] != rightAns[i]]), 0) / len(widget.vars) \
                    if any([i for i in userAns]) else 0
            else:
                widget.point = 0
        self.point += int(widget.point)
        widget.close()
        if self.qWidgetsDict.get(f'question_{self.curquestion + 1}', 0):
            self.curquestion += 1
            self.qWidgetsDict[f'question_{self.curquestion}'].show()
        else:
            self.getResult()

    def getResult(self):
        fTime = dt.datetime.now().time()
        self.finishTime = dt.timedelta(hours=fTime.hour, minutes=fTime.minute, seconds=fTime.second)
        self.time = self.finishTime - self.startTime
        self.res = int(self.point / self.maxpoint * 100) if self.maxpoint else 100
        cur = self.connection.cursor()
        cur.execute(f"INSERT INTO results VALUES " \
                    f"((SELECT id FROM data WHERE title='{self.test}'), '{self.name}', '{self.date}'," \
                    f"'{self.startTime}', '{self.time}', '{self.res}%', 0)")
        self.connection.commit()
        self.finTestWidget = FinishTest(self)
        self.finTestWidget.res.setText(f'Вы набрали {self.point} из {self.maxpoint} баллов, что составляет {self.res}%')
        self.finTestWidget.show()
        self.finTestWidget.closeBut.clicked.connect(self.finTestWidget.close)

    def historyFunc(self):
        self.hide()
        self.hWidget = HWidget(self)
        self.hWidget.show()
        cur = self.connection.cursor()
        res = cur.execute('''SELECT (SELECT title FROM data WHERE id=testid),
        who, date, startTime, time, res, deleted FROM results''').fetchall()[::-1]
        self.hWidget.tableWidget.setColumnCount(6)
        self.hWidget.tableWidget.setRowCount(0)
        for i, row in enumerate(res):
            self.hWidget.tableWidget.setRowCount(
                self.hWidget.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row[:6]):
                if row[6] and j == 0:
                    elem = 'Удалено'
                self.hWidget.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.hWidget.clear.clicked.connect(self.clearHist)

    def clearHist(self):
        cur = self.connection
        valid = QMessageBox.question(
            self, 'Подтвердите действие', 'Действительно очистить?',
            QMessageBox.Yes, QMessageBox.No)
        if valid == QMessageBox.Yes:
            cur.execute("DELETE FROM results")
            self.connection.commit()
            self.hWidget.close()
            self.historyFunc()

    def redactFunc(self):
        self.hide()
        self.isCreating = False
        self.redactingTest = None
        cur = self.connection.cursor()
        self.testAndOption = ChooseTestAndOption(self)
        testList = cur.execute("SELECT title FROM data").fetchall()
        self.testAndOption.tests.addItems([i[0] for i in testList])
        self.testAndOption.show()
        self.testAndOption.redact.clicked.connect(self.redactTest)
        self.testAndOption.New.clicked.connect(self.newTest)
        self.testAndOption.deleteTest.clicked.connect(self.deleteTest)

    def redactTest(self):
        self.hide()
        if not self.isCreating:
            self.redactingTest = self.testAndOption.tests.currentText()
            self.testAndOption.close()
        self.maxpoint = 0
        cur = self.connection.cursor()
        self.hide()
        self.questions = cur.execute(f'SELECT * FROM questions WHERE testid=(SELECT id FROM data'
                                     f' WHERE title="{self.redactingTest}")').fetchall()
        self.widgetsDict = {}
        for n, i in enumerate(self.questions):
            n = len(self.questions) - n
            widget = EdititngQuestion(self.widgetClosedUnexpected)
            widget.nv.setText(widget.nv.text() + str(n))
            widget.title.setText(i[1])
            d = {0: 'Ввод ответа', 1: 'Один из нескольких вариантов', 2: 'Несколько вариантов'}
            widget.ansType.setCurrentText(d[i[2]])
            if i[2]:
                vars = i[3].split(';')
                widget.vars.setDisabled(False)
                widget.vars.setPlainText('\n'.join(vars))
            widget.ans.setText(i[4])
            widget.point.setText(str(i[5]))
            widget.picture = i[6]
            if i[6]:
                widget.loadImage.setText(i[6].split('/')[-1])
            widget.next.clicked.connect(self.allIsOk)
            self.widgetsDict[n] = widget
        self.curquestion = 1
        self.widgetsDict[1].show()

    def widgetClosedUnexpected(self):
        n = len(self.questions) - self.curquestion
        self.maxpoint += self.questions[n][5]
        self.curquestion += 1
        if self.curquestion <= len(self.questions):
            self.widgetsDict[self.curquestion].show()
        else:
            self.loadChangings()

    def allIsOk(self):
        widget = self.widgetsDict[self.curquestion]
        n = len(self.questions) - self.curquestion
        d = {'Ввод ответа': 0, 'Один из нескольких вариантов': 1, 'Несколько вариантов': 2}
        title, ansType, vars, ans, point, picture = widget.title.text(), d[widget.ansType.currentText()], \
                                                    ';'.join(widget.vars.toPlainText().split('\n')), \
                                                    widget.ans.text(), widget.point.text(), widget.picture
        try:
            if not title:
                raise TitleError
            if ansType and not vars:
                raise VarsError
            if not ans:
                raise AnsError
            if ansType and not all([i.isdigit() or i == ';' for i in ans]) \
                    or ansType and not any([i.isdigit() for i in ans]) \
                    or ansType and any([int(i) > len(vars.split(';')) for i in ans.split(';')]) \
                    or ansType and len(set(ans.split(';'))) != len(ans.split(';')) \
                    or ansType == 1 and len(ans.split(';')) > 1:
                raise AnsFormError
            if not point:
                raise PointError
            if not point.isdigit():
                raise PointFormError
            widget.canBeClosed = True
            widget.close()
            self.getRedaction(n, title, ansType, vars, ans, point, picture)
        except TPErrors as e:
            message = QMessageBox.about(widget, 'Ошибка', e.getErrorText())

    def getRedaction(self, *args):
        n, title, ansType, vars, ans, point, picture = args
        vars = vars if vars else None
        if picture:
            cur = self.connection.cursor()
            if picture not in cur.execute("SELECT DISTINCT picture FROM questions").fetchall():
                im = Image.open(picture)
                newfname = 'pictures/' + picture.split('/')[-1]
                im.save(newfname)
            picture = newfname
        self.questions[n] = (self.questions[n][0], title, ansType, vars, ans, point, picture)
        self.maxpoint += int(point)
        self.curquestion += 1
        if self.curquestion <= len(self.questions):
            self.widgetsDict[self.curquestion].show()
        else:
            self.loadChangings()

    def loadChangings(self):
        cur = self.connection.cursor()
        cur.execute(f"UPDATE data SET maxpoint={self.maxpoint} WHERE title='{self.redactingTest}'")
        cur.execute(
            f"DELETE FROM questions WHERE testid=(SELECT id FROM data WHERE title='{self.redactingTest}')")
        cur.execute(f"""INSERT INTO questions VALUES
{', '.join(['(' + ', '.join([str(j if j != None else 'NULL') if k in [0, 2, 5] or j == None else "'" + str(j) + "'"
                             for k, j in enumerate(i)]) + ')' for i in self.questions])}""")
        self.connection.commit()
        self.isCreating = False
        self.show()

    def newTest(self):
        self.testAndOption.close()
        self.createTest = CreateTest(self)
        self.hide()
        self.createTest.show()
        self.createTest.cr.clicked.connect(self.crTest)

    def crTest(self):
        cur = self.connection.cursor()
        title = self.createTest.title.text()
        nvopr = self.createTest.nvopr.text()
        try:
            if not nvopr or not all([i.isdigit() or i == '-' for i in nvopr]) or not title:
                raise CrTestFormError
            if title in [i[0] for i in cur.execute('SELECT title FROM data').fetchall()]:
                raise TitleNotNewError
            if int(nvopr) < 1:
                raise QCountError
            newid = max([int(i[0]) for i in cur.execute('SELECT id from data').fetchall()]) + 1
            cur.execute(f"INSERT INTO data VALUES ({newid}, '{title}', 0)")
            cur.execute(f"""INSERT INTO questions VALUES 
{", ".join([f"({newid}, '', 0, NULL, '', 0, NULL)" for i in range(int(nvopr))])}""")
            self.connection.commit()
            self.isCreating = True
            self.redactingTest = title
            self.createTest.close()
            self.redactTest()
        except TPErrors as e:
            message = QMessageBox.about(self.createTest, 'Ошибка', e.getErrorText())

    def deleteTest(self):
        testname = self.testAndOption.tests.currentText()
        cur = self.connection.cursor()
        valid = QMessageBox.question(
            self, 'Подтвердите действие', f'Действительно удалить тест {testname}?',
            QMessageBox.Yes, QMessageBox.No)
        if valid == QMessageBox.Yes:
            cur.execute(f"UPDATE results SET deleted=1 WHERE testid=(SELECT id from data where title='{testname}')")
            cur.execute(f"DELETE from questions where testid=(SELECT id from data where title='{testname}')")
            cur.execute(f"DELETE from data where title='{testname}'")
            self.connection.commit()
            self.testAndOption.close()

    def infShow(self):
        self.hide()
        self.infWidget = InfWidget(self)
        self.infWidget.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
