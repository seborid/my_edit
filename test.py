import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar, QAction, QMenu, QToolButton
from PyQt5.QtCore import Qt

class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.toolbar = self.addToolBar('Main Toolbar')

        # Create a dropdown menu
        self.menu = QMenu(self)
        option1 = QAction('Option 1', self)
        option1.triggered.connect(self.option1_function)
        self.menu.addAction(option1)

        option2 = QAction('Option 2', self)
        option2.triggered.connect(self.option2_function)
        self.menu.addAction(option2)

        option3 = QAction('Option 3', self)
        option3.triggered.connect(self.option3_function)
        self.menu.addAction(option3)

        # Create a tool button with a dropdown menu
        self.toolButton = QToolButton(self)
        self.toolButton.setText('Dropdown')
        self.toolButton.setMenu(self.menu)
        self.toolButton.setPopupMode(QToolButton.InstantPopup)

        # Add the tool button to the toolbar
        self.toolbar.addWidget(self.toolButton)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Toolbar with Dropdown Menu')
        self.show()

    def option1_function(self):
        pass
    def option2_function(self):
        pass
    def option3_function(self):
        pass
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())