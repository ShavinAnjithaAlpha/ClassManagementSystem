from PyQt5.QtWidgets import (QWidget, QLabel, QHBoxLayout, QVBoxLayout)
from PyQt5.QtCore import Qt, QTime, QTimer, QSize, QDate, QTimerEvent

from file_manager.class_manager import ClassManager

class_time_file = "db/class_times.json"

class DailyClassBar(QWidget):
    def __init__(self, parent = None):
        super(DailyClassBar, self).__init__(parent)
        # create the timer
        self.timer = QTimer()
        # arrange the class times bars
        # create the class manager object for get classes
        cls_manager = ClassManager()

        # get the week day
        day_of_week = QDate().currentDate().dayOfWeek()
        classes = cls_manager.getTimesFromDay(day_of_week, class_time_file)

        self.setLayout(QVBoxLayout())

        self.widgets = []
        for item in classes:
            st_time = QTime.fromString(item["start_time"], "hh:mm")
            en_time = QTime.fromString(item["end_time"], "hh:mm")
            widget = TimeBar_(item["className"], item["grade"], st_time, en_time)

            self.widgets.append(widget)
            self.layout().addWidget(widget)

        self.timer.startTimer(1000)
        self.timer.timeout.connect(self.updateWidgets)

    def updateWidgets(self):

        for widget in self.widgets:
            widget.updateTimerLabel()

class TimeBar_(QWidget):
    def __init__(self, class_name : str , grade : int , start_time : QTime, end_time : QTime):
        super(TimeBar_, self).__init__()
        self.setFixedSize(QSize(600, 100))

        self.start_time = start_time
        self.end_time = end_time

        self.status_label = QLabel()
        self.status_label.setFixedSize(QSize(50, 100))
        self.status_label.setStyleSheet("""
                                QLabel {background-color  :red;}""")

        # create the labels
        title_label = QLabel(class_name)
        title_label.setObjectName("title_label")

        grade_label = QLabel(f"grade {grade}")
        grade_label.setObjectName("grade_label")

        start_time_label = QLabel("from\n{}".format(start_time.toString("hh mm A")))
        end_time_label = QLabel("to\n{}".format(end_time.toString("hh mm A")))

        start_time_label.setObjectName("time_label")
        end_time_label.setObjectName("time_label")

        self.timer_label = QLabel()
        self.timer_label.setObjectName("timer_label")
        self.updateTimerLabel()

        # pack the all of labels
        vbox1 = QVBoxLayout()
        vbox1.addWidget(title_label)
        vbox1.addWidget(grade_label)

        vbox2 = QVBoxLayout()
        vbox2.addWidget(start_time_label)
        vbox2.addWidget(end_time_label)

        hbox = QHBoxLayout()
        hbox.addWidget(self.status_label)
        hbox.addLayout(vbox1)
        hbox.addLayout(vbox2)
        hbox.addWidget(self.timer_label)
        hbox.setContentsMargins(0, 0, 0, 0)

        base = QWidget()
        base.setObjectName("base")
        self.setLayout(QVBoxLayout())

        base.setLayout(hbox)
        self.layout().addWidget(base)
        self.layout().setContentsMargins(0, 0 ,0, 0)

        self.setContentsMargins(0, 0, 0, 0)

        self.setStyleSheet("""
        
                QWidget#base {background-color : rgba(0, 0 ,100, 0.7);
                        margin : 0px;
                        border-radius : 5px;}
                        
                QLabel {background : none;
                        color : white;}
                
                QLabel#title_label {background : none;
                                    font-size : 32px;}
                                    
                QLabel#grade_label {background : none;
                                    font-size : 18px;}
                                    
                QLabel#timer_label {background-color : rgba(0, 150, 250, 0.5);
                                    font-size : 32px;
                                    color : rgb(0, 0, 50)}
                
                QLabel#time_label {font-size : 16px;}
        """)

    def updateTimerLabel(self):

        current_time = QTime.currentTime()
        if current_time < self.start_time and current_time < self.end_time:
            h = self.start_time.hour() - current_time.hour()
            m = abs(self.start_time.minute() - current_time.minute())

            self.timer_label.setText("{:02d}:{:02d}".format(h, m))


        elif current_time > self.start_time and current_time > self.end_time:
            if not self.timer_label.isHidden():
                self.timer_label.hide()
            self.status_label.setStyleSheet("""
                                QLabel {background-color : rgb(0, 250, 100);}""")

        else:
            if not self.timer_label.isHidden():
                self.timer_label.hide()
            self.status_label.setStyleSheet("""
                                QLabel {background-color : yellow}""")