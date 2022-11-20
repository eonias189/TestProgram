class TPErrors(Exception):
    def __init__(self):
        self.errorText = ''

    def getErrorText(self):
        return self.errorText


class TitleError(TPErrors):
    def __init__(self):
        self.errorText = 'Введите текст вопроса'


class VarsError(TPErrors):
    def __init__(self):
        self.errorText = 'Введите варианты ответа'


class AnsError(TPErrors):
    def __init__(self):
        self.errorText = 'Введите ответ'


class AnsFormError(TPErrors):
    def __init__(self):
        self.errorText = 'Неверная форма ответа'


class PointError(TPErrors):
    def __init__(self):
        self.errorText = 'Введите балл'


class PointFormError(TPErrors):
    def __init__(self):
        self.errorText = 'Неверная форма балла'


class CrTestFormError(TPErrors):
    def __init__(self):
        self.errorText = 'Неверная форма'


class TitleNotNewError(TPErrors):
    def __init__(self):
        self.errorText = 'Тест с таким именем уже есть'


class QCountError(TPErrors):
    def __init__(self):
        self.errorText = 'В тесте должен быть хотябы один вопрос'
