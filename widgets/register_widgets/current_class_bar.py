import os

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QHBoxLayout, QGridLayout, QVBoxLayout
from PyQt5.QtCore import Qt, QSize, QTime, QDate, pyqtSignal

from file_manager.class_manager import ClassManager

class ClassButton(QPushButton):
    def __init__(self, cls_id : int, week_day : int = 1):
        super(ClassButton, self).__init__()
        self.cls_id = cls_id
        if week_day > 7:
            raise IndexError
        self.week_day = week_day

        self.loadData()
        self.initiateUI()

    def loadData(self):

        cls_manager = ClassManager()
        # load the data from the cls_manager object
        self.class_name = cls_manager.get(self.cls_id, "className")
        self.grade = int(cls_manager.get(self.cls_id , "grade"))

        times = cls_manager.getClassTimes(self.cls_id)

        self.start_time  : QTime = None
        self.last_time  : QTime = None

        for time in times:
            if time["week_day"] == self.week_day:
                self.start_time = times[0]["start_time"]
                self.last_time = times[0]["end_time"]
                break


    def initiateUI(self):

        self.setMinimumHeight(270)
        self.setMaximumWidth(550)

        name_label = QLabel(self.class_name)
        name_label.setWordWrap(True)
        name_label.setObjectName("name_label")

        grade_label = QLabel(f"grade {self.grade}")
        grade_label.setFont(QFont('verdana', 14))

        start_time_label = QLabel(f"start time : {self.start_time.toString('hh:mm A')}")
        end_time_label = QLabel(f"end time : {self.last_time.toString('hh:mm A')}")

        for label in [start_time_label, end_time_label]:
            label.setFont(QFont("verdana", 12))

        # pack the buttons
        vbox = QVBoxLayout()

        vbox.addWidget(name_label)
        vbox.addWidget(grade_label)
        vbox.addSpacing(20)
        vbox.addWidget(start_time_label)
        vbox.addWidget(end_time_label)

        self.setLayout(vbox)
        self.setToolTipDuration(500)

        self.setStyleSheet("""
        
                    QPushButton {background-color  :rgb(0, 0, 150);}
                    
                    QPushButton:hover {background-color  : rgb(0, 0, 180);}
                    
                    QPushButton:pressed {background-color  :rgb(0, 0, 200;)}
                    
                    QLabel {font-family : verdana;
                            font-size: 22px;}
                      
                    QLabel#name_label {font-size : 35px;
                                        font-weight : bold;
                                        color  : rgb(0, 200, 250);}
                    
                    
                    
                    QLabel {color : white;
                            background : none;}
                            
                    
        
                        """)

    def toolTip(self) -> str:
        return f"{self.class_name} for grade {self.grade}"


class ClassBar(QWidget):

    registor_signal = pyqtSignal(int)

    def __init__(self):
        super(ClassBar, self).__init__()
        self.weeK_day = QDate().currentDate().dayOfWeek()

        cls_manager = ClassManager()
        cls_ids = cls_manager.getClassIDFromWeekDay(self.weeK_day)

        # get the current started class ids
        started_class_files = os.listdir("db/classes")
        started_ids = [int(file.split("@")[1]) for file in started_class_files]

        hbox = QHBoxLayout()
        hbox.setSpacing(20)
        for id in cls_ids:
            if int(id) in started_ids:
                # create the class card widgets
                cls_widget = ClassButton(id, self.weeK_day)
                cls_widget.pressed.connect(lambda e = id : self.openRegister(e))

                hbox.addWidget(cls_widget)

        base  = QWidget()
        base.setObjectName("base")
        base.setLayout(hbox)

        self.setLayout(QHBoxLayout())
        self.layout().addWidget(base)

        self.setStyleSheet("""
                        QWidget#base {border-bottom : 2px solid rgb(100, 100, 150);
                                    margin : 0px;}""")

    def openRegister(self, id : int):

        self.registor_signal.emit(id)