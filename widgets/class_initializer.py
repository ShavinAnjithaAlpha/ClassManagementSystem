import os, threading

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QWidget, QPushButton, QCheckBox, QLabel, QButtonGroup, QLineEdit, QComboBox, QHBoxLayout,
                             QDateEdit, QVBoxLayout, QListWidget, QListWidgetItem, QMessageBox)
from PyQt5.QtCore import Qt, QSize, QDate

from file_manager.class_manager import ClassManager
from file_manager.student_manager import StudentManager
from file_manager.class_utils import ClassInitializer

from style_sheets.new_class_style_sheet import style_sheet

from util.datetimeutil import DateTimeUtil

class StudentChecker(QWidget):
    def __init__(self, grade : int , chooses_ids : list):
        super(StudentChecker, self).__init__()
        self.data = self.generateData(grade, chooses_ids)
        self.getStatus = False

        # create the search bar for widget
        self.searchBar = QLineEdit()
        self.searchBar.resize(300, 30)
        self.searchBar.setPlaceholderText("search students")
        self.searchBar.returnPressed.connect(self.search)

        search_box = QHBoxLayout()
        search_box.addStretch()
        search_box.addWidget(QLabel("Search"))
        search_box.addWidget(self.searchBar)

        self.listBox = QHBoxLayout()

        # create the list for store the list widgets
        self.student_lists = []

        self.generateLists(self.listBox)

        vbox = QVBoxLayout()
        vbox.addLayout(search_box)
        vbox.addLayout(self.listBox)

        self.setLayout(vbox)

        self.setStyleSheet("""
        
                    QLabel {font-size : 14px;}""")

    def generateLists(self, layout : QHBoxLayout):

        thread = threading.Thread(target=self.generateLists_, args=(layout, ), daemon=True)
        thread.run()

    def generateLists_(self, layout : QHBoxLayout):

        self.title_label = []
        # split bu the sex
        sexes = {"male" : [],
                 "female" : [],
                "other" : []}

        for row in self.data:
            if row["sex"] == 0:
                sexes["male"].append(row)
            elif row["sex"] == 1:
                sexes["female"].append(row)
            else:
                sexes["other"].append(row)

        for title in sexes.keys():
            if sexes[title]:
                # create the list widget
                list_widget = QListWidget()
                for row in sexes[title]:
                    item = QListWidgetItem("{} {}".format(row["firstName"], row["lastName"]))
                    item.setCheckState(False)
                    item.setData(Qt.UserRole, row["ID"])
                    item.setData(Qt.FontRole, QFont("Helvetica", 11))
                    list_widget.addItem(item)

                self.student_lists.append(list_widget)

                title_label = QLabel(title)
                self.title_label.append(title_label)

                # add to the layout
                vbox = QVBoxLayout()
                vbox.addWidget(title_label)
                vbox.addWidget(list_widget)

                layout.addLayout(vbox)


    def generateData(self, grade , chooses_ids):

        data = []
        # create the student manager
        std_manager = StudentManager()
        cls_ids = std_manager.getFromKey("ID")

        for id in cls_ids:
            id = int(id)
            # get the f name ,l name, and sex
            if DateTimeUtil.gradeFromText(std_manager.get(id , "birthDay")) == grade:
                fName, lName , sex = std_manager.get(id , "firstName"), std_manager.get(id, "lastName"), \
                                    int(std_manager.get(id, "sex"))

                data.append({
                    "ID" : id,
                    "firstName" : fName,
                    "lastName" : lName,
                    "sex" : sex
                })

        return data

    def search(self):

        text = self.searchBar.text()
        if text == "":
            for widget in self.student_lists:
                for i in range(widget.count()):
                    widget.item(i).setHidden(False)
            return None

        for widget in self.student_lists:
            for index in range(widget.count()):
                item  : QListWidgetItem = widget.item(index)

                if text.lower() in item.text().lower():
                    item.setHidden(False)
                else:
                    item.setHidden(True)

    def getChooseIDs(self) -> list[int]:

        chooses_ids = []

        for list_widget in self.student_lists:
            for index in range(list_widget.count()):
                item : QListWidgetItem = list_widget.item(index)
                # get the student id and check state
                student_id  : int = int(item.data(Qt.UserRole))

                if item.data(Qt.CheckStateRole):
                     chooses_ids.append(student_id)

        self.getStatus = True
        return chooses_ids



    def update(self, grade , chooses_ids : list):

        [widget.deleteLater() for widget in self.student_lists]
        self.student_lists.clear()

        [label.deleteLater() for label in self.title_label]
        self.title_label.clear()

        self.data = self.generateData(grade, chooses_ids)
        self.generateLists(self.listBox)

class ClassInitializerWidget(QWidget):
    def __init__(self):
        super(ClassInitializerWidget, self).__init__()
        self.choose_ids = []

        # build the UI
        top_lyt = QHBoxLayout()
        self.setUpTop(top_lyt)

        # get the grades
        # create the student manager object
        std_manager = StudentManager()
        bDays = std_manager.getFromKey("birthDay")

        # produce the grades list
        grades = set()
        [grades.add(DateTimeUtil.gradeFromText(date)) for date in bDays]
        del bDays

        self.StudentChooserBox = StudentChecker(min(grades), self.choose_ids)

        # create the button bar for this
        button_lyt = QHBoxLayout()
        self.buildButtonBar(button_lyt, grades)


        bottom_lyt = QHBoxLayout()
        self.setUpBottom(bottom_lyt)

        # create the main layout
        vbox = QVBoxLayout()
        vbox.addLayout(top_lyt)
        vbox.addLayout(button_lyt)
        vbox.addWidget(self.StudentChooserBox)
        vbox.addLayout(bottom_lyt)

        self.setLayout(vbox)

        self.setStyleSheet(style_sheet)


    def setUpTop(self, layout : QHBoxLayout):

        # first create the class manager
        cls_manager = ClassManager()
        # get the class manger classes
        cls_ids = cls_manager.getFromKey("id")
        # create the combo box for pack the classes
        self.classes_combo_box = QComboBox()
        for i in cls_ids:
            self.classes_combo_box.addItem("{} - grade {}".format(cls_manager.get(int(i), "className"),
                                                             cls_manager.get(int(i), "grade")), userData=int(i))

        layout.addWidget(QLabel("Choose Class You want to initiate the class"))
        layout.addWidget(self.classes_combo_box)
        layout.addWidget(QLabel("for year {}".format(QDate().currentDate().year())))
        layout.addStretch()


    def buildButtonBar(self, layout : QHBoxLayout, grades : list):

        layout.setSpacing(0)

        self.button_bar = []
        for grade in grades:
            button = QPushButton(f"Grade {grade}")
            button.setObjectName("bar_button")
            button.pressed.connect(lambda e = grade, b = button : self.switchGrade(e, b))
            self.button_bar.append(button)
            # add to the layout
            layout.addWidget(button)

        layout.addStretch()
        # select the button
        self.button_bar[0].setDisabled(True)

    def setUpBottom(self, layout : QHBoxLayout):

        # create the date chooser for choose the starting day
        self.start_day_edit = QDateEdit()
        self.start_day_edit.setCalendarPopup(True)

        # create the add student button
        add_student_button = QPushButton("Add Students")
        add_student_button.pressed.connect(self.addStudent)

        complete_button = QPushButton("Complete")
        complete_button.pressed.connect(self.createNewClass)

        layout.addWidget(QLabel("Choose Starting Day for Class"))
        layout.addWidget(self.start_day_edit)
        layout.addStretch()
        layout.addWidget(add_student_button)
        layout.addWidget(complete_button)

    def switchGrade(self, grade : int, button : QPushButton):

        if not self.StudentChooserBox.getStatus:
            # show the add student message for user
            message = QMessageBox.question(self, "Student Adding", "Add the student to system.\nif you ignore this check states are clearing.",
                                           QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No)

            if message == QMessageBox.StandardButton.Yes:
                # call to the add student function
                self.addStudent()
            else:
                QMessageBox.information(self, "Data Clearing", "Your Student Checked data is lost.", QMessageBox.StandardButton.Ok)

        self.StudentChooserBox.update(grade, self.choose_ids)

        button.setDisabled(True)
        for b in self.button_bar:
            if b != button:
                b.setEnabled(True)

    def addStudent(self):

        # get the chooses id from student chooser
        chooses_id = self.StudentChooserBox.getChooseIDs()
        # append to the main id list
        [self.choose_ids.append(index) for index in chooses_id]

        # display the message box for task complete
        QMessageBox.information(self, "Student Added", "Student Added Successful.", QMessageBox.StandardButton.Ok)


    def createNewClass(self):

        if os.path.exists(f"db/classes/{QDate.currentDate().year()}@{self.classes_combo_box.currentData()}@class.json"):
            QMessageBox.information(self, "New Class Start","Class already created.You cannot overwrite the class.", QMessageBox.StandardButton.Ok)
            return

        # create the class initializer
        cls_initializer = ClassInitializer()
        cls_initializer.initializeClass(int(self.classes_combo_box.currentData()), QDate.currentDate().year(), self.choose_ids)

        QMessageBox.information(self, "Start New Class", "New Class Start Successful.", QMessageBox.StandardButton.Ok)
