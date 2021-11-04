from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QFormLayout, QPushButton, \
    QMessageBox)
from PyQt5.QtCore import Qt, QSize, QTime

from file_manager.class_manager import ClassManager


class ClassTimeDialog(QDialog):

    week_days = ["Monday", "TuesDay", "WednesDay", "ThursDay", "FriDay", "SaturDay", "Sunday"]

    def __init__(self, cls_id : int, parent = None):
        super(ClassTimeDialog, self).__init__(parent)
        self.setFixedSize(QSize(250, 250))
        self.setWindowTitle("Class Time Dialog")
        self.cls_id = cls_id

        self.initializeUI()
        self.show()

    def initializeUI(self):

        # create the combo box of days
        self.days_box = QComboBox()
        self.days_box.addItems(self.week_days)
        self.days_box.setCurrentIndex(0)

        # create the start time box
        start_time_box = QHBoxLayout()

        self.start_hour  = QComboBox()
        self.start_hour.addItems([str(i) for i in range(1, 13)])
        self.start_minutes = QComboBox()
        self.start_minutes.addItems([str(i) for i in (0, 15, 30, 45)])

        self.start_type = QComboBox()
        self.start_type.addItems(["AM", "PM"])

        start_time_box.addWidget(self.start_hour)
        start_time_box.addWidget(QLabel(" : "))
        start_time_box.addWidget(self.start_minutes)
        start_time_box.addSpacing(15)
        start_time_box.addWidget(self.start_type)


        # create the start time box
        end_time_box = QHBoxLayout()

        self.end_hour = QComboBox()
        self.end_hour.addItems([str(i) for i in range(1, 13)])

        self.end_minutes = QComboBox()
        self.end_minutes.addItems([str(i) for i in (0, 15, 30, 45)])

        self.end_type = QComboBox()
        self.end_type.addItems(["AM", "PM"])

        end_time_box.addWidget(self.end_hour)
        end_time_box.addWidget(QLabel(" : "))
        end_time_box.addWidget(self.end_minutes)
        end_time_box.addSpacing(15)
        end_time_box.addWidget(self.end_type)

        # create the form for pack the widget
        form = QFormLayout()
        form.setVerticalSpacing(25)
        form.setFormAlignment(Qt.AlignCenter)
        form.setLabelAlignment(Qt.AlignRight)

        form.addRow("Day", self.days_box)
        form.addRow("Start Time" , start_time_box)
        form.addRow("End Time", end_time_box)

        # create the buttons
        save_button = QPushButton("Save")
        close_button = QPushButton("Cancel")

        save_button.pressed.connect(self.accept)
        close_button.pressed.connect(self.reject)

        hbox = QHBoxLayout()
        hbox.addWidget(save_button)
        hbox.addWidget(close_button)

        vbox  = QVBoxLayout()
        vbox.addLayout(form)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def accept(self) -> None:

        # get the data from the widgets
        week_day = self.days_box.currentIndex()

        s_hour = int(self.start_hour.currentText()) if self.start_type.currentText() == "AM" \
                                                    else int(self.start_hour.currentText()) + 12
        e_hour = int(self.end_hour.currentText()) if self.end_type.currentText() == "AM" \
                                                    else int(self.end_hour.currentText()) + 12

        start_time = QTime(s_hour, int(self.start_minutes.currentText()))
        end_time = QTime(e_hour, int(self.end_minutes.currentText()))


        if (end_time <= start_time):
            self.end_hour.setFocus()
            return

        # update the class json file
        # create the class manager object
        class_mng = ClassManager()
        if (class_mng.isCrashTime(week_day + 1, start_time, end_time)):
            # display the warning message
            QMessageBox.warning(self, "Class Time Crash",
                                "Your Times is Crashes the Other Classes times...please Change time or day",
                                QMessageBox.StandardButton.Ok)
            self.days_box.setCurrentIndex(0)
            return

        class_mng.addTimeForClass(self.cls_id, week_day + 1, start_time, end_time)

        QMessageBox.information(self, "Class Time Added", "Your Class Time Added Successfull", QMessageBox.StandardButton.Ok)
        super().accept()