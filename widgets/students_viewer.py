from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLineEdit, QRadioButton, QGroupBox,
                             QHBoxLayout, QVBoxLayout, QTableView, QHeaderView, QButtonGroup, QLabel, QComboBox,
                             QDateEdit, QCheckBox, QStackedLayout)
from PyQt5.QtCore import Qt, QSize, QAbstractTableModel, QModelIndex, QDate
from PyQt5.QtGui import QFont, QColor
from file_manager.student_manager import StudentManager

from dialogs.student_dialog import StudentDialog
from widgets.filter_list import FiltersStudentList

from style_sheets.student_viewer_style_sheet import style_sheet

from util import datetimeutil

db_file = "../db/main.db"

class StudentTableModel(QAbstractTableModel):
    def __init__(self):
        super(StudentTableModel, self).__init__()
        self.data_ = []
        # declare the row titles list
        self.fields = ["ID", "First Name", "Last Name", "Address", "Sex", "Telephone Number", "Parent Telephone Number",
                       "Birth Day", "School", "Entered Day"]
        # setup the students tabular  data
        self.fillData()

    def fillData(self):

        # create the student manager object
        student_manager = StudentManager()
        # load the data
        indexes = student_manager.getFromKey("id")
        for index in indexes:
            row = student_manager.getFromIndex(index)
            # fill the row
            self.data_.append(
                (index,
                row[1],
                row[2],
                row[3],
                row[-1],
                row[4],
                row[5],
                row[6],
                row[7],
                row[8])
            )


    def data(self, index: QModelIndex, role: int = ...):

        row, column = index.row(), index.column()
        if role == Qt.DisplayRole:
            if column == 4:
                if self.data_[row][column] == 0:
                    return "Male"
                elif self.data_[row][column] == 1:
                    return "FeMale"
                else:
                    return "Other"

            return self.data_[row][column]

        elif role == Qt.BackgroundRole:

            if column == 4:
                if self.data_[row][column] == 0:
                    return QColor(0, 100, 250)
                elif self.data_[row][column] == 1:
                    return QColor(250, 100, 0)
                else:
                    return QColor(0, 250, 0)

        elif role == Qt.ForegroundRole:
            if column == 4:
                return QColor(255, 255, 255)

    def rowCount(self, parent: QModelIndex = ...) -> int:

        return len(self.data_)

    def columnCount(self, parent: QModelIndex = ...) -> int:

        return len(self.fields)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...):

        if orientation == Qt.Horizontal and role in (Qt.DisplayRole, Qt.EditRole):
            try:
                return self.fields[section]
            except:
                pass
        return super().headerData(section, orientation, role)

class StudentViewer(QWidget):
    def __init__(self):
        super(StudentViewer, self).__init__()
        self.initializeUI()

    def initializeUI(self):

        # create the main parts
        # create the main widgets
        # create the stack widgets
        self.stack_pane = QStackedLayout()

        self.table = QTableView()
        self.setUpTable()
        self.stack_pane.addWidget(self.table)

        # create the vbox for searching widgets
        self.searchBox = QHBoxLayout()
        self.setUpSearchWidgets()

        # create the another h box for pack the other components
        self.ohterBox = QHBoxLayout()
        self.setUpTop()

        # create the vox for all of this
        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.addLayout(self.ohterBox)
        vbox.addLayout(self.searchBox)
        vbox.addLayout(self.stack_pane)
        self.setLayout(vbox)

        self.setStyleSheet(style_sheet)

    def setUpTable(self):

        # create the student table model
        self.student_model = StudentTableModel()
        # set the model
        self.table.setModel(self.student_model)

        # another configurations
        # self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

    def setUpSearchWidgets(self):

        # create the search option dict
        self.search_options = {1 : "ID",
                                2 : "First Name",
                               3 : "Last Name",
                               4 : "Address",
                               5 : "School",
                               6 : "telephone Number",
                               7 : "birth day"}
        self.button_group = QButtonGroup()
        groupBox = QGroupBox("Search Options")

        # create the hbox for this
        radio_box = QHBoxLayout()
        groupBox.setLayout(radio_box)

        # create the radio buttons
        for i, text in enumerate(self.search_options.values()):
            radio = QRadioButton(text)
            # add to the button group
            self.button_group.addButton(radio, i + 1)
            # add to the hbox
            radio_box.addWidget(radio)
        self.button_group.button(2).setChecked(True)
        self.button_group.idToggled.connect(self.setUpSearchStyle)

        # create the search Edit
        self.searchBar = QLineEdit()
        self.searchBar.resize(250, 40)
        self.searchBar.returnPressed.connect(self.searchNames)

        # create the school combo box
        self.searchSchoolBox = QComboBox()
        self.searchSchoolBox.addItems(set(StudentManager().getFromKey("school")))
        self.searchSchoolBox.setVisible(False)
        self.searchSchoolBox.textActivated.connect(self.searchSchool)

        # create the birth day checker
        self.birthdaySearchBox = QDateEdit()
        self.birthdaySearchBox.setVisible(False)
        self.birthdaySearchBox.setCalendarPopup(True)
        self.birthdaySearchBox.dateChanged.connect(self.searchBirthDay)

        showAllButton = QPushButton("Show All")
        showAllButton.pressed.connect(self.showAll)

        self.searchBox.addWidget(groupBox)
        self.searchBox.addSpacing(20)
        self.searchBox.addWidget(showAllButton)
        self.searchBox.addWidget(QLabel("Search"))
        self.searchBox.addWidget(self.searchBar)
        self.searchBox.addWidget(self.searchSchoolBox)
        self.searchBox.addWidget(self.birthdaySearchBox)

    def setUpSearchStyle(self, index : int , check : bool):

        if index == 5:
            self.searchBar.setVisible(False)
            self.searchSchoolBox.setVisible(True)
            self.birthdaySearchBox.setVisible(False)
        elif index == 1 or index == 2 or index == 3 or index == 4:
            self.searchSchoolBox.setVisible(False)
            self.searchBar.setVisible(True)
            self.birthdaySearchBox.setVisible(False)
        elif index == 7:
            self.searchSchoolBox.setVisible(False)
            self.searchBar.setVisible(False)
            self.birthdaySearchBox.setVisible(True)

    def setUpTop(self):

        # create the filter option box
        filter_option_group = QGroupBox("Filter options")
        hbox = QHBoxLayout()
        filter_option_group.setLayout(hbox)
        self.filter_checks = []

        # create the radio buttons for this
        options = ["Sex", "School", "Grade"]
        for i in range(len(options)):
            check = QCheckBox(options[i])
            check.stateChanged.connect(lambda s , e = i : self.setUpChooser(e, s))
            # add to the button group
            hbox.addWidget(check)
            self.filter_checks.append(check)


        std_manager = StudentManager()

        # create the filter choosers
        self.sex_chooser = QComboBox()
        self.sex_chooser.setVisible(False)
        self.sex_chooser.addItems(["Male", "Female", "Other"])

        self.school_chooser = QComboBox()
        self.school_chooser.addItems(set(std_manager.getFromKey("school")))
        self.school_chooser.setVisible(False)

        # filter the birth days
        bdays = std_manager.getFromKey("birthDay")
        dates = []
        for day in bdays:
            y, m ,d = day.split("-")
            dates.append(QDate(int(y), int(m), int(d)))

        max_date = max(dates)
        min_date = min(dates)
        del dates
        del bdays

        min_grade = datetimeutil.DateTimeUtil.grade(max_date)
        max_grade = datetimeutil.DateTimeUtil.grade(min_date)

        self.grade_chooser = QComboBox()
        self.grade_chooser.addItems([str(i) for i in range(min_grade, max_grade + 1)])
        self.grade_chooser.setVisible(False)

        filter_chooser_box = QHBoxLayout()
        filter_chooser_box.addWidget(self.sex_chooser)
        filter_chooser_box.addWidget(self.school_chooser)
        filter_chooser_box.addWidget(self.grade_chooser)


        # create the filter button
        self.filterButton = QPushButton("filter")
        self.filterButton.pressed.connect(self.filter)
        self.filterButton.setDisabled(True)

        # create the student add button
        student_add_button = QPushButton("+ Add Student")
        student_add_button.setFont(QFont('verdana', 15))
        student_add_button.pressed.connect(self.addStudent)

        self.tableShowButton = QPushButton("show table")
        self.tableShowButton.setDisabled(True)
        self.tableShowButton.pressed.connect(self.showTable)

        self.ohterBox.addWidget(filter_option_group)
        self.ohterBox.addLayout(filter_chooser_box)
        self.ohterBox.addWidget(self.filterButton)
        self.ohterBox.addStretch()
        self.ohterBox.addWidget(self.tableShowButton)
        self.ohterBox.addWidget(student_add_button)

    def showTable(self):

        self.stack_pane.setCurrentIndex(0)

        # delete the other widgets
        self.stack_pane.removeWidget(self.stack_pane.widget(1))

    def setUpChooser(self, index : int , state : bool):

        if index == 0:
            if state:
                self.sex_chooser.show()
            else:
                self.sex_chooser.hide()

        elif index == 1:
            if state:
                self.school_chooser.show()
            else:
                self.school_chooser.hide()

        else:
            if state:
                self.grade_chooser.show()
            else:
                self.grade_chooser.hide()

        for check in self.filter_checks:
            if check.isChecked():
                self.filterButton.setEnabled(True)
                return
        self.filterButton.setDisabled(True)


    def searchNames(self):

        # first check the search options
        option = self.button_group.checkedId()
        search_index = self.searchBar.text()

        if option == 1 or option == 2 or option == 3:
            # search by ID
            for i in range(len(self.student_model.data_)):
                if not search_index.lower() in str(self.student_model.data_[i][option - 1]).lower():
                    self.table.hideRow(i)
                else:
                    self.table.showRow(i)

    def searchSchool(self, text):

        for i in range(len(self.student_model.data_)):
            if str(self.student_model.data_[i][8]) == text:
                self.table.showRow(i)
            else:
                self.table.hideRow(i)


    def searchBirthDay(self, date : QDate):

        for i in range(len(self.student_model.data_)):
            # get the date
            date_text  = self.student_model.data_[i][7]
            y, m, d = date_text.split("-")
            birthday = QDate(int(y), int(m) ,int(d))

            if birthday == date:
                self.table.showRow(i)
            else:
                self.table.hideRow(i)

    def showAll(self):

        for i in range(len(self.student_model.data_)):
            if self.table.isRowHidden(i):
                self.table.showRow(i)

        self.searchBar.clear()
        self.searchSchoolBox.setCurrentIndex(0)

    def addStudent(self):

        self.dialog = StudentDialog()

    def filter(self):

        # filter the data
        data = self.student_model.data_

        filter1 = []
        if self.filter_checks[0].isChecked():

            for row in data:
                if row[4] == self.sex_chooser.currentIndex():
                    filter1.append(row)
            data = filter1


        filter2 = []
        if self.filter_checks[1].isChecked():
            for row in data:
                if row[8] == self.school_chooser.currentText():
                    filter2.append(row)
            data = filter2
        elif not self.filter_checks[2].isChecked():
            self.addFilterList(filter1)
            return

        filter3 = []
        if self.filter_checks[2].isChecked():
            for row in data:
                if int(self.grade_chooser.currentText()) == datetimeutil.DateTimeUtil.gradeFromText(row[7]):
                    filter3.append(row)
            data = filter3
        else:
            self.addFilterList(filter2)
            return

        self.addFilterList(data)

    def addFilterList(self, filtered_list : list):

        if self.stack_pane.count() > 1:
            self.stack_pane.removeWidget(self.stack_pane.widget(1))
        # create the another filter widgets
        filter_list = FiltersStudentList(filtered_list)

        # add to the stack layout
        self.stack_pane.addWidget(filter_list)
        self.stack_pane.setCurrentIndex(1)

        self.tableShowButton.setEnabled(True)