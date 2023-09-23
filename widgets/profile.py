import json
import shutil

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QWidget, QPushButton, QLabel, QLineEdit, QHBoxLayout, QGroupBox, QFormLayout, QVBoxLayout,
                             QFileDialog, QScrollArea, QGridLayout)
from PyQt5.QtCore import Qt, QSize

from style_sheets.profile_style_sheet import style_sheets
from style_sheets.main_style_sheet import main_style_sheet

profile_json_file = "db/profile.json"

class ProfileItem(QWidget):
    def __init__(self, json_attr : str , input_mask : str = None):
        super(ProfileItem, self).__init__()
        self.setContentsMargins(0, 0, 0, 0)
        # initialize the UI
        self.json_attr = json_attr
        self.value = self.loadValue()

        # create the value label
        self.value_label = QLabel(str(self.value))
        self.value_label.setObjectName("item_label")

        self.edit_entry = QLineEdit()
        self.edit_entry.resize(300, 30)

        if input_mask != "":
            self.edit_entry.setInputMask(input_mask)
        self.edit_entry.hide()
        self.edit_entry.returnPressed.connect(self.edit)

        self.edit_button = QPushButton("edit")
        self.edit_button.setObjectName("edit_button")
        self.edit_button.pressed.connect(self.edit)

        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(self.value_label)
        self.layout().addWidget(self.edit_entry)
        self.layout().addWidget(self.edit_button)
        self.layout().addStretch()

    def loadValue(self):

        with open(profile_json_file) as file:
            data = json.load(file)
            value = data[self.json_attr]

        return value

    def edit(self):

        if self.edit_button.text() == "edit":

            self.edit_entry.show()
            self.value_label.hide()

            self.edit_entry.setText(self.value_label.text())
            self.edit_button.setText("save")

        else:
            # save the current value
            self.edit_entry.hide()
            self.value_label.setText(self.edit_entry.text())
            self.value_label.show()

            self.edit_button.setText("edit")

            with open(profile_json_file) as file:
                data = json.load(file)
                data[self.json_attr] = self.edit_entry.text()

            with open(profile_json_file, "w")as file:
                json.dump(data , file, indent=4)

class Profile(QWidget):
    def __init__(self, parent = None):
        super(Profile, self).__init__(parent)

        # create the scroll area for this
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(scroll_area)

        # begin the  build the UI
        basic_attr = {
            "First Name" : "first_name",
            "Last Name" : "last_name",
            "Quality" : "quality",
            "User Name" : "user_name"

        }

        ins_attr = {
            "Institute Name" : "ins_name",
            "Institute Address" : "ins_address",
            "Institute Contact Number" : "ins_number"
        }

        contact_attr = {
            "Personal Contact Number" : "personal_number",
            "WhatsApp Number" : "whatsapp_number",
            "E Mail Address" : "email"
        }

        # now build the forms
        group_box1 = QGroupBox("Basic Info")
        form1 = QFormLayout()
        form1.setVerticalSpacing(0)
        form1.setFormAlignment(Qt.AlignTop)
        form1.setLabelAlignment(Qt.AlignRight)

        group_box1.setLayout(form1)

        for field in basic_attr.keys():
            form1.addRow(field, ProfileItem(basic_attr[field]))

        group_box2 = QGroupBox("Institute Info")
        form2 = QFormLayout()
        form2.setVerticalSpacing(0)
        form2.setFormAlignment(Qt.AlignTop)
        form2.setLabelAlignment(Qt.AlignRight)

        group_box2.setLayout(form2)

        for field in ins_attr.keys():
            if field == "Institute Contact Number":
                form2.addRow(field, ProfileItem(ins_attr[field], "xxx-xx xx xxx"))
                continue
            form2.addRow(field, ProfileItem(ins_attr[field]))

        group_box3 = QGroupBox("Contact Info")
        form3 = QFormLayout()
        form3.setVerticalSpacing(0)
        form3.setFormAlignment(Qt.AlignTop)
        form3.setLabelAlignment(Qt.AlignRight)

        group_box3.setLayout(form3)

        for field in contact_attr.keys():
            if field == "E Mail Address":
                form3.addRow(field, ProfileItem(contact_attr[field]))
                continue
            form3.addRow(field, ProfileItem(contact_attr[field], "xxx-xx xx xxx"))


        # create the wall paper change button
        self.wallpaper_label = QLabel()
        self.wallpaper_label.setFixedSize(QSize(600, 550))
        self.wallpaper_label.setPixmap(QPixmap("images/system_images/wallpaper.jpg").scaled(self.wallpaper_label.size(),
                                        Qt.KeepAspectRatio, Qt.SmoothTransformation))

        change_button = QPushButton("change")
        change_button.pressed.connect(self.changeWallpaper)

        hbox = QHBoxLayout()
        hbox.addWidget(QLabel("Wallpaper"))
        hbox.addWidget(self.wallpaper_label)
        hbox.addWidget(change_button)
        hbox.addStretch()

        # create the security box
        security_box = QGroupBox("Security")
        self.setUpSecurityBox(security_box)

        base = QWidget()
        base.setObjectName("base")
        scroll_area.setWidget(base)

        vbox = QVBoxLayout()
        vbox.addWidget(group_box1)
        vbox.addWidget(group_box2)
        vbox.addWidget(group_box3)
        vbox.addWidget(security_box)
        vbox.addLayout(hbox)

        base.setLayout(vbox)
        self.setStyleSheet(style_sheets)

    def setUpSecurityBox(self, box : QGroupBox):

        # create the grid layout for this
        grid = QGridLayout()

        # create the password section
        des_label1 = QLabel("""Password give the authorized access to this system and confirm some\n
                                high priority processes.""")
        des_label1.setAlignment(Qt.AlignLeft)
        des_label1.setObjectName("des_label")

        grid.addWidget(des_label1, 0, 0, 1, 4)
        grid.addWidget(QLabel("Current Password"), 1, 1)
        grid.addWidget(QLabel("New Password"), 1, 2)
        grid.addWidget(QLabel("Confirm Password"), 1, 3)
        grid.addWidget(QLabel("Change Password"), 2, 0)

        self.current_pw_box = QLineEdit()
        self.current_pw_box.setEchoMode(QLineEdit.Password)
        self.current_pw_box.setObjectName("passwordBox")

        self.new_pw_box = QLineEdit()
        self.new_pw_box.setEchoMode(QLineEdit.Password)
        self.new_pw_box.setObjectName("passwordBox")

        self.confirm_pw_box = QLineEdit()
        self.confirm_pw_box.setEchoMode(QLineEdit.Password)
        self.confirm_pw_box.setObjectName("passwordBox")

        grid.addWidget(self.current_pw_box, 2, 1)
        grid.addWidget(self.new_pw_box, 2, 2)
        grid.addWidget(self.confirm_pw_box, 2, 3)

        box.setLayout(grid)

    def changeWallpaper(self):

        file, ok = QFileDialog.getOpenFileName(self, "Change Wallpaper", "D:/Gallery", "JPEG Files(*.jpg)")
        if ok:
            # copy the file
            shutil.copyfile(file, "images/system_images/wallpaper.jpg")
            self.wallpaper_label.setPixmap(
                QPixmap(file).scaled(self.wallpaper_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            )

            self.parent().setStyleSheet(main_style_sheet)