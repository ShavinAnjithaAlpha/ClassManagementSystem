from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QListWidget, QListWidgetItem, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, \
    QGridLayout, QCheckBox, QMessageBox
from PyQt5.QtCore import Qt, QSize, QDate, QTime

from file_manager.class_utils import ClassInitializer
from file_manager.student_manager import StudentManager
from file_manager.class_manager import ClassManager

from style_sheets.register_style_sheet import style_sheet

class RegisterWidget(QWidget):
    def __init__(self, cls_id : int , year : int):
        super(RegisterWidget, self).__init__()
        self.cls_id, self.year = cls_id, year
        self.saveStatus = False

        # load the students for mark the register
        self.loadStudents()

        # create the title bar of the widget
        title_bar = QHBoxLayout()
        self.createTitleBar(title_bar)


        self.studentListWidget = QListWidget()
        # create the register content of the widget
        # create the list widget
        for student in self.student_names:
            check_button = QCheckBox(student[1])
            check_button.stateChanged.connect(self.updateValue)
            check_button.setMinimumHeight(50)

            listWidgetItem = QListWidgetItem(self.studentListWidget)
            self.studentListWidget.setItemWidget(listWidgetItem, check_button)



        info_bar = QGridLayout()
        self.createInfoBar(info_bar)

        # create the submit button
        submit_button = QPushButton("Submit Register")
        submit_button.pressed.connect(self.saveRegister)

        # create the register close button
        close_button = QPushButton("Close Register")
        close_button.pressed.connect(self.closeRegister)

        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(submit_button)
        hbox.addWidget(close_button)

        # create the main layout
        vbox = QVBoxLayout()
        vbox.addLayout(title_bar)
        vbox.addWidget(self.studentListWidget)
        vbox.addLayout(info_bar)
        vbox.addLayout(hbox)

        self.setLayout(vbox)
        self.setStyleSheet(style_sheet)

    def loadStudents(self):

        # get the students from the json file for this class
        class_manager = ClassInitializer()
        student_ids = class_manager.getClassStudents(self.cls_id, self.year)

        # get the student full name from the student ids
        std_manager = StudentManager()

        # get the student firstName list

        first_names = std_manager.gets(list(map(int, student_ids)), "firstName")
        last_names = std_manager.gets(list(map(int, student_ids)), "lastName")

        # combined the names to unique list
        self.student_names = [(student_ids[i] ,f"{first_names[i]} {last_names[i]}") for i in range(len(first_names))]

    def createTitleBar(self, layout : QHBoxLayout):


        # create the class manager for this
        cls_manager = ClassManager()
        name = cls_manager.get(self.cls_id, "className")
        grade = int(cls_manager.get(self.cls_id, "grade"))

        name_label = QLabel(name)
        name_label.setObjectName("name_label")


        grade_label = QLabel(f"grade {grade}")
        grade_label.setObjectName("grade_label")

        date = QDate.currentDate()
        date_label = QLabel("{:02d} {}\n{} {}".format(date.day(), date.longDayName(date.dayOfWeek()),
                                                      date.longMonthName(date.month()), date.year()))
        date_label.setObjectName("date_label")

        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(name_label)
        layout.addWidget(grade_label)
        layout.addWidget(date_label)


    def createInfoBar(self, layout : QGridLayout):

        # create the title labels
        present_label = QLabel("Present Students")
        absent_label = QLabel("Absent Students")
        percent_label = QLabel("Present Percent")

        for label in [present_label, absent_label, percent_label]:
            label.setObjectName("field_label")

        # create the present students label
        self.present_std_label = QLabel("0")
        self.absent_std_label = QLabel(f"{len(self.student_names)}")

        self.percent_label = QLabel("0.00%")

        for label in [self.present_std_label, self.absent_std_label, self.percent_label]:
            label.setObjectName("value_label")

        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(present_label, 0, 0)
        layout.addWidget(absent_label, 0, 1)
        layout.addWidget(percent_label, 0, 2)
        layout.addWidget(self.present_std_label, 1, 0)
        layout.addWidget(self.absent_std_label, 1, 1)
        layout.addWidget(self.percent_label, 1, 2)

    def updateValue(self, state : int):

        present = int(self.present_std_label.text())
        absent = int(self.absent_std_label.text())

        # update the value of the labels
        if state == Qt.Checked:
            self.present_std_label.setText(f"{present + 1}")
            self.absent_std_label.setText(f"{absent - 1}")

            self.percent_label.setText("{:02.2f}%".format((present + 1) / len(self.student_names) * 100))

        else:
            self.present_std_label.setText(f"{present - 1}")
            self.absent_std_label.setText(f"{absent + 1}")

            self.percent_label.setText("{:02.2f}%".format((present - 1) / len(self.student_names) * 100))

    def saveRegister(self):

        data = []
        # get the state data of the students
        for i in range(int(self.studentListWidget.count())):
            item : QCheckBox  = self.studentListWidget.itemWidget(self.studentListWidget.item(i))
            data.append((self.student_names[i][0], item.isChecked()))

        # create the new class util object for save the register data
        class_worker = ClassInitializer()
        class_worker.completedDay(self.cls_id, self.year, data)

        # show the complete message and delete the current register
        QMessageBox.information(self, "Register Save Info", f"Register of {QDate.currentDate().toString('yyyy MMM dd')} is successful saved.",
                                QMessageBox.StandardButton.Ok)
        self.saveStatus = True
        self.studentListWidget.hide()

    def closeRegister(self):

        # close the register
        if self.saveStatus:
            result = QMessageBox.question(self, "Close Register", "Are you sure tp close the register.",
                                QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No)
            if result == QMessageBox.StandardButton.Yes:
                self.deleteLater()

        else:
            result = QMessageBox.warning(self, "Close Register", "Are you sure to close register.\ndata will be lost!!!",
                                         QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No)
            if result == QMessageBox.StandardButton.Yes:
                self.deleteLater()