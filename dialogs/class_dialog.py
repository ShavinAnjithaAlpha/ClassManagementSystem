from PyQt5.QtWidgets import (QWidget,QApplication, QDialog, QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox, QLabel,
                             QGroupBox, QButtonGroup, QVBoxLayout, QPushButton, QStackedLayout, QRadioButton, QFormLayout, QHBoxLayout,
                             QMessageBox)
from PyQt5.QtCore import Qt, QSize, QDate
from file_manager.class_manager import ClassManager

class classDialog(QDialog):

    subjects = ["Chemistry", "Physics", "Mathematics", "ÏCT", "Sinhala", "English"]

    def __init__(self):
        super(classDialog, self).__init__()
        self.setModal(True)
        self.setWindowTitle("New Class Dialog")
        self.setFixedSize(QSize(400, 400))

        # create the new UI
        self.initializeUI()
        self.show()

    def initializeUI(self):

        # create the stack layout
        self.stackLyt = QStackedLayout()

        # create the current widget
        main_widget = QWidget()
        self.display_widget = QWidget()

        self.stackLyt.addWidget(main_widget)
        self.stackLyt.addWidget(self.display_widget)

        # create the main vbox for this
        vbox  = QVBoxLayout()
        main_widget.setLayout(vbox)

        self.setLayout(self.stackLyt)

        # create the two group box and one hbox
        self.classBox = QGroupBox("Class Informations")
        self.paymentBox = QGroupBox("Payment Infomations")

        hbox = QHBoxLayout()

        # create the buttons
        save_button = QPushButton("Next")
        cancel_button  = QPushButton("Cancel")

        # set the method for buttons
        save_button.pressed.connect(self.submit)
        cancel_button.pressed.connect(self.reject)

        hbox.addWidget(save_button)
        hbox.addWidget(cancel_button)

        vbox.addWidget(self.classBox)
        vbox.addWidget(self.paymentBox)
        vbox.addLayout(hbox)

        self.setUpClassBox()
        self.setUpPaymentBox()

    def setUpDislayWidget(self, data : dict):

        self.display_widget.deleteLater()
        self.display_widget = QWidget()
        self.stackLyt.addWidget(self.display_widget)

        # create form layout
        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignRight)
        form.setFormAlignment(Qt.AlignVCenter)

        form.addRow("Class Name" , QLabel(data["className"]))
        form.addRow("Grade", QLabel(f"grade {data['grade']}"))
        form.addRow("Subject" , QLabel(f"{data['subject']}"))
        form.addRow("Class Type" , QLabel(data['type']))
        form.addRow("Cash (Rs.)" , QLabel(f"{data['cash']}"))

        # create hboc for buttons
        hbox = QHBoxLayout()

        save_button = QPushButton("Save")
        cancel_button = QPushButton("Cancel")
        back_button = QPushButton("Back")

        save_button.pressed.connect(lambda e = data : self.accept(e))
        cancel_button.pressed.connect(self.reject)
        back_button.pressed.connect(lambda  : self.stackLyt.setCurrentIndex(0))

        hbox.addWidget(back_button)
        hbox.addWidget(save_button)
        hbox.addWidget(cancel_button)

        save_button.setFocus()

        vbox = QVBoxLayout()
        vbox.addLayout(form)
        vbox.addLayout(hbox)

        self.display_widget.setLayout(vbox)

    def setUpClassBox(self):

        # create the class name edit
        self.name_entry = QLineEdit()
        self.name_entry.resize(200, 40)

        self.grade_box = QSpinBox()
        self.grade_box.setMinimum(1)

        self.subject_box = QComboBox()
        self.subject_box.addItems(self.subjects)
        self.subject_box.setCurrentIndex(0)
        self.subject_box.setEditable(True)

        # create the form layout
        form = QFormLayout()
        form.setVerticalSpacing(15)
        form.setLabelAlignment(Qt.AlignRight)
        form.setFormAlignment(Qt.AlignCenter)

        form.addRow("Class Name", self.name_entry)
        form.addRow("Grade", self.grade_box)
        form.addRow("Subject" , self.subject_box)

        self.classBox.setLayout(form)

    def setUpPaymentBox(self):

        # create the radio buttons
        daily_radio = QRadioButton("Daily")
        monthly_radio = QRadioButton("Monthly")

        daily_radio.setChecked(True)
        daily_radio.setAutoExclusive(True)

        # create radio group box
        self.button_group = QButtonGroup()
        self.button_group.addButton(daily_radio, 0)
        self.button_group.addButton(monthly_radio, 1)

        # create hbox for pack the radio buttons
        hbox = QHBoxLayout()
        hbox.addWidget(daily_radio)
        hbox.addWidget(monthly_radio)

        self.cash_box = QDoubleSpinBox()
        self.cash_box.setMinimum(0.00)
        self.cash_box.setDecimals(2)
        self.cash_box.setMaximum(10000)

        # add to the layout
        form = QFormLayout()
        form.setVerticalSpacing(15)
        form.setLabelAlignment(Qt.AlignRight)
        form.setFormAlignment(Qt.AlignCenter)

        form.addRow("Class Type", QLabel())
        form.addItem(hbox)
        form.addRow("Cash (Rs.)", self.cash_box)

        self.paymentBox.setLayout(form)

    def submit(self) -> None:

        # collect the data and check the all of the data fileds are filled
        if self.name_entry.text() == "":
            self.name_entry.setFocus()
            return
        if self.cash_box.value() == 0:
            self.cash_box.setFocus()
            return

        classType = "day" if self.button_group.checkedId() == 0 else "monthly"

        data = {
            "className" : self.name_entry.text(),
            "grade" : self.grade_box.value(),
            "subject" : self.subject_box.currentText(),
            "type" : classType,
            "cash" : self.cash_box.value()
        }

        self.setUpDislayWidget(data)
        self.stackLyt.setCurrentIndex(1)

    def accept(self, data : dict) -> None:

        # create the class manager object
        class_manager = ClassManager()
        class_manager.addClass(data, "../db/main.db")

        QMessageBox.information(self, "Information", "Class Save Successfully", QMessageBox.StandardButton.Ok)

        super().accept()



if __name__ == "__main__":
    app = QApplication([])
    window = classDialog()
    app.exec_()


