import json
import os
import shutil
import sys

from PyQt5.QtGui import QColor, QPalette, QFont, QIcon
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QStackedLayout, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QDesktopWidget, QFrame, QGridLayout, QGraphicsDropShadowEffect,
                             QInputDialog, QLineEdit, QMessageBox, QFileDialog)
from PyQt5.QtCore import QSize, Qt, QPropertyAnimation, QTime, QDate, QTimer, QEasingCurve
from PyQt5.QtGui import QColor

from file_manager.class_manager import ClassManager
from file_manager.student_manager import StudentManager

from widgets.time_table import TimeTableWidget
from widgets.containers import ContainerWidget
from widgets.students_viewer import StudentViewer
from widgets.daily_class_bar import DailyClassBar
from widgets.class_initializer import ClassInitializerWidget
from widgets.profile import Profile
from widgets.register_widgets.main_widget import Registor

from dialogs.class_dialog import classDialog
from dialogs.student_dialog import StudentDialog
from dialogs.user_dialog import UserDialog

from util.logger import Logger
from style_sheets.main_style_sheet import main_style_sheet

week_days = ["Monday", "TuesDay", "WednesDay", "ThursDay", "FriDay", "SaturDay", "SunDay"]

class ClassManagementSystem(QMainWindow):
    def __init__(self):
        super(ClassManagementSystem, self).__init__()
        self.initializeFiles()
        self.logToSystem()

        self.initializeUI()

    def initializeFiles(self):

        # create the student and class manager objects
        self.student_manager = StudentManager()
        self.class_manager = ClassManager()

        if not os.path.exists("db"):
            os.mkdir("db")
            self.student_manager.initiateTable()
            self.class_manager.initiateTable()
        if not os.path.exists("db/log_data.json"):
            with open("db/log_data.json", "w") as file:
                json.dump([], file, indent=4)

        if not os.path.exists("db/log"):
            os.mkdir("db/log")

        if not os.path.exists("db/classes"):
            os.mkdir("db/classes")

    def logToSystem(self):

        if not os.path.exists("db/profile.json"):
            # get the user data from user dialog
            self.user_dialog = UserDialog(self)

        # log to the system
        # ask the password for enters
        # get the password
        with open("db/profile.json") as file:
            password = json.load(file)["password"]

        again = True
        while again:
            pw, ok = QInputDialog.getText(self, "Password Dialog", "Enter Password", echo=QLineEdit.Password)
            if ok:
                if password == pw:
                    break
                else:
                    message  = QMessageBox.warning(self, "Password Dialog", "Your Passowrd is InCorrect, Are you want try again?",
                                                   QMessageBox.Yes|QMessageBox.StandardButton.No)
                    if message == QMessageBox.StandardButton.No:
                        self.close()
                        return
            else:
                again = False
                self.close()
                return

        # start the config logging
        log_file = f"{QDate.currentDate().toString('yyyyMMdd')}-{QTime.currentTime().toString('hh-mm')}.log"
        log_data = []
        with open("db/log_data.json") as file:
            log_data = json.load(file)

        log_data.append({
            "enter" : f"{QDate.currentDate().toString('yyyy MM dd')} {QTime.currentTime().toString('hh:mm')}",
            "log" : log_file
        })

        with open("db/log_data.json", "w") as file:
            json.dump(log_data, file, indent=4)

        self.logger = Logger(f"db/log/{log_file}")

    def initializeUI(self):

        # setting the window
        desktop_rect = QDesktopWidget().geometry()
        self.setGeometry(0, 30, desktop_rect.width(), desktop_rect.height())
        self.setAnimated(True)

        self.setWindowTitle("Class Management System")
        # create the main widget
        main_widget = QWidget()
        main_widget.setContentsMargins(0, 0, 0, 0)
        # create the layout for main widget
        self.main_h_box = QHBoxLayout()
        self.main_h_box.setContentsMargins(0, 0, 0, 0)
        self.main_h_box.setSpacing(0)
        main_widget.setLayout(self.main_h_box)


        self.setCentralWidget(main_widget)
        self.setUpMainWidget()

        # show the window in the screen
        self.show()

    def setUpMainWidget(self):

        # create the Frame for side  panel
        self.sidePanel = QWidget()
        self.sidePanel.setObjectName("sidePanel")
        self.sidePanel.setMaximumWidth(int(self.width() * 0.2))
        self.sidePanel.setGeometry(0, 0, 0, 0)


        # create the stack layout fot main page store
        self.mainStackLayout = QStackedLayout()
        self.mainStackLayout.setContentsMargins(0, 0, 0, 0)

        # add to the main widget
        self.main_h_box.addWidget(self.sidePanel)
        self.main_h_box.addLayout(self.mainStackLayout)


        self.setUpSidePanel()
        self.setUpMainPanel()

    def setUpSidePanel(self):

        # create the side panel layout
        side_panel_vbox = QVBoxLayout()
        side_panel_vbox.setContentsMargins(0, 0, 0, 0)
        self.sidePanel.setLayout(side_panel_vbox)

        # create the show and hide button
        show_hide_button  = QPushButton("=")
        show_hide_button.setObjectName("notRoundButton")
        show_hide_button.setFixedWidth(int(self.width() * 0.03))
        show_hide_button.pressed.connect(self.showAndHidePanel)
        show_hide_button.setFont(QFont("Hack", 12))

        # create the hbox for this
        hbox1 = QHBoxLayout()
        hbox1.addWidget(show_hide_button)
        hbox1.addStretch()

        # create the vbox for add the actions forside panel
        action_vbox = QVBoxLayout()
        self.setUpSidePanelActions(action_vbox)

        # add the button
        side_panel_vbox.addLayout(hbox1)
        side_panel_vbox.addLayout(action_vbox)
        side_panel_vbox.addStretch()

    def setUpSidePanelActions(self, layout : QVBoxLayout):

        # create the profile name label
        with open("db/profile.json")as file:
            profile_data = json.load(file)
            name = "Hi! {} {}".format(profile_data["first_name"], profile_data["last_name"])

        name_label = QLabel(name)
        name_label.setFont(QFont("verdana", 18))
        name_label.setWordWrap(True)
        name_label.setObjectName("name_label")

        # create the actions
        change_walpaper_action = QPushButton("change wallpaper")
        change_walpaper_action.setObjectName("side_panel_action")
        change_walpaper_action.pressed.connect(self.changeWallpaper)


        layout.addWidget(name_label)
        layout.addSpacing(20)
        layout.addWidget(change_walpaper_action)
        layout.addStretch()

    def showAndHidePanel(self):

        self.showHideAnimation = QPropertyAnimation(self.sidePanel, b'maximumWidth')
        self.showHideAnimation.setStartValue(self.sidePanel.width())
        self.showHideAnimation.setEasingCurve(QEasingCurve.InCurve)

        if (self.sidePanel.width() < self.width() * 0.2):
            # show the panel
            self.showHideAnimation.setEndValue(int(self.width() * 0.2))
        else:
            self.showHideAnimation.setEndValue(int(self.width() * 0.03))

        self.showHideAnimation.start()


    def setUpMainPanel(self):

        # crete the main page widget
        main_page = QWidget()
        main_page.setObjectName("mainPage")
        main_page.setContentsMargins(0, 0, 0, 0)
        # add to the stack layout
        self.mainStackLayout.addWidget(main_page)

        # create the button text list
        self.main_button_texts = ["Add Student", "Student Viewer", "Start New Class", "Register", "Payments", "Time Table", "Add New Class", "Online Works", "Events" ,
                                  "Exams", "Marks"]

        y0 = int(self.height() * 0.3)
        x0 = int(main_page.width() * 0.5)

        button_width = 230
        button_height = 150


        for i in range(len(self.main_button_texts)):
            # crate the button
            button = QPushButton(self.main_button_texts[i], parent=main_page)
            button.setObjectName("mainButtons")
            button.resize(QSize(button_width, button_height))

            shadow = QGraphicsDropShadowEffect()
            shadow.setColor(QColor(100, 100, 100))
            shadow.setBlurRadius(40)
            shadow.setXOffset(10)
            shadow.setYOffset(10)

            button.setGraphicsEffect(shadow)
            # set the button clicked event
            button.pressed.connect(lambda e = i : self.responseToButton(e))

            # add to the main page
            button.move(x0 + (i % 4) * button_width , y0 + (i // 4) * button_height)

        # create the time date label
        dateFont = QFont("Helvetica [Cronyx]", 85)
        dateFont.setBold(True)
        self.date_label = QLabel(QTime().currentTime().toString("hh:mm A"), main_page)
        self.date_label.setFont(dateFont)
        self.date_label.setObjectName("timeLabel")

        current_date = QDate().currentDate()
        week_day = week_days[current_date.dayOfWeek() - 1]
        self.time_label = QLabel("{}    {}".format(current_date.toString("dd MMM yyyy"), week_day), main_page)
        self.time_label.setFont(QFont("Helvetica [Cronyx]", 25))
        self.time_label.setObjectName("timeLabel")

        self.date_label.move(main_page.width()  + 200, 0)
        self.time_label.move(main_page.width()  + 200, 180)

        # create the timer object and update the time and dat enables
        self.mainTimer = QTimer()
        self.mainTimer.setInterval(1000)
        self.mainTimer.timeout.connect(self.updateTime)

        # setup the welcome message and profile buttons
        self.setUpProfile(main_page)

    def setUpProfile(self, page : QWidget):

        profile_button = QPushButton("Profile", page)
        profile_button.setObjectName("profileButton")
        profile_button.move(30, 30)
        profile_button.pressed.connect(self.openProfile)

        class_bar = DailyClassBar(page)
        class_bar.move(900, 800)

    def responseToButton(self, index : int):

        if self.main_button_texts[index] == "Time Table":
            # call to the time table open method
            self.openTimeTable()
        elif self.main_button_texts[index] == "Add New Class":
            # create the new dialog for class and show it
            self.newClassDialog = classDialog()
        elif self.main_button_texts[index] == "Student Viewer":
            self.openStudentViewer()
        elif self.main_button_texts[index] == "Add Student":
            self.newStudentDialog = StudentDialog()
        elif self.main_button_texts[index] == "Start New Class":
            self.initiateNewClass()
        elif self.main_button_texts[index] == "Register":
            self.openRegister()

    def openTimeTable(self):

        # create the time  table widget
        time_table = TimeTableWidget()
        # create the container widget
        container = ContainerWidget(time_table, "Time Table of Classes")

        # add to the stack widget
        self.mainStackLayout.addWidget(container)
        self.mainStackLayout.setCurrentIndex(1)

    def openStudentViewer(self):

        student_viewer = StudentViewer()
        # create the container
        container = ContainerWidget(student_viewer, "Students")

        self.mainStackLayout.addWidget(container)
        self.mainStackLayout.setCurrentIndex(1)

    def updateTime(self):

        self.time_label.setText(QTime.currentTime().toString("hh:mm A"))

        current_date = QDate().currentDate()
        week_day = week_days[current_date.dayOfWeek() - 1]
        self.date_label.setText("{}    {}".format(current_date.toString("dd MMMM yyyy"), week_day))

    def initiateNewClass(self):

        widget = ClassInitializerWidget()
        # create the container and studenr chooser
        container = ContainerWidget(widget, "Start New Class")

        self.mainStackLayout.addWidget(container)
        self.mainStackLayout.setCurrentIndex(1)

    def openProfile(self):

        widget = Profile(self)
        container = ContainerWidget(widget, "Profile")

        self.mainStackLayout.addWidget(container)
        self.mainStackLayout.setCurrentIndex(1)

    def changeWallpaper(self):

        # change the wallpaper of main window
        file, ok = QFileDialog.getOpenFileName(self, "Change Wallpaper", "D:/Gallery", "JPEG Files(*.jpg)")
        if ok:
            # copy the image to the image folder
            shutil.copyfile(file, "images/system_images/wallpaper.jpg")
            # set the again main style sheet to the window
            self.setStyleSheet(main_style_sheet)

    def openRegister(self):

        widget = Registor()
        container = ContainerWidget(widget, "Registor")

        self.mainStackLayout.addWidget(container)
        self.mainStackLayout.setCurrentIndex(1)

    def closeEvent(self, event) -> None:

        self.logger.close()
        del self.logger
        super().closeEvent(event)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(main_style_sheet)
    app.setWindowIcon(QIcon("images/system_images/app_icon.png"))

    window = ClassManagementSystem()
    app.exec_()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
