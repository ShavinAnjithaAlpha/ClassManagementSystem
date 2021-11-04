from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QDialog, QWidget, QHBoxLayout, QFormLayout, QGroupBox, QVBoxLayout, QPushButton,
                             QLabel, QDateEdit, QRadioButton, QLineEdit, QComboBox, QButtonGroup, QMessageBox,
                             QApplication)
from PyQt5.QtCore import Qt, QSize

from file_manager.student_manager import StudentManager

class StudentDialog(QDialog):
    def __init__(self):
        super(StudentDialog, self).__init__()
        self.setModal(True)
        self.setWindowTitle("New Student Dialog")
        self.resize(500, 500)

        self.initializeUI()
        self.show()

    def initializeUI(self):

        # setup the dialog
        basic_info_group = QGroupBox("Basic Info")
        self.setUpBasicGroup(basic_info_group)

        contact_group = QGroupBox("Contact")
        self.setUpContactGroup(contact_group)

        # create the id label
        self.id_label = QLabel()
        self.id_label.setStyleSheet("""
                                    QLabel {font-size : 25px;
                                            font-family  :verdana;
                                            padding : 10px;}""")

        # create the buttons for dialog
        cancel_button = QPushButton("Cancel")
        self.save_button  = QPushButton("Save")
        self.submit_button = QPushButton("Submit")

        self.save_button.setVisible(False)

        cancel_button.pressed.connect(self.reject)
        self.save_button.pressed.connect(self.accept)
        self.submit_button.pressed.connect(self.showID)

        hbox  = QHBoxLayout()
        hbox.addWidget(self.save_button)
        hbox.addWidget(self.submit_button)
        hbox.addWidget(cancel_button)

        vbox = QVBoxLayout()
        vbox.addWidget(basic_info_group)
        vbox.addWidget(contact_group)
        vbox.addWidget(self.id_label)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def setUpBasicGroup(self, group : QGroupBox):

        # create the fileds
        self.first_name_entry = QLineEdit()
        self.first_name_entry.returnPressed.connect(lambda : self.last_name_entry.setFocus())

        self.last_name_entry = QLineEdit()
        self.last_name_entry.returnPressed.connect(lambda : self.address_entry.setFocus())

        self.address_entry = QLineEdit()
        self.address_entry.returnPressed.connect(lambda : self.school_entry.setFocus())

        self.school_entry = QComboBox()
        self.school_entry.addItems(set(StudentManager().getFromKey("school")))
        self.school_entry.setEditable(True)
        self.school_entry.keyPressEvent = lambda e : self.birthday_edit.setFocus()

        # birth day edit
        self.birthday_edit = QDateEdit()
        self.birthday_edit.setCalendarPopup(True)

        # create the radio buttons for choose sex
        male_radio = QRadioButton("Male")
        male_radio.setChecked(True)

        female_radio = QRadioButton("FeMale")
        other_radio = QRadioButton("Other")

        # create the button group for set exclsuive to radios
        self.radio_group = QButtonGroup()
        self.radio_group.addButton(male_radio, 0)
        self.radio_group.addButton(female_radio, 1)
        self.radio_group.addButton(other_radio, 2)

        hbox  = QHBoxLayout()
        hbox.addWidget(male_radio)
        hbox.addWidget(female_radio)
        hbox.addWidget(other_radio)

        # create the form for packed them
        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignRight)
        form.setFormAlignment(Qt.AlignCenter)

        form.addRow("First Name", self.first_name_entry)
        form.addRow("Last Name", self.last_name_entry)
        form.addRow("Address", self.address_entry)
        form.addRow("School", self.school_entry)
        form.addRow("Birth Day", self.birthday_edit)
        form.addRow("Sex", hbox)

        group.setLayout(form)


    def setUpContactGroup(self, group : QGroupBox):

        # create the telephone numbers edits
        self.tel_number_edit = QLineEdit()
        self.tel_number_edit.setInputMask("xxx-xx xx xxx")
        self.tel_number_edit.returnPressed.connect(lambda  : self.parent_tel_edit.setFocus())

        self.parent_tel_edit = QLineEdit()
        self.parent_tel_edit.setInputMask("xxx-xx xx xxx")

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignRight)

        form.addRow("TelePhone Number", self.tel_number_edit)
        form.addRow("Parent Telephone Number", self.parent_tel_edit)

        group.setLayout(form)

    def accept(self) -> None:

        # create the student mnanager
        std_manager = StudentManager()
        std_manager.addStudent(self.data)

        QMessageBox.information(self, "New Student Added", "Student Added Successful", QMessageBox.StandardButton.Ok)

        super().accept()

    def showID(self):

        # check the all of the requred data is filled
        if self.first_name_entry.text() == "":
            self.first_name_entry.setFocus()
            return
        if self.last_name_entry.text() == "":
            self.last_name_entry.setFocus()
            return
        if self.address_entry.text() == "":
            self.address_entry.setFocus()
            return
        if self.school_entry.text() == "":
            self.school_entry.setFocus()
            return
        if self.parent_tel_edit.text() == "":
            self.parent_tel_edit.setFocus()
            return

        sex = "male" if self.radio_group.checkedId() == 0 else "female"
        # build the data
        self.data = {"firstName" : self.first_name_entry.text(),
                "lastName" : self.last_name_entry.text(),
                "address" : self.address_entry.text(),
                "school" : self.school_entry.text(),
                "parTelNumber" : self.parent_tel_edit.text(),
                "birthDay" : self.birthday_edit.date().toString("yyyy-MM-dd"),
                "sex" : sex,
                "telNumber" : self.tel_number_edit.text(),

            }

        # create the class manager
        class_manager  = StudentManager()
        if class_manager.getFromKey("id") == []:
            index = 1
        else:
            index = class_manager.getFromKey("id")[-1] + 1

        # show the id
        self.id_label.setText(f"Your ID : <font color = 'blue' >{index} </font>")

        self.submit_button.setVisible(False)
        self.save_button.setVisible(True)


if __name__ == "__main__":
    app = QApplication([])
    window = StudentDialog()
    app.exec_()