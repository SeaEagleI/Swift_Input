# -*- coding: utf-8 -*-
import sys
import math
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication,QMainWindow
from PyQt5.QtCore import Qt
import time,os,re
from Homepage import Ui_Homepage
from ChoicePanel import Ui_ChoicePanel
from VoiceInput.voiceinput import VoiceInput
from PinyinInput.pinyininput import PinyinInput
import pyperclip
import threading

class SwiftInput(QMainWindow):
    def __init__(self):
        super(SwiftInput, self).__init__()
        self.pi = PinyinInput()
        self.inputMode = 'en_us'
        self.isVisible = False
        self.buffer = ''
        self.py_result = []
        self.MaxRowID = 5
        self.row_id = 1
        self.cands = 6

        self.vi = VoiceInput()
        self.isListening = False
        self.sr_result = ''

        self.formerText = ''

        self.homepage = QtWidgets.QMainWindow()
        self.ui_homepage = Ui_Homepage()
        self.ui_homepage.setupUi(self.homepage)
        self.choicepanel = QtWidgets.QMainWindow()
        self.ui_choicepanel = Ui_ChoicePanel()
        self.ui_choicepanel.setupUi(self.choicepanel)

        self.speakingIcon = QtGui.QIcon()
        self.speakingIcon.addPixmap(QtGui.QPixmap("icons/speaking.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.silenceIcon = QtGui.QIcon()
        self.silenceIcon.addPixmap(QtGui.QPixmap("icons/silence.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui_homepage.inputPanel.setAttribute(QtCore.Qt.WA_InputMethodEnabled, True)
        self.choiceButtons = [self.ui_choicepanel.choice1_btn,self.ui_choicepanel.choice2_btn,self.ui_choicepanel.choice3_btn,
                              self.ui_choicepanel.choice4_btn,self.ui_choicepanel.choice5_btn,self.ui_choicepanel.choice6_btn]

        # QtCore.Qt.ShiftModifier.connect(self.changeMode)
        self.ui_homepage.inputPanel.textChanged.connect(self.on_inputPanel_textChanged)
        self.ui_homepage.pinyinInput_btn.clicked.connect(self.on_pinyinInput_btn_clicked)
        self.ui_homepage.voiceInput_btn.clicked.connect(self.on_voiceInput_btn_clicked)
        self.ui_homepage.clearText_btn.clicked.connect(self.on_clearText_btn_clicked)
        self.ui_homepage.copyText_btn.clicked.connect(self.on_copyText_btn_clicked)

    def update_choice_btns(self,row_id=1):
        self.row_id = row_id
        self.py_result = self.pi.Application(self.buffer,cands=30)
        # self.choices = self.py_result[(self.row_id-1)*self.cands:self.row_id*self.cands]
        self.gotNum = min(self.cands,len(self.py_result)-self.cands*(self.row_id-1))
        self.offset = (self.row_id-1)*self.cands
        for i in range(self.gotNum):
            self.choiceButtons[i].setText("{}.{}".format(i+1,self.py_result[self.offset+i]))
        for j in range(self.gotNum+1,self.cands):
            self.choiceButtons[j].setText("")
        self.choicepanel.show()
        self.isVisible = True

    # self.ui_homepage.keyPressEvent = self.keyPressEvent
    def keyPressEvent(self,event):
        if event.modifiers() == Qt.ShiftModifier:
            self.inputMode = 'zh_cn' if self.inputMode == 'en_us' else 'en_us'
            # self.ui_homepage.statusBar.set
            if self.inputMode == 'en_us':
                self.ui_homepage.inputPanel.append(self.buffer)
                self.exit_choicePanel()
        if self.inputMode == 'en_us':
            return
        elif event.key() == Qt.Key_Escape:
            self.exit_choicePanel()
        elif event.key() == Qt.Key_Space:
            self.ui_homepage.inputPanel.append(self.choiceButtons[0].text())
            self.exit_choicePanel()
        elif event.key()>=Qt.Key_1 and event.key()<=Qt.Key_6:
            choice_id = self.offset + event.key() - Qt.Key_1
            if choice_id<len(self.py_result):
                self.ui_homepage.inputPanel.append(self.py_result[choice_id])
            self.exit_choicePanel()
        elif event.key() == Qt.LeftArrow:
            self.row_id = self.row_id-1 if self.row_id>1 else self.row_id
            self.update_choice_btns(self.row_id)
        elif event.key() == Qt.RightArrow:
            self.row_id = self.row_id+1 if self.row_id<self.MaxRowID and self.row_id<math.ceil(len(self.sr_result)/self.cands) else self.row_id
            self.update_choice_btns(self.row_id)
        elif event.key()>=0x41 and event.key()<=0x5a:
            self.buffer += chr(ord('a')+event.key()-Qt.Key_A)
            self.update_choice_btns()

    def exit_choicePanel(self):
        self.choicepanel.hide()
        self.isVisible = False
        self.buffer = ''

    def on_inputPanel_textChanged(self):
        if self.inputMode == 'en_us':
            return

        self.choicepanel.show()
        self.isVisible = True
        # while QtCore.Qt.Modifier


        self.choicepanel.hide()
        self.isVisible = False

    def on_pinyinInput_btn_clicked(self):
        self.inputMode = 'zh_cn' if self.inputMode=='en_us' else 'en_us'

    def on_voiceInput_btn_clicked(self):
        self.isListening = bool(1-self.isListening)
        t = ''
        if self.isListening:
            # t = threading.Thread(self.vi.recognize())
            self.ui_homepage.voiceInput_btn.setIcon(self.speakingIcon)
            self.duration,self.vi.sr_result = self.vi.recognize()
            # self.ui_homepage.voiceInput_btn.setIcon(self.silenceIcon)

        elif not self.isListening or self.vi.sr_result!='':
            # if self.vi.sr_result=='':
            #     t.join()
            self.ui_homepage.voiceInput_btn.setIcon(self.silenceIcon)
            self.ui_homepage.inputPanel.append(self.vi.sr_result)

    def on_clearText_btn_clicked(self):
        self.formerText = self.ui_homepage.inputPanel.toPlainText()
        self.ui_homepage.inputPanel.clear()

    def on_copyText_btn_clicked(self):
        pyperclip.copy(self.ui_homepage.inputPanel.toPlainText())

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    swiftInput = SwiftInput()
    swiftInput.homepage.show()
    sys.exit(app.exec_())

    # app = QtWidgets.QApplication(sys.argv)
    # choicepanel = QtWidgets.QMainWindow()
    # form = Ui_ChoicePanel()
    # form.setupUi(choicepanel)
    # choicepanel.show()
    # sys.exit(app.exec_())

