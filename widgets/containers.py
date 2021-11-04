from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout)
from PyQt5.QtCore import pyqtSignal, Qt, QSize
from PyQt5.QtGui import QFont, QIcon


class ContainerWidget(QWidget):
    def __init__(self, widget : QWidget , title  : str):
        super(ContainerWidget, self).__init__()
        self.title = title
        self.widget = widget

        # create the back button
        back_button = QPushButton()
        back_button.setIcon(QIcon("images/system_images/back.png"))
        back_button.setIconSize(QSize(70, 70))
        back_button.setObjectName("notRoundButton")
        back_button.pressed.connect(self.deleteLater)
        back_button.setStyleSheet("""
                                QPushButton {background-color  : rgb(0, 0, 100);
                                            padding : 20px;
                                            font-size : 30px;}
                                            
                                QPushButton:hover , QPushButton:pressed {background-color : rgb(0, 50, 100)}""")

        # create the title label
        title_label = QLabel(self.title)
        title_label.setFont(QFont('verdana', 23))
        title_label.setStyleSheet("""
                                    QLabel {background-color : rgb(0, 30, 150);
                                            color : white;
                                            padding-left : 100px;}
                                    
                                    """)

        # create the h box for upper bar
        upper_box = QHBoxLayout()
        upper_box.addWidget(back_button, stretch= 2)
        upper_box.addWidget(title_label, stretch=8)

        # create the vbox for pack the all of thid
        vbox = QVBoxLayout()
        vbox.setSpacing(0)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.addLayout(upper_box)
        vbox.addWidget(self.widget)

        self.setLayout(vbox)
