from PyQt5.QtGui import QColor, QFont, QTextCharFormat
from PyQt5.QtCore import Qt

class Quirk():
    name = 'default'
    preText = ''
    color = QColor(Qt.black)
    font = QFont()
    bgcolor = QColor()
    quirkCode = None
    state = False

    def __init__(self, path = None, font = None):
        import json
        #self.font.setBold(True)
        # self.font.setPixelSize(11)
        if path:
            file = json.loads(path.read_text(encoding='utf-8'))
            fileName = path.stem

            if 'name' in file and file['name'].lower() == fileName:
                self.name = file['name']
                if 'preText' in file:
                    self.preText = file['preText']
                if 'color' in file:
                    color = file['color']
                    self.setColor(color['r'], color['g'], color['b'], color['a'])
                if 'bgcolor' in file:
                    self.bgcolor = file['bgcolor']
                if 'quirk' in file and type(file['quirk']) == str:
                    self.quirkCode = file['quirk']
                self.state = True
            else:
                raise ValueError(f'File "{path}" is not correct file.')

        if font:
            self.font = font

        self.formatQuirk = QTextCharFormat()
        self.setFormatQuirk()

    def setFormatQuirk(self):
        #self.formatQuirk.setFont(self.font)
        self.formatQuirk.setForeground(self.color)
        #self.formatQuirk.setBackground(self.bgcolor)

    def updateFont(self, font):
        self.font = font
        #self.formatQuirk.setFont(self.font)


    def setColor(self, r = 0, g = 0, b = 0, a = 255):
        self.color.setRgb(r, g, b, a)

    def setBGColor(self, r = 255, g = 255, b = 255, a = 255):
        self.bgcolor.setRgb(r, g, b, a)

    def insertPreText(self, document):
        document.textCursor().insertText(self.preText)
        #document.moveCursor()

    def quirk(self, textBlock, previousBlock = None):
        pass

    def getFormatQuirk(self):
        return self.formatQuirk