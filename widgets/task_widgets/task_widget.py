from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QGridLayout, QVBoxLayout
from PyQt5.QtCore import Qt, QSize ,QDate
from PyQt5.QtGui import QPixmap

from file_manager.task_manager import TaskManger

class QuickTaskWidget(QWidget):
    def __init__(self, title : str , date : str , end_date : str , end_time : str, is_completed = False):
        super(QuickTaskWidget, self).__init__()
        self.is_complete = is_completed
        self.title = title
        self.date = QDate.fromString(date , "yyyy MMM dd")
        # create the base widget
        base = QWidget()
        base.setObjectName("main")

        # create the title label
        title_label = QLabel(title)
        title_label.setObjectName("title_label")

        start_date_label = QLabel(f"started on {date}")
        end_date_and_time_label = QLabel(f"end : {end_date}\nat {end_time}")

        start_date_label.setObjectName("date_label")
        end_date_and_time_label.setObjectName("date_label")

        is_completed_label = QLabel()
        is_completed_label.setObjectName("image_label")
        is_completed_label.setFixedSize(QSize(60, 50))
        is_completed_label.mousePressEvent = lambda e, l = is_completed_label : self.setAsComplete(l)
        if is_completed:
            is_completed_label.setPixmap(QPixmap("images/system_images/completed_oval.png").scaled(is_completed_label.size(),
                                        Qt.KeepAspectRatio, Qt.FastTransformation))
        else:
            is_completed_label.setPixmap(QPixmap("images/system_images/not_complete_oval.png").scaled(is_completed_label.size(),
                                        Qt.KeepAspectRatio, Qt.FastTransformation))

        # create the grid layout for pack the widgets
        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        grid.addWidget(is_completed_label, 0, 0, 2, 1)
        grid.addWidget(title_label, 0, 1, 1, 2)
        grid.addWidget(start_date_label, 1, 1)
        grid.addWidget(end_date_and_time_label, 1, 2)

        base.setLayout(grid)
        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(vbox)
        self.layout().addWidget(base)
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("""
                        QLabel#title_label {
                                    font-size : 24px;
                                    background : none;
                                    color : white;}
                                    
                        QLabel#image_label {
                                border-radius : 30px;
                                margin-left : 8px;}
                                
                        QLabel#image_label:hover {border : 2px solid blue;
                                                border-radius : 30px}
                        
                        QLabel#date_label {color : rgb(220, 200, 200);
                                            background : none;
                                            font-size : 13px;
                                            padding : 5px;}
                        
                        QWidget#main {background-color  : rgba(0, 0, 60, 0.5);
                                    border-bottom : 1px solid rgba(0, 10, 240, 0.8);
                                    padding-bottom : 5px;}
                                    
                        QWidget#main:hover {background-color : rgba(0, 20, 80, 0.7)}""")

    def setAsComplete(self, label : QLabel):

        # set the image label
        if not self.is_complete:
            label.setPixmap(QPixmap("images/system_images/completed_oval.png").scaled(label.size(), Qt.KeepAspectRatio ,
                                                                                Qt.FastTransformation))
            # set the json file attributes
            # create the task manager object
            task_manager = TaskManger()
            task_manager.setAsComplete(self.title , self.date)
