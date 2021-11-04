from PyQt5.QtWidgets import (QApplication, QWidget, QScrollArea, QLabel, QListWidget, QPushButton, QVBoxLayout,
                             QHBoxLayout, QGridLayout)
from PyQt5.QtCore import QSize, Qt, QTime
from PyQt5.QtGui import QColor, QFont, QPainter
#
from dialogs.class_time_dialog import ClassTimeDialog
from file_manager.class_manager import ClassManager
from style_sheets.time_table_style_sheet import style_sheet

db_file = "./db/main.db"
time_file = "./db/class_times.json"

class TimeWidget(QWidget):
    def __init__(self, class_name : str , grade : int , x1 : int , x2 : int, week_day : int, parent = None):
        super(TimeWidget, self).__init__(parent)
        self.class_name = class_name
        self.grade = grade
        self.x1 = x1
        self.x2 = x2
        self.day = week_day

        # cretae the base widget
        base = QWidget()
        base.setContentsMargins(0, 0, 0, 0)
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.addWidget(base)

        self.setContentsMargins(0, 0, 0, 0)
        # create the two labels for name and grade
        name_label = QLabel(self.class_name)
        name_label.setFont(QFont("verdana", 16))
        name_label.setWindowOpacity(1.0)
        name_label.setWordWrap(True)

        grade_label = QLabel(f"Grade {self.grade}")
        grade_label.setFont(QFont("verdana", 13))
        grade_label.setWordWrap(True)

        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.addWidget(name_label)
        vbox.addWidget(grade_label)
        base.setLayout(vbox)

        self.setLayout(hbox)
        base.setObjectName("classButton")

        self.setStyleSheet("""
                    
                    QLabel {
                        padding  : 20px;}
                    
                    QWidget#classButton {background-color : rgb(230, 160, 20);
                                            border : 1px solid rgb(200, 200, 200);
                                            color  : black;
                                            font-size : 16px}
                    
                                            
                    QWidget#classButton:hover {background-color : rgb(250, 200, 10)}""")



class TimeTableWidget(QWidget):

    week_days = ["Monday", "TuesDay", "WednesDay", "ThursDay", "FriDay", "SaturDay", "Sunday"]

    def __init__(self):
        super(TimeTableWidget, self).__init__()
        self.initializeUI()
        self.setStyleSheet(style_sheet)
        self.resize(2000, 1000)

    def initializeUI(self):

        # divide the widget to two space
        self.class_box = QVBoxLayout()
        # create the main widget
        self.main_widget = QWidget()
        self.main_widget.setContentsMargins(0, 0, 0, 0)
        self.main_widget.resize(2000, 1500)

        # create the scroll widge tfor pack the main widgets
        scroll_area = QScrollArea()
        scroll_area.setWidget(self.main_widget)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.display_widget = QWidget()

        # create the vbox for pack the scroll and display widgets
        vbox = QVBoxLayout()
        vbox.addWidget(scroll_area)
        vbox.addWidget(self.display_widget)

        # create the hbox for divide hte space
        hbox = QHBoxLayout()
        hbox.setSpacing(50)
        hbox.setContentsMargins(0, 0, 0, 50)

        hbox.addLayout(vbox)
        hbox.addLayout(self.class_box)

        self.setLayout(hbox)

        self.setUpMainWidget()
        self.setUpClassBox()
        self.setUpDisplayWidget()

    def setUpClassBox(self):

        # create the class object for this
        class_manager = ClassManager()
        # get the class names
        class_names  = class_manager.getClassNames(db_file)
        self.grades = class_manager.getGrades(db_file)

        # create the list widget of this items
        self.classNamesBox = QListWidget()
        self.classNamesBox.setMaximumWidth(350)
        self.classNamesBox.itemClicked.connect(lambda e : self.time_add_button.setEnabled(True))
        self.classNamesBox.addItems(class_names)

        # create the button fot add the times for class
        self.time_add_button = QPushButton("Add Times")
        self.time_add_button.pressed.connect(self.addTime)
        self.time_add_button.setEnabled(False)

        self.class_box.addWidget(self.classNamesBox)
        self.class_box.addWidget(self.time_add_button)


    def setUpDisplayWidget(self):

        # create the class data labels
        self.class_name_label = QLabel()
        self.class_name_label.setWordWrap(True)
        self.grade_label = QLabel()
        self.start_time_label = QLabel()
        self.end_time_label = QLabel()

        for label in [self.class_name_label, self.grade_label, self.start_time_label, self.end_time_label]:
            label.setFont(QFont("verdana", 23))

        label = []
        for text in ["Class Name", "Grade", "Start Time", "End Time"]:
            lb = QLabel(text)
            lb.setFont(QFont('verdana', 13))
            label.append(lb)

        grid = QGridLayout()
        grid.setVerticalSpacing(20)

        grid.addWidget(label[0], 0, 0)
        grid.addWidget(label[1], 0, 1)
        grid.addWidget(label[2], 0, 2)
        grid.addWidget(label[3], 0, 3)

        grid.addWidget(self.class_name_label, 1, 0)
        grid.addWidget(self.grade_label, 1, 1)
        grid.addWidget(self.start_time_label, 1, 2)
        grid.addWidget(self.end_time_label, 1, 3)

        self.display_widget.setLayout(grid)

    def setUpMainWidget(self):

        # declared the main parameters
        self.width = 200
        self.height = 40
        self.begin_x = 150
        self.begin_y = 50

        # declare the all of buttons lists
        self.week_name_buttons = []
        self.time_range_labels = []
        self.hour_label = []
        self.minute_labels = []

        # first place the week buttons
        for i, name in enumerate(self.week_days):
            label = QLabel(name, self.main_widget)
            label.setObjectName("week_title_label")
            label.setFixedSize(QSize(self.width, 60))
            # add to the list
            self.week_name_buttons.append(label)
            # move the buttons
            label.move(self.begin_x + i * self.width , self.begin_y - label.height())


        # create the two range for time
        time_ranges = [range(6, 13), range(1, 13)]
        time_range_names = ["AM", "PM"]
        h = [0, self.height * 2 * len(time_ranges[0])]

        i = 0
        k = 0
        for name in range(len(time_range_names)):
            # create the label and sett them
            name_label = QLabel(time_range_names[name], self.main_widget)
            name_label.setObjectName("time_range_label")
            name_label.setFixedSize(QSize(50, self.height * 2 * len(time_ranges[name])))
            # add to the list
            self.time_range_labels.append(name_label)
            name_label.move(self.begin_x - 110 - name_label.width(), self.begin_y + h[name])

            for hour in time_ranges[name]:
                label = QLabel("{:2d}".format(hour), self.main_widget)
                label.setObjectName("hour_label")
                label.setFixedSize(QSize(60, self.height * 2))
                label.setAlignment(Qt.AlignTop)
                label.move(self.begin_x - label.width() - 50, self.begin_y + k * 2 * self.height)

                self.hour_label.append(label)
                k += 1

                for minute in [0, 30]:
                    label = QLabel("{:2d}".format(minute), self.main_widget)
                    label.setObjectName("minute_label")
                    label.setFixedSize(QSize(70, self.height))
                    label.setAlignment(Qt.AlignTop)
                    # add to list
                    self.minute_labels.append(label)
                    label.move(self.begin_x - label.width() - 2, self.begin_y + i * self.height)
                    i += 1

        # create the empty labels
        for i in range(len(self.week_name_buttons)):
            for j in range(len(self.minute_labels) // 2):
                button = QPushButton(self.main_widget)
                button.setObjectName("timeButton")
                button.setFixedSize(QSize(self.width, self.height * 2))
                button.move(self.begin_x + i * self.width, self.begin_y + j * self.height * 2)

        # create the buttons list
        self.time_button_list = []
        self.updateTable()


    def addTime(self):

        # get the class id first
        # create the class manager
        class_manager = ClassManager()
        cls_id = class_manager.getID(self.classNamesBox.currentItem().text() ,
                                     self.grades[self.classNamesBox.currentIndex().row()], db_file)

        # create the dialog
        self.dialog = ClassTimeDialog(cls_id, self)

        if self.dialog.exec_():
            self.updateTable()

    def updateTable(self):

        # create the class manager
        class_manager = ClassManager()
        class_names_grades = class_manager.getClassWithGrades(db_file)

        for class_, grade  in class_names_grades:
            # get the id
            class_id = class_manager.getID(class_, grade, db_file)
            times = class_manager.getClassTimes(class_id, time_file)

            # draw on the table
            for time in times:
                # move to right place
                start_time = time["start_time"]
                end_time = time["end_time"]

                diff = TimeTableWidget.times_sub(end_time, start_time)
                h = diff.hour() * 2 + int(diff.minute() / 30)
                height = diff.hour() * 2 * self.height + int(diff.minute() / 30  * self.height)

                diff2 = TimeTableWidget.times_sub(start_time , QTime(6, 0))
                x1 = diff2.hour() * 2 + int(diff2.minute() / 30)
                start_y = diff2.hour() * 2 * self.height + int(diff2.minute() / 30  * self.height)

                # create the button
                button = TimeWidget(class_, grade, x1, x1 + h, time["week_day"],self.main_widget)
                button.setFixedSize(QSize(self.width, height))
                button.move(self.begin_x + self.width * (time["week_day"] - 1) , self.begin_y + start_y)
                # add tolist
                self.time_button_list.append(button)
                button.setObjectName("classButton")

                button.mousePressEvent = lambda e , x1 = button.x1 , x2 = button.x2, \
                                            name = button.class_name , d = time["week_day"],g = button.grade \
                                            ,t1 = start_time, t2 = end_time, \
                                            : self.highlightButton(x1 , x2, d ,name, g, t1, t2)

    def highlightButton(self, x1, x2, day , name, grade, start_time : QTime , end_time : QTime):

        for i in range(len(self.minute_labels)):
            if i <= x2 and i >= x1:
                self.minute_labels[i].setStyleSheet("""
                                                    QLabel {background-color : rgb(250, 130, 0);
                                                    font-weight : bold;
                                                    border  : 1px solid orange}""")
            else:
                self.minute_labels[i].setStyleSheet("""
                                    QLabel {background-color : rgb(0, 200, 50);
                                        color  : black;
                                        padding : 7px;
                                        border : 1px solid rgb(0, 200, 10);
                                        font-size : 15px;}""")

        for i in range(len(self.hour_label)):
            if (i <= x2//2 and i >= x1//2):
                self.hour_label[i].setStyleSheet("""
                                                QLabel {background-color  : rgb(250, 130, 0);
                                                font-weight : bold;
                                                border : 1px solid orange}""")
            else:
                self.hour_label[i].setStyleSheet("""
                                    QLabel {background-color : rgb(0, 250, 20);
                                        border : 1px solid rgb(0, 200, 0);
                                        padding : 7px;
                                        font-family : verdana;
                                        font-size : 16px;}""")

        for i in range(len(self.week_name_buttons)):
            if i == day - 1:
                self.week_name_buttons[i].setStyleSheet("""
                                                QLabel {background-color  : rgb(250, 130, 0);
                                                        font-weight : bold}""")
            else:
                self.week_name_buttons[i].setStyleSheet("""
                                    QLabel {background : none;
                                            padding : 40px;
                                            font-size : 17px;}""")

        self.class_name_label.setText(name)
        self.grade_label.setText(f"{grade}")
        self.start_time_label.setText(start_time.toString("hh:mm A"))
        self.end_time_label.setText(end_time.toString("hh:mm A"))

    @staticmethod
    def times_sub(time1 : QTime, time2 : QTime):

        if (time1 < time2):
            raise IndexError()

        minute = 0
        hour = 0

        if (time1.minute()< time2.minute()):
            minute = 60 + time1.minute() - time2.minute()
            hour = time1.hour() - time2.hour() - 1
        else:
            minute = time1.minute() - time2.minute()
            hour = time1.hour() - time2.hour()

        return QTime(hour, minute)




if __name__ == "__main__":
    app = QApplication([])
    app.setStyleSheet("""
    
                    QLabel#time_range_label {background-color : rgb(0, 220, 70);
                                        border : 1px solid rgb(0, 200,0);
                                        padding : 7px;
                                        font-size : 17px;}
                    
                    QLabel#hour_label {background-color : rgb(0, 250, 20);
                                        border : 1px solid rgb(0, 200, 0);
                                        padding : 7px;
                                        font-family : verdana;
                                        font-size : 16px;}
                    
                    QLabel#minute_label {background-color : rgb(0, 200, 50);
                                        color  : black;
                                        padding : 7px;
                                        border : 1px solid rgb(0, 200, 10);
                                        font-size : 15px;}
                                        
                    QLabel#week_title_label {background : none;
                                            padding : 40px;
                                            font-size : 17px;}
                    
    
                    QPushButton#timeButton {
                                        border : 1px solid rgb(200, 200, 200);}
                                        
                    QWidget#classButton {background-color : rgb(230, 160, 20);
                                            border : 1px solid rgb(200, 200, 200);
                                            color  : black;
                                            font-size : 16px}
                                            
                    QWidget#classButton:hover {background-color : rgb(200, 50, 10)}""")
    window = TimeTableWidget()
    window.show()

    app.exec_()