import sys
from tkinter import font

from PyQt5.QtWidgets import QApplication, QMainWindow, QMdiArea, QMdiSubWindow, QTextEdit, QAction, QFileDialog, \
    QFontDialog, QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QDesktopWidget
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt

class TextEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.file_name = None
        self.mdi = QMdiArea()
        self.setCentralWidget(self.mdi)

        self.createActions()
        self.createMenus()
        self.createToolBars()

        self.resize(1200, 800)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.setWindowTitle('多文档文本编辑器')
        self.setWindowIcon(QIcon('icon.png'))

        #让打开时就有一个子窗口
        self.newFile()


    def createActions(self):
        self.newAct = QAction(QIcon('icons/new.png'), '新建', self)
        self.newAct.triggered.connect(self.new_window)

        self.openAct = QAction(QIcon('icons/open.png'), '打开', self)
        self.openAct.triggered.connect(self.openFile)

        self.saveAct = QAction(QIcon('icons/save.png'), '保存', self)
        self.saveAct.triggered.connect(self.saveFile)

        self.fontAct = QAction(QIcon('icons/font.png'), '设置字体', self)
        self.fontAct.triggered.connect(self.setFont)

        self.boldAct = QAction(QIcon('icons/bold.png'), '设置粗体', self)
        self.boldAct.triggered.connect(self.setBold)

        self.italicAct = QAction(QIcon('icons/italic.png'), '设置斜体', self)
        self.italicAct.triggered.connect(self.setItalic)



        self.cascadeAct = QAction('层叠排列', self)
        self.cascadeAct.triggered.connect(self.mdi.cascadeSubWindows)

        self.tileAct = QAction('平铺排列', self)
        self.tileAct.triggered.connect(self.mdi.tileSubWindows)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu('文件')
        self.fileMenu.addAction(self.newAct)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAct)

        self.formatMenu = self.menuBar().addMenu('格式')
        self.formatMenu.addAction(self.fontAct)
        self.formatMenu.addAction(self.boldAct)
        self.formatMenu.addAction(self.italicAct)


        self.windowMenu = self.menuBar().addMenu('窗口')
        self.windowMenu.addAction(self.cascadeAct)
        self.windowMenu.addAction(self.tileAct)

    def createToolBars(self):
        self.fileToolBar = self.addToolBar('文件')
        self.fileToolBar.addAction(self.newAct)
        self.fileToolBar.addAction(self.openAct)
        self.fileToolBar.addAction(self.saveAct)

        self.formatToolBar = self.addToolBar('格式')
        self.formatToolBar.addAction(self.fontAct)
        self.formatToolBar.addAction(self.boldAct)
        self.formatToolBar.addAction(self.italicAct)


    def new_window(self):
        self.new_window =TextEditor()
        self.new_window.setGeometry(self.width() - 700, self.height() - 350, 1200, 800)
        self.new_window.show()

    def newFile(self):
        sub = QMdiSubWindow()
        textEdit = QTextEdit()
        sub.setWidget(textEdit)
        textEdit.setFont(QFont('Arial', 24))
        sub.setAttribute(Qt.WA_DeleteOnClose)
        self.mdi.addSubWindow(sub)
        sub.showMaximized()

    def openFile(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "打开文件", "", "Text Files (*.txt);;All Files (*)", options=options)
        if fileName:
            self.file_name=fileName
            with open(fileName, 'r', encoding='utf-8') as file:
                text = file.read()
            sub = QMdiSubWindow()
            textEdit = QTextEdit()
            textEdit.setText(text)
            sub.setWidget(textEdit)
            sub.setAttribute(Qt.WA_DeleteOnClose)
            self.mdi.addSubWindow(sub)
            sub.show()

    def saveFile(self):
        print(f"saveFile called, file_name: {self.file_name}")
        if self.file_name:
            #不打开新窗口，直接保存
            activeSubWindow = self.mdi.activeSubWindow()
            if activeSubWindow:
                textEdit = activeSubWindow.widget()
                text = textEdit.toPlainText()
                print(f"Saving text to {self.file_name}")
                with open(self.file_name, 'w', encoding='utf-8') as file:
                    file.write(text)
            else:
                print("No active subwindow found.")
        else:
            #如果没有文件名，则调用另存为
            print("No file name, calling saveAsFile")
            self.saveAsFile()

    def saveAsFile(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "另存为", "", "Text Files (*.txt);;All Files (*)", options=options)
        self.file_name=fileName
        self.saveFile()



    def setFont(self):
        activeSubWindow = self.mdi.activeSubWindow()
        if activeSubWindow:
            textEdit = activeSubWindow.widget()
            font, ok = QFontDialog.getFont()
            if ok:
                textEdit.setCurrentFont(font)

    def setBold(self):
        activeSubWindow = self.mdi.activeSubWindow()
        if activeSubWindow:
            textEdit = activeSubWindow.widget()
            if textEdit.fontWeight() == QFont.Bold:
                textEdit.setFontWeight(QFont.Normal)
            else:
                textEdit.setFontWeight(QFont.Bold)

    def setItalic(self):
        activeSubWindow = self.mdi.activeSubWindow()
        if activeSubWindow:
            textEdit = activeSubWindow.widget()
            state = textEdit.fontItalic()
            textEdit.setFontItalic(not state)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = TextEditor()
    editor.show()
    sys.exit(app.exec_())