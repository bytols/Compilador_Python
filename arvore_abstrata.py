from rply.token import BaseBox


class Programa():

    def __init__(self, value) -> None:
        self.value = value
        self.child = [None] * 2

    def eval(self):
        return int(self.value) 