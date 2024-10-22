import sys
from typing import Union

from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from PyQt5.QtWidgets import QApplication, QMainWindow, QMdiArea, QMdiSubWindow, QTextEdit, QAction, QFileDialog, \
    QFontDialog, QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QDesktopWidget, QMenu, QToolButton, QLabel, QStatusBar, \
    QShortcut, QMessageBox, QInputDialog
from PyQt5.QtGui import QIcon, QFont, QKeySequence, QTextCursor, QPainter
from PyQt5.QtCore import Qt
import json
import time


class TextEditor(QMainWindow):
    wordCountLabel: Union[QLabel, QLabel]

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
        self.createStatusBar()

        self.resize(1800, 1200)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.setWindowTitle('多文档文本编辑器')
        self.setWindowIcon(QIcon('icon.png'))

        # 让打开时就有一个子窗口
        self.newFile()
        self.shortcut = QShortcut(QKeySequence('Esc'), self)
        self.shortcut.activated.connect(self.close)

    def createActions(self):
        self.newAct = QAction(QIcon('icons/new.png'), '&新建', self)
        self.newAct.setShortcut('Ctrl+N')
        self.newAct.triggered.connect(self.new_window)

        self.openAct = QAction(QIcon('icons/open.png'), '&打开', self)
        self.openAct.setShortcut('Ctrl+O')
        self.openAct.triggered.connect(self.openFile_with_history)

        self.saveAct = QAction(QIcon('icons/save.png'), '&保存', self)
        self.saveAct.setShortcut('Ctrl+S')
        self.saveAct.triggered.connect(self.saveFile)

        self.fontAct = QAction(QIcon('icons/font.png'), '设置&字体', self)
        self.fontAct.setShortcut('Ctrl+Shift+F')
        self.fontAct.triggered.connect(self.setFont)

        self.boldAct = QAction(QIcon('icons/bold.png'), '设置&粗体', self)
        self.boldAct.setShortcut('Ctrl+B')
        self.boldAct.triggered.connect(self.setBold)

        self.italicAct = QAction(QIcon('icons/italic.png'), '设置&斜体', self)
        self.italicAct.setShortcut('Ctrl+I')
        self.italicAct.triggered.connect(self.setItalic)

        self.cascadeAct = QAction('&层叠排列', self)
        self.cascadeAct.setShortcut('Ctrl+Shift+C')
        self.cascadeAct.triggered.connect(self.mdi.cascadeSubWindows)

        self.tileAct = QAction('&平铺排列', self)
        self.tileAct.setShortcut('Ctrl+Shift+T')
        self.tileAct.triggered.connect(self.mdi.tileSubWindows)

        # 新增功能，另存为，撤回，重做，全选，复制，剪切，粘贴
        self.saveAsAct = QAction(QIcon('icons/save_as.png'), '另存为', self)
        self.saveAsAct.setShortcut('Alt+Shift+S')
        self.saveAsAct.triggered.connect(self.saveAsFile)

        self.undoAct = QAction(QIcon('icons/undo.png'), '撤回', self)
        self.undoAct.setShortcut('Ctrl+Z')
        self.undoAct.triggered.connect(self.undo)

        self.redoAct = QAction(QIcon('icons/redo.png'), '重做', self)
        self.redoAct.setShortcut('Ctrl+Y')
        self.redoAct.triggered.connect(self.redo)

        # 全选，复制，剪切，粘贴
        self.selectAllAct = QAction(QIcon('icons/all_act.png'), '全选', self)
        self.selectAllAct.setShortcut('Ctrl+A')
        self.selectAllAct.triggered.connect(self.selectAll)

        self.copyAct = QAction(QIcon('icons/copy.png'), '复制', self)
        self.copyAct.setShortcut('Ctrl+C')
        self.copyAct.triggered.connect(self.copy)

        self.cutAct = QAction(QIcon('icons/cut.png'), '剪切', self)
        self.cutAct.setShortcut('Ctrl+X')
        self.cutAct.triggered.connect(self.cut)

        self.pasteAct = QAction(QIcon('icons/paste.png'), '粘贴', self)
        self.pasteAct.setShortcut('Ctrl+V')
        self.pasteAct.triggered.connect(self.paste)

        # 搜索
        self.searchAct = QAction(QIcon('icons/search.png'), '搜索', self)
        self.searchAct.setShortcut('Ctrl+F')
        self.searchAct.triggered.connect(self.search)

        # 打印
        self.printAct = QAction(QIcon('icons/print.png'), '打印', self)
        self.printAct.setShortcut('Ctrl+P')
        self.printAct.triggered.connect(self.print)

    def print(self):
        activeSubWindow = self.mdi.activeSubWindow()
        if activeSubWindow:
            textEdit = activeSubWindow.widget()
            text = textEdit.toPlainText()
            # 调用打印机
            printer = QPrinter()
            printDialog = QPrintDialog(printer, self)
            if printDialog.exec_():
                painter = QPainter(printer)
                painter.drawText(10, 10, text)
                painter.end()

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu('文件')
        self.fileMenu.addAction(self.newAct)
        self.fileMenu.addAction(self.openAct)
        self.openFile_with_history()
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addAction(self.saveAsAct)
        self.fileMenu.addAction(self.printAct)

        self.formatMenu = self.menuBar().addMenu('编辑')
        self.formatMenu.addAction(self.fontAct)
        self.formatMenu.addAction(self.boldAct)
        self.formatMenu.addAction(self.italicAct)
        self.formatMenu.addAction(self.undoAct)
        self.formatMenu.addAction(self.redoAct)
        self.formatMenu.addAction(self.selectAllAct)
        self.formatMenu.addAction(self.copyAct)
        self.formatMenu.addAction(self.cutAct)
        self.formatMenu.addAction(self.pasteAct)
        self.formatMenu.addAction(self.searchAct)

        self.windowMenu = self.menuBar().addMenu('窗口')
        self.windowMenu.addAction(self.cascadeAct)
        self.windowMenu.addAction(self.tileAct)

    def createToolBars(self):
        self.fileToolBar = self.addToolBar('文件')
        self.fileToolBar.addAction(self.newAct)
        self.fileToolBar.addAction(self.openAct)
        self.fileToolBar.addAction(self.saveAct)
        self.fileToolBar.addAction(self.saveAsAct)
        self.fileToolBar.addAction(self.printAct)

        self.formatToolBar = self.addToolBar('编辑')
        self.formatToolBar.addAction(self.fontAct)
        self.formatToolBar.addAction(self.boldAct)
        self.formatToolBar.addAction(self.italicAct)
        self.formatToolBar.addAction(self.undoAct)
        self.formatToolBar.addAction(self.redoAct)
        self.formatToolBar.addAction(self.selectAllAct)
        self.formatToolBar.addAction(self.copyAct)
        self.formatToolBar.addAction(self.cutAct)
        self.formatToolBar.addAction(self.pasteAct)
        self.formatToolBar.addAction(self.searchAct)

    def createStatusBar(self):
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.wordCountLabel = QLabel('字数: 0')
        self.selectedCountLabel = QLabel('选中字符数: 0')
        self.fontSizeLabel = QLabel('字号: 24')
        self.statusBar.addPermanentWidget(self.wordCountLabel, 1)
        self.statusBar.addPermanentWidget(self.selectedCountLabel, 1)
        self.statusBar.addPermanentWidget(self.fontSizeLabel, 1)

    def new_window(self):
        self.new_window = TextEditor()
        self.new_window.setGeometry(self.geometry().x() + 30, self.geometry().y() + 30, self.width(), self.height())
        self.new_window.show()

    def newFile(self):
        sub = QMdiSubWindow()
        self.textEdit = QTextEdit()
        self.textEdit.textChanged.connect(self.updateStatusBar)
        self.textEdit.cursorPositionChanged.connect(self.updateStatusBar)
        sub.setWidget(self.textEdit)
        self.textEdit.setFont(QFont('Arial', 24))
        sub.setAttribute(Qt.WA_DeleteOnClose)
        self.mdi.addSubWindow(sub)
        sub.showMaximized()

    def openFile(self, file_name):
        print(file_name)
        if file_name:
            try:
                with open(file_name, 'r', encoding='utf-8') as file:
                    text1 = file.read()
                    # 让textEdit显示文件内容
                    activeSubWindow = self.mdi.activeSubWindow()
                    if activeSubWindow:
                        self.textEdit = activeSubWindow.widget()
                        self.textEdit.setPlainText(text1)
                    self.textEdit.textChanged.connect(self.updateStatusBar)
                    print(text1)
                # 保存在history.json中
                self.file_name = file_name
                self.saveFile()
                self.openFile_with_history()
            except FileNotFoundError:
                text = ''
                # 给出消息框提示文件不存在
                QMessageBox.warning(self, '错误', '文件不存在')
                # 在history.json中删除不存在的文件
                history = []
                try:
                    with open('history.json', 'r', encoding='utf-8') as file:
                        history = json.load(file)
                except FileNotFoundError:
                    pass
                except json.JSONDecodeError:
                    pass
                if history:
                    for file in history:
                        if file['file_name'] == file_name:
                            history.remove(file)
                            with open('history.json', 'w', encoding='utf-8') as file:
                                json.dump(history, file)
                    # 刷新界面
                    self.openFile_with_history()
        else:
            # 打开文件选取框
            options = QFileDialog.Options()
            fileName, _ = QFileDialog.getOpenFileName(self, "打开文件", "", "Text Files (*.txt);;All Files (*)",
                                                      options=options)
            if fileName:
                with open(fileName, 'r', encoding='utf-8') as file:
                    text1 = file.read()
                    file_name = fileName

        sub = QMdiSubWindow()
        textEdit = QTextEdit()
        textEdit.setPlainText(text1)
        textEdit.textChanged.connect(self.updateStatusBar)
        textEdit.cursorPositionChanged.connect(self.updateStatusBar)
        sub.setWidget(textEdit)
        sub.setAttribute(Qt.WA_DeleteOnClose)
        self.mdi.addSubWindow(sub)
        textEdit.setFont(QFont('Arial', 24))
        sub.show()
        self.setWindowTitle(f'多文档文本编辑器 - {file_name}')
        self.file_name = file_name
        self.updateStatusBar()

    def openFile_with_history(self):
        history = []
        try:
            with open('history.json', 'r', encoding='utf-8') as file:
                history = json.load(file)
        except FileNotFoundError:
            pass
        except json.JSONDecodeError:
            pass
        self.historyMenu = QMenu(self)
        if history:
            for file in history:
                file_name1 = file['file_name']
                file_time = file['open_time']
                action = QAction(f'{file_name1} {file_time}', self)
                action.triggered.connect(lambda checked, file_name=file_name1: self.openFile(file_name))
                self.historyMenu.addAction(action)
            self.openAct.setMenu(self.historyMenu)
        else:
            self.openAct.setMenu(self.historyMenu)
        self.historyMenu.addSeparator()
        self.openNewAct = QAction('打开新文件', self)
        self.openNewAct.triggered.connect(self.openFile)
        self.historyMenu.addAction(self.openNewAct)

    def saveFile(self):
        if self.file_name:
            activeSubWindow = self.mdi.activeSubWindow()
            if activeSubWindow:
                try:
                    # 获取textEdit的内容
                    # 刷新textEdit
                    textEdit = activeSubWindow.widget()
                    text = textEdit.toPlainText()
                    print(text)
                except Exception as e:
                    print(f"Error reading text: {e}")
                with open(self.file_name, 'w', encoding='utf-8') as file:
                    file.write(text)
                    print(file)
        else:
            self.saveAsFile()
        try:
            history = []
            try:
                with open('history.json', 'r', encoding='utf-8') as file:
                    history = json.load(file)
            except FileNotFoundError:
                pass
            except json.JSONDecodeError:
                pass
            if self.file_name:
                file_names = [file['file_name'] for file in history]
                if self.file_name not in file_names:
                    history.append({'file_name': self.file_name, 'open_time': time.strftime('%Y-%m-%d %H:%M:%S')})
                    with open('history.json', 'w', encoding='utf-8') as file:
                        json.dump(history, file)
                else:
                    for file in history:
                        if file['file_name'] == self.file_name:
                            file['open_time'] = time.strftime('%Y-%m-%d %H:%M:%S')
                            with open('history.json', 'w', encoding='utf-8') as file:
                                json.dump(history, file)
                print('保存成功')
        except Exception as e:
            pass
        try:
            self.openFile_with_history()
            self.setWindowTitle(f'多文档文本编辑器 - {self.file_name}')
        except Exception as e:
            pass

    def saveAsFile(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "另存为", "", "Text Files (*.txt);;All Files (*)",
                                                  options=options)
        self.file_name = fileName

    def setFont(self):
        activeSubWindow = self.mdi.activeSubWindow()
        if activeSubWindow:
            textEdit = activeSubWindow.widget()
            font, ok = QFontDialog.getFont()
            if ok:
                textEdit.setCurrentFont(font)
                self.updateStatusBar()

    def setBold(self):
        activeSubWindow = self.mdi.activeSubWindow()
        if activeSubWindow:
            textEdit = activeSubWindow.widget()
            if textEdit.fontWeight() == QFont.Bold:
                textEdit.setFontWeight(QFont.Normal)
            else:
                textEdit.setFontWeight(QFont.Bold)
            self.updateStatusBar()

    def setItalic(self):
        activeSubWindow = self.mdi.activeSubWindow()
        if activeSubWindow:
            textEdit = activeSubWindow.widget()
            state = textEdit.fontItalic()
            textEdit.setFontItalic(state)
            self.updateStatusBar()

    def updateStatusBar(self):
        activeSubWindow = self.mdi.activeSubWindow()
        if activeSubWindow:
            textEdit = activeSubWindow.widget()
            text = textEdit.toPlainText()
            word_count = len(text)
            selected_count = len(textEdit.textCursor().selectedText())
            font_size = textEdit.font().pointSize()
            self.wordCountLabel.setText(f'字数: {word_count}')
            self.selectedCountLabel.setText(f'选中字符数: {selected_count}')
            self.fontSizeLabel.setText(f'字号: {font_size}')

    def saveAsFile(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "另存为", "", "Text Files (*.txt);;All Files (*)",
                                                  options=options)
        if fileName:
            with open(fileName, 'w', encoding='utf-8') as file:
                text = self.textEdit.toPlainText()
                file.write(text)

    def undo(self):
        activeSubWindow = self.mdi.activeSubWindow()
        if activeSubWindow:
            textEdit = activeSubWindow.widget()
            textEdit.undo()

    def redo(self):
        activeSubWindow = self.mdi.activeSubWindow()
        if activeSubWindow:
            textEdit = activeSubWindow.widget()
            textEdit.redo()

    def selectAll(self):
        activeSubWindow = self.mdi.activeSubWindow()
        if activeSubWindow:
            textEdit = activeSubWindow.widget()
            textEdit.selectAll()

    def copy(self):
        activeSubWindow = self.mdi.activeSubWindow()
        if activeSubWindow:
            textEdit = activeSubWindow.widget()
            textEdit.copy()

    def cut(self):
        activeSubWindow = self.mdi.activeSubWindow()
        if activeSubWindow:
            textEdit = activeSubWindow.widget()
            textEdit.cut()

    def paste(self):
        activeSubWindow = self.mdi.activeSubWindow()
        if activeSubWindow:
            textEdit = activeSubWindow.widget()
            textEdit.paste()

    def search(self):
        activeSubWindow = self.mdi.activeSubWindow()
        if activeSubWindow:
            textEdit = activeSubWindow.widget()
            text = textEdit.toPlainText()
            search_text, ok = QInputDialog.getText(self, '搜索', '请输入要搜索的内容')
            if ok:
                index = text.find(search_text)
                if index != -1:
                    # 将搜索内容选中
                    cursor = textEdit.textCursor()
                    cursor.setPosition(index)
                    cursor.setPosition(index + len(search_text), QTextCursor.KeepAnchor)
                    textEdit.setTextCursor(cursor)

                else:
                    QMessageBox.information(self, '搜索', '未找到搜索内容')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = TextEditor()
    editor.show()
    sys.exit(app.exec_())
