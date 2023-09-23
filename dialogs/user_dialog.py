import json

from PyQt5.QtWidgets import (QApplication, QDialog, QGroupBox, QFormLayout, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel,
                             QMessageBox)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont

class UserDialog(QDialog):
    def __init__(self, parent = None):
        super(UserDialog, self).__init__(parent)
        self.setModal(True)
        self.resize(500, 400)
        self.setWindowTitle("User Profile Dialog")

        self.initializeUI()
        self.show()

    def initializeUI(self):

        self.required_fileds = []

        # create the three group for this
        basic_group = QGroupBox("Basic Info")
        self.setUpBasicBox(basic_group)

        # create the insititute group
        institute_group = QGroupBox("Institute Info")
        self.setUpInstituteBox(institute_group)

        # create the personal contact group
        personal_contact_group = QGroupBox("Personal Contacts")
        self.setUpContactBox(personal_contact_group)

        # create the security box
        security_box  = QGroupBox("Security")
        self.setUpSecurityBox(security_box)

        # create the buttons
        save_button = QPushButton("Save")
        cancel_button = QPushButton("Cancel")

        save_button.pressed.connect(self.accept)
        cancel_button.pressed.connect(self.reject)

        hbox = QHBoxLayout()
        hbox.addWidget(save_button)
        hbox.addWidget(cancel_button)

        vbox = QVBoxLayout()
        vbox.addWidget(basic_group)
        vbox.addWidget(institute_group)
        vbox.addWidget(personal_contact_group)
        vbox.addWidget(security_box)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def setUpBasicBox(self, group : QGroupBox):

        # create the feleds
        self.first_name_entry = QLineEdit()

        self.last_name_entry = QLineEdit()

        self.qualify_entry = QLineEdit()

        self.user_name_entry = QLineEdit()

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignRight)

        form.addRow("First Name", self.first_name_entry)
        form.addRow("Last Name", self.last_name_entry)
        form.addRow("Qualifiers", self.qualify_entry)
        form.addRow("User Name", self.user_name_entry)
        form.addWidget(QLabel("*user name must be a one word without white spaces"))

        group.setLayout(form)

        [self.required_fileds.append(i) for i in (self.first_name_entry, self.last_name_entry,
                                                  self.qualify_entry, self.user_name_entry)]

    def setUpInstituteBox(self, group : QGroupBox):

        self.ins_name_entry  = QLineEdit()
        self.ins_address_entry = QLineEdit()
        self.ins_number_entry  = QLineEdit()

        self.ins_number_entry.setInputMask("xxx-xx xx xxx")

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignRight)
        form.addRow("Institute Name", self.ins_name_entry)
        form.addRow("Address", self.ins_address_entry)
        form.addRow("Institute Contact Number(LAN)", self.ins_number_entry)

        group.setLayout(form)

        [self.required_fileds.append(i) for i in (self.ins_number_entry, self.ins_address_entry)]

    def setUpContactBox(self, group : QGroupBox):

        self.per_number = QLineEdit()
        self.per_number.setInputMask("xxx-xx xx xxx")

        self.email_entry = QLineEdit()
        self.whatsapp_entry = QLineEdit()
        self.whatsapp_entry.setInputMask("xxx-xx xx xxx")

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignRight)
        form.addRow("Personal Contact Number", self.per_number)
        form.addRow("Whatsapp Number" ,self.whatsapp_entry)
        form.addRow("Class Email Address", self.email_entry)

        group.setLayout(form)

        [self.required_fileds.append(i) for i in (self.per_number, )]

    def setUpSecurityBox(self, group : QGroupBox):

        def enableConfirm(text):
            if not self.enter_pw_confirm.isEnabled():
                self.enter_pw_confirm.setEnabled(True)

        def enablePin(text):
            if not self.exit_pin_cofirm.isEnabled():
                self.exit_pin_cofirm.setEnabled(True)

        self.enter_pw = QLineEdit()
        self.enter_pw.setEchoMode(QLineEdit.EchoMode.Password)
        self.enter_pw.textChanged.connect(enableConfirm)

        self.enter_pw_confirm = QLineEdit()
        self.enter_pw_confirm.setEchoMode(QLineEdit.EchoMode.Password)
        self.enter_pw_confirm.setEnabled(False)

        self.exit_pin = QLineEdit()
        self.exit_pin.setEchoMode(QLineEdit.EchoMode.Password)
        self.exit_pin.setInputMask("xxxx")
        self.exit_pin.textChanged.connect(enablePin)

        self.exit_pin_cofirm = QLineEdit()
        self.exit_pin_cofirm.setEnabled(False)
        self.exit_pin_cofirm.setEchoMode(QLineEdit.EchoMode.Password)
        self.exit_pin_cofirm.setInputMask("xxxx")

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignRight)
        form.addWidget(QLabel("*Password must be least 8 charactor with numbers and alphabetics"))
        form.addRow("Logging Password", self.enter_pw)
        form.addRow("Confirm Password", self.enter_pw_confirm)
        form.addWidget(QLabel(""))
        form.addWidget(QLabel("pin must be a 4 numbers"))
        form.addRow("Exit pin", self.exit_pin)
        form.addRow("Confirm pin", self.exit_pin_cofirm)

        group.setLayout(form)

        [self.required_fileds.append(i) for i in (self.enter_pw, self.exit_pin)]

    def accept(self) -> None:

        for edit in self.required_fileds:
            if edit.text() == "" or edit.text() == "   -         ":
                edit.setFocus()
                return

        if self.user_name_entry.text().isspace():
            self.user_name_entry.setFocus()
            return

        if self.enter_pw.text() != self.enter_pw_confirm.text():
            self.enter_pw_confirm.setText("")
            self.enter_pw.setEchoMode(QLineEdit.EchoMode.Password)
            self.enter_pw_confirm.setFocus()
            return

        if self.exit_pin.text() != self.exit_pin_cofirm.text():
            self.exit_pin_cofirm.setText("")
            self.exit_pin.setEchoMode(QLineEdit.Password)
            self.exit_pin_cofirm.setFocus()

        # collect the data to dictionary
        data = {
            "first_name" : self.first_name_entry.text(),
            "last_name" : self.last_name_entry.text(),
            "quality" : self.qualify_entry.text(),
            "user_name" : self.user_name_entry.text(),

            "ins_name" : self.ins_name_entry.text(),
            "ins_address" : self.ins_address_entry.text(),
            "ins_number" : self.ins_number_entry.text(),

            "personal_number" : self.per_number.text(),
            "whatsapp_number" : self.whatsapp_entry.text(),
            "email" : self.email_entry.text(),

            "password" : self.enter_pw.text(),
            "pin" : int(self.exit_pin.text())
        }

        with open("db/profile.json", "w") as file:
            json.dump(data, file, indent=4)

        QMessageBox.information(self, "User Dialog Message", "User Profile Update Successfull", QMessageBox.StandardButton.Ok)

        super().accept()


if __name__ == "__main__":
    app = QApplication([])
    window = UserDialog()
    app.exec_()
