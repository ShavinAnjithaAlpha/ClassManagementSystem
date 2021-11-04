from PyQt5.QtGui import QFont, QColor, QPainter
from PyQt5.QtWidgets import (QWidget, QListView, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QFormLayout, QLineEdit,
                                QStyledItemDelegate, QStyleOptionViewItem)
from PyQt5.QtCore import Qt, QSize, QAbstractListModel, QModelIndex

class listBox(QStyledItemDelegate):
    def __init__(self, data : list):
        super(listBox, self).__init__()
        self.data = data

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex) -> None:

        painter.save()
        # drwa the rect
        text = self.data[index.row()]
        painter.drawRect(option.rect)

        painter.drawText(option.rect , 12, text)

        painter.restore()
        painter.end()


class FilteredStudentModel(QAbstractListModel):
    def __init__(self, data : list):
        super(FilteredStudentModel, self).__init__()
        if data:
            self.data_ = data
        else:
            self.data_ = []

    def data(self, index: QModelIndex, role: int = ...):

        row = index.row()
        if role == Qt.DisplayRole:
            name = "{} {}".format(self.data_[row][1] , self.data_[row][2])

            return name

        elif role == Qt.FontRole:
            return QFont("Helvetica", 12)

    def rowCount(self, parent: QModelIndex = ...) -> int:

        return len(self.data_)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return 1

class StudentForm(QWidget):
    def __init__(self, row : list , parent = None):
        super(StudentForm, self).__init__(parent)
        self.setFixedSize(int(parent.width() / 3), parent.height())

        # create the form for this
        student_form = QFormLayout()
        student_form.setLabelAlignment(Qt.AlignRight)
        student_form.setFormAlignment(Qt.AlignCenter)
        student_form.setVerticalSpacing(20)
        student_form.setHorizontalSpacing(30)


        title = QLabel("{} {}".format(row[1], row[2]))
        title.setObjectName("title_label")
        title.setWordWrap(True)
        title.setAlignment(Qt.AlignRight)

        sex = "Male"
        if row[4] == 1:
            sex = "FeMale"
        elif row[4] == 2:
            sex == "Other"


        # create the address abel
        add_label = QLabel(row[3])
        add_label.setWordWrap(True)

        school_label = QLabel(row[6])
        tel_label = QLabel(row[7])
        tel2_label = QLabel(row[8])
        sex_label = QLabel(sex)

        for label in [add_label, school_label, tel_label, tel2_label, sex_label]:
            label.setObjectName("formLabel")


        # add the data to the form
        student_form.addWidget(title)
        student_form.setAlignment(title, Qt.AlignHCenter)
        student_form.addRow("Address :", add_label)
        student_form.addRow("School :", school_label)
        student_form.addWidget(QLabel(""))
        student_form.addRow("Telephone Number :", tel_label)
        student_form.addRow("Parent Telephone Number :", tel2_label)

        self.setLayout(student_form)

        self.setStyleSheet("""
                    QLabel {font-size : 25px;}
                    
                    QLabel#title_label {font-family : Helvetica;
                                        font-size : 40px;}
        
        """)

class FiltersStudentList(QWidget):
    def __init__(self, model : list, titles : dict = {}):
        super(FiltersStudentList, self).__init__()
        self.model = FilteredStudentModel(model)
        self.titles = titles

        self.student_form : QWidget = None

        # create the main list view
        self.listView = QListView()
        self.listView.setModel(self.model)

        self.listView.clicked.connect(self.showStudent)

        # create the search bar
        self.searchBar = QLineEdit()
        self.searchBar.returnPressed.connect(self.search)
        self.searchBar.resize(200, 35)

        hbox1 = QHBoxLayout()
        hbox1.addWidget(QLabel("Search"))
        hbox1.addWidget(self.searchBar)

        # create the vbox for this
        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addWidget(self.listView)

        # create the layout for insert the student forms
        self.main_hbox = QHBoxLayout()
        self.main_hbox.addLayout(vbox)


        self.setLayout(self.main_hbox)

    def search(self):

        text = self.searchBar.text()
        for i in range(len(self.model.data_)):
            if text.lower() in "{} {}".format(self.model.data_[i][1], self.model.data_[i][2]).lower():
                self.listView.setRowHidden(i, False)
            else:
                self.listView.setRowHidden(i, True)

    def showStudent(self, index : QModelIndex):

        # get the data
        row = self.model.data_[index.row()]
        # add the widget for this
        if self.student_form:
            self.student_form.deleteLater()

        # add to the layout
        self.student_form = StudentForm(row, self)
        self.main_hbox.insertWidget(1, self.student_form)