from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QComboBox, QGridLayout, QVBoxLayout, \
    QHBoxLayout, QSpinBox, QLineEdit
from PyQt5.QtCore import Qt, QDate, QTime, QSize, pyqtSignal
from PyQt5.QtGui import QColor, QFont, QIcon, QKeyEvent, QPixmap, QPalette

from file_manager.class_manager import ClassManager
from util.datetimeutil import DateTimeUtil

from style_sheets.calander_style_sheet import style_sheet

class ClassCard(QWidget):
    def __init__(self, name , grade : int , start_time , end_time):
        super(ClassCard, self).__init__()
        # create the name label
        name_label = QLabel(name)
        name_label.setObjectName("name_label")

        grade_label = QLabel(f"grade {grade}")
        grade_label.setObjectName("grade_label")

        time_label = QLabel(f"start from {start_time}\nend at {end_time}")
        time_label.setObjectName("time_label")

        title_label = QLabel("Class")
        title_label.setObjectName("title_label")

        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.addWidget(title_label)
        vbox.addWidget(name_label)
        vbox.addWidget(grade_label)
        vbox.addWidget(time_label)

        base = QWidget()
        base.setLayout(vbox)
        lyt = QHBoxLayout()
        lyt.setContentsMargins(0, 0, 0, 0)
        lyt.addWidget(base)
        self.setLayout(lyt)
        self.setContentsMargins(0, 0, 0, 0)

        self.setStyleSheet("""
            QWidget {background-color : rgb(0, 0, 150);
                    margin : 0px;
                    padding : 5px;
                    border : none;
                    border-bottom : 1px solid blue;}
                
            QLabel {background : none;
                    padding-left : 10px;
                    border : none;}
            
            QLabel#title_label {background-color : rgb(0, 20, 100);
                                color : white;
                                padding : 10px;
                                font-size : 18px;}
                                
            QLabel#name_label {
                                color : white;
                                font-family : verdana;
                                font-size : 40px;}
                                
            QLabel#grade_label {
                        font-size : 25px;}
                                
            QLabel#time_label {color : rgb(200, 200 ,250);
                                font-size : 18px;}
            
        """)

class Calander(QWidget):

    # declare the calander changed signal
    calendarChanged = pyqtSignal()

    def __init__(self):
        super(Calander, self).__init__()
        self.initializeUI()

    def initializeUI(self):

        # setup the configurations of ui and main design
        self.year = QDate.currentDate().year()
        self.month = QDate.currentDate().month()
        # list for day work labels
        self.day_work_labels = []

        # create the layouts for pack the widgets
        main_hbox = QHBoxLayout()
        main_hbox.setSpacing(0)
        main_hbox.setContentsMargins(0, 0, 0, 0)

        # create the grid for calander widgets and label for Present date text
        vbox = QVBoxLayout()
        # create the date tex label
        self.present_date_label = QLabel()

        # create the gird
        self.calanderGrid = QGridLayout()
        self.calanderGrid.setSpacing(0)
        self.calanderGrid.setVerticalSpacing(0)
        self.calanderGrid.setVerticalSpacing(0)
        self.calanderGrid.setContentsMargins(0, 0, 0, 0)


        vbox.addLayout(self.calanderGrid)
        vbox.addWidget(self.present_date_label)
        vbox.addStretch()

        # create the year and month layout
        self.select_hbox = QHBoxLayout()

        # create the widget for shedule panel
        self.shedulePanel = QWidget()
        # vbox for pack the hbo and widget
        vbox2 = QVBoxLayout()
        vbox2.addLayout(self.select_hbox)
        vbox2.addWidget(self.shedulePanel)
        vbox2.addStretch()

        main_hbox.addLayout(vbox)
        main_hbox.addLayout(vbox2)

        # call to the setup function for build the main UI components
        self.setUpCalanderGrid()
        self.setUpTodayLabel()
        self.setUpShedulePanel()
        self.setUpComboBoxes()


        self.calendarChanged.connect(self.updateCalendar)
        self.setObjectName("main_widget")
        self.setLayout(main_hbox)
        self.setStyleSheet(style_sheet)

    def setUpCalanderGrid(self):

        # first create the week day bar
        self.week_day_bar = []
        for i in range(1, 8):
            # get the week day
            dayName = DateTimeUtil.getWeekDay(i)
            # create the button for this
            button = QPushButton("{}".format(dayName)[0:2])
            button.setFixedSize(QSize(150, 100))
            button.setObjectName("weekDayButton")
            button.setContentsMargins(0, 0, 0, 0)
            # append to the list
            self.week_day_bar.append(button)
            # add to the grid
            self.calanderGrid.addWidget(button, 0, i - 1)

        self.dayButtons = []
        # draw the current month
        self.updateCalendar()



    def setUpTodayLabel(self):

        # get the today date
        date = QDate.currentDate()
        # get thee month string
        month = date.longMonthName(date.month())
        # get the week day name
        week_day_name = DateTimeUtil.getWeekDay(date.dayOfWeek())

        self.present_date_label.setText("{} {} of {} {}".format(date.day(), week_day_name , month, date.year()))

        # set the style name
        self.present_date_label.setObjectName("present_date_label")
        self.present_date_label.setMinimumHeight(150)

    def setUpShedulePanel(self):

        self.shedulePanel.setFixedWidth(500)
        # create the clicked date label
        self.clickedDateLabel = QLabel()
        self.clickedDateLabel.setObjectName("clickedDateLabel")

        # create the vbox fo the shedule panel
        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)
        vbox.addWidget(self.clickedDateLabel)
        vbox.addStretch()

        self.shedulePanel.setLayout(vbox)


    def setUpComboBoxes(self):

        # create the arrow buttons
        backButton = QPushButton("<")
        forwardButton = QPushButton(">")

        backButton.setObjectName("arrowButton")
        forwardButton.setObjectName("arrowButton")

        backButton.pressed.connect(self.backToCalendar)
        forwardButton.pressed.connect(self.forwardToCalendar)

        # create the two labels and tow combo box for manage it
        self.yearLabel = QLabel(f"{self.year}")
        self.monthLabel = QLabel("{}".format(QDate.longMonthName(self.month)))
        self.yearLabel.setObjectName("yearLabel")
        self.monthLabel.setObjectName("monthLabel")

        # create the combo boc for month select
        month_combo_box = QComboBox()
        month_combo_box.addItems([QDate.longMonthName(i) for i in range(1, 13)])
        month_combo_box.setVisible(False)

        # create the year spin boc
        self.yearBox = QLineEdit()
        self.yearBox.setText(f"{self.year}")
        self.yearBox.setVisible(False)

        # create the hbox for pack the all of widgets
        self.select_hbox.setContentsMargins(0, 0, 0, 0)
        self.select_hbox.addWidget(backButton)
        self.select_hbox.addWidget(self.yearLabel)
        self.select_hbox.addWidget(self.yearBox)
        self.select_hbox.addWidget(self.monthLabel)
        self.select_hbox.addWidget(month_combo_box)
        self.select_hbox.addWidget(forwardButton)

        # create the actions
        self.yearLabel.mousePressEvent = lambda e, w = self.yearBox : self.yearLabelPressed(w)
        self.monthLabel.mousePressEvent = lambda e, w = month_combo_box : self.MonthLabelPressed(w)

        month_combo_box.currentIndexChanged.connect(lambda m , e = month_combo_box : self.changeMonth(m, e))
        self.yearBox.returnPressed.connect(self.changeYear)

    def changeMonth(self, index : int, widget : QWidget):

        self.month = index + 1

        self.monthLabel.setText(QDate.longMonthName(index + 1))
        self.monthLabel.setVisible(True)
        self.monthLabel.setVisible(True)
        widget.setVisible(False)

        self.calendarChanged.emit()

    def changeYear(self):

        self.year = int(self.yearBox.text())
        self.yearLabel.setText(f"{self.year}")

        self.yearBox.setText(f"{self.year}")
        self.yearLabel.setVisible(True)
        self.yearBox.setVisible(False)

        self.calendarChanged.emit()

    def yearLabelPressed(self, widget : QWidget):

        self.yearLabel.setVisible(False)
        widget.setVisible(True)
        widget.setFocus()

    def MonthLabelPressed(self, widget : QWidget):

        self.monthLabel.setVisible(False)
        widget.setVisible(True)

    def updateCalendar(self):

        for widget in self.dayButtons:
            widget.deleteLater()

        self.dayButtons = []
        for i in range(1, QDate.currentDate().daysInMonth() + 1):
            # get the day of week
            day_of_week = QDate(self.year, self.month, i).dayOfWeek()
            # create the  button
            button = QPushButton(f"{i}")
            button.pressed.connect(lambda e = i : self.updateDate(e))
            button.setFixedSize(QSize(150, 120))
            button.setContentsMargins(0, 0, 0, 0)
            button.setWindowOpacity(0.8)
            # append to the list
            self.dayButtons.append(button)
            # add to the grid
            self.calanderGrid.addWidget(button, QDate(self.year, self.month, i).weekNumber()[0], day_of_week - 1)

            if (QDate(self.year , self.month , i) == QDate.currentDate()):
                button.setObjectName("dayButtonToday")
            else:
                button.setObjectName("dayButton")

    def updateDate(self, day : int):

        date = QDate(self.year, self.month, day)
        # set the date text of the clicked date label
        self.clickedDateLabel.setText("{} {} of {} {}".format(day , DateTimeUtil.getWeekDay(date.dayOfWeek()),
                                                              date.longMonthName(self.month), self.year))

        # fill the day works
        self.fillDayWorks(QDate(self.year , self.month , day))

    def fillDayWorks(self, date : QDate):

        [widget.deleteLater() for widget in self.day_work_labels]
        self.day_work_labels.clear()

        # get the class of this day
        cls_manager = ClassManager()
        cls_data = cls_manager.getTimesFromDay(date.dayOfWeek())

        for cls in cls_data:
            # create the cls widget
            cls_card = ClassCard(cls["className"], cls["grade"], cls["start_time"], cls["end_time"])
            self.day_work_labels.append(cls_card)
            self.shedulePanel.layout().addWidget(cls_card)


    def backToCalendar(self):

        if self.month != 1:
            self.month -= 1
        else:
            self.month = 12
            self.year -= 1

        # change the Label and fire the signal
        self.yearLabel.setText(f"{self.year}")
        self.monthLabel.setText(f"{QDate.longMonthName(self.month)}")

        self.calendarChanged.emit()

    def forwardToCalendar(self):

        if (self.month != 12):
            self.month += 1
        else:
            self.month = 1
            self.year += 1

        # change the Label and fire the signal
        self.yearLabel.setText(f"{self.year}")
        self.monthLabel.setText(f"{QDate.longMonthName(self.month)}")

        self.calendarChanged.emit()
