from PyQt5.QtCore import QRegularExpression
from PyQt5.QtGui import QTextCharFormat, QSyntaxHighlighter, QFont, QTextBlockUserData
import sys
from pathlib import Path

class QuirkOptions(QTextBlockUserData):
    lineType = 'none'
    def __init__(self, quirkType = 'default', lineType = 'none', data = None):
        super().__init__()
        self.quirkType = quirkType
        self.lineType = lineType
        if data:
            self.data = data
            
    def copy(self):
        return self.quirkType, self.lineType, self.data

class QuirkSyntax(QSyntaxHighlighter):
    def __init__(self, doc, project = None):
        super().__init__(doc)
        from Quirk import Quirk

        self.quirks = {'default': Quirk()}

        OptionsFormat = QTextCharFormat()
        OptionsFormat.setFontWeight(QFont.Thin)

        self.TextPatternStartMultiLine = QRegularExpression('<(?!(?:/|\\\\))(.*?)(?<!(?:/|\\\\)):')

        self.TextPatternEndMultiLine = QRegularExpression('((.*?)(?<!(?:/|\\\\)))>')

    def updateQuirks(self, quirks):
        for k, v in quirks.items():
            self.quirks.update({k: v})
    
    def previousBlockUserData(self):
        blockNumber = self.currentBlock().blockNumber()
        if blockNumber > 0:
            block = self.document().findBlockByNumber(blockNumber - 1)
            return block.userData()
        else:
            return QuirkOptions()

    def beginningOfCommand(self, match):
        options = [i.strip() for i in match[1:-1].split(';')]
        quirkType = 'default'
        for i in options:
            if i.lower() in self.quirks:
                quirkType = i.lower()
                break

        self.setCurrentBlockUserData(QuirkOptions(quirkType, 'start', options))

    def highlightBlock(self, text):            
        self.setCurrentBlockState(0)
        self.setCurrentBlockUserData(QuirkOptions())
        quirkSelector = 'default'

        startIndex = 0

        if self.previousBlockState() != 1:
            startIndex = self.TextPatternStartMultiLine.match(text).capturedStart()
            self.beginningOfCommand(self.TextPatternStartMultiLine.match(text).captured())
                    
        while startIndex >= 0:
            match = self.TextPatternEndMultiLine.match(text, startIndex)
            endIndex = match.capturedEnd()
            
            if endIndex == -1:
                self.setCurrentBlockState(1)
                textLength = len(text) - startIndex
                if self.currentBlockUserData().lineType == 'start':
                    quirkSelector = self.currentBlockUserData().quirkType
                elif self.previousBlockUserData().lineType in ['start', 'continue']:
                    p = self.previousBlockUserData().copy()
                    self.setCurrentBlockUserData(QuirkOptions(p[0], 'continue', p[2]))
                    quirkSelector = p[0]
            else :
                textLength = match.capturedLength()
                if self.currentBlockUserData().lineType == 'start':
                    quirkSelector = self.currentBlockUserData().quirkType
                elif self.previousBlockUserData().lineType in ['start', 'continue']:
                    self.setCurrentBlockUserData(QuirkOptions())
                    quirkSelector = self.previousBlockUserData().quirkType

            if quirkSelector == None:
                quirkSelector = 'default'

            self.setFormat(startIndex, textLength, self.quirks[quirkSelector].getFormatQuirk()),

            startIndex = self.TextPatternStartMultiLine.match(text, startIndex + textLength).capturedStart()

            if startIndex >= 0:
                self.beginningOfCommand(self.TextPatternStartMultiLine.match(text, startIndex).captured())