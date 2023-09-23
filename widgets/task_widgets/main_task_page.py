from PyQt5.QtWidgets import (QWidget, QLabel, QPushButton, QLineEdit, QCheckBox, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QStackedLayout, QTextEdit, QDateEdit, QTimeEdit, QGroupBox, QFileDialog, QScrollArea,
                             QMessageBox, QInputDialog, QAction, QMenu)
from PyQt5.QtCore import Qt, QSize, QDate, QTime
from PyQt5.QtGui import QFont, QPixmap, QContextMenuEvent

from file_manager.task_manager import TaskManger

from style_sheets.task_page_style_sheet import style_sheet

class Tasklabel(QWidget):
    def __init__(self, title : str , is_completed : bool, date : str):
        super(Tasklabel, self).__init__()
        self.setMinimumHeight(120)

        self.is_completed = is_completed
        self.date = date
        self.title = title

        # create the label of completed
        image_label = QLabel()
        image_label.setFixedSize(QSize(50, 50))
        self.setUpCompleted(image_label)
        image_label.mousePressEvent = lambda event , label = image_label : self.setUpCompleted(label, True)
        # create the title label
        title_label = QLabel(title)
        title_label.setWordWrap(True)
        title_label.setObjectName("title_label")

        date_label = QLabel(date)
        date_label.setObjectName("date_label")

        base = QWidget()

        base.setLayout(QHBoxLayout())
        base.layout().addWidget(image_label)
        base.layout().addWidget(title_label)
        base.layout().addWidget(date_label)

        lyt = QHBoxLayout()
        lyt.setContentsMargins(0, 0, 0, 0)
        self.setLayout(lyt)
        self.setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(base)
        self.setStyleSheet("""
                QWidget {background-color : rgb(0, 20, 100);
                        margin : 0px;
                        border : none;
                        border-bottom : 1px solid rgb(0, 0, 140);}
                        
                QWidget:hover {background-color : rgb(0, 20, 110)}
                QWidget:pressed {background-color : rgb(0, 20, 120)}
                        
                QLabel {background : none;
                        border : none;}
                
                QLabel#title_label {
                            color : white;
                            font-size : 25px;
                            margin : 5px;}
                            
                QLabel#date_label {font-size : 16px;
                                color : rgb(0, 40, 250)}
                            
                """)

    def setUpCompleted(self, label : QLabel, change : bool = False):

        if change:
            self.is_completed = not(self.is_completed)
            TaskManger.setAsComplete(self.title , QDate.fromString(self.date , "yyyy MMM dd"), self.is_completed)

        if self.is_completed:
            label.setPixmap(QPixmap("images/system_images/completed_oval.png").scaled(label.size() , Qt.KeepAspectRatio , Qt.FastTransformation))
        else:
            label.setPixmap(QPixmap("images/system_images/not_complete_oval.png").scaled(label.size(), Qt.KeepAspectRatio,
                                                                                 Qt.FastTransformation))

    def contextMenuEvent(self, event  : QContextMenuEvent) -> None:

        # create the action
        delete_action = QAction("delete")
        delete_action.triggered.connect(self.deleteTask)

        context_menu = QMenu()
        context_menu.addAction(delete_action)

        context_menu.exec_(self.mapToGlobal(event.pos()))

    def deleteTask(self):

        stat = QMessageBox.warning(self, "delete task", "Are you want to delete task?",
                                   QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No)
        if stat == QMessageBox.StandardButton.Yes:

            # delete from the task file
            TaskManger.deleteTask(self.title , self.date)

            self.deleteLater()

class TaskPage(QWidget):
    def __init__(self):

        self.sub_tasks_count = 0
        self.sub_tasks = []
        self.choosed_images = []
        self.task_cards = []


        self.task_month = QDate.currentDate().month()
        self.task_year = QDate.currentDate().year()

        super(TaskPage, self).__init__()
        # create the side panel and stack layout for content
        self.side_panel = QWidget()
        self.side_panel.setContentsMargins(0, 0, 0, 0)
        self.side_panel.setObjectName("side_panel")
        self.side_panel.setMaximumWidth(400)

        # create the stack layout for content
        self.stackLyt = QStackedLayout()
        self.stackLyt.setContentsMargins(0, 0, 0, 0)

        # create the task viewer panel
        self.taskViewerPanel = QWidget()
        # create the new task panel
        self.newTaskPanel = QScrollArea()
        self.newTaskPanel.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.newTaskPanel.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.newTaskPanel.setObjectName("newTaskPanel")

        self.stackLyt.addWidget(self.taskViewerPanel)
        self.stackLyt.addWidget(self.newTaskPanel)
        self.stackLyt.setCurrentIndex(1)

        # create the h box for pack this
        hbox = QHBoxLayout()
        hbox.setSpacing(0)
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.addWidget(self.side_panel)
        hbox.addLayout(self.stackLyt)

        self.setLayout(hbox)

        self.setUpSidePanel()
        self.setUpNewTaskPage()

        self.setStyleSheet(style_sheet)

    def setUpSidePanel(self):

        w = QWidget()
        w.setObjectName("scroll_area_widget")
        w.setMaximumWidth(400)
        w.setContentsMargins(0, 0, 0, 0)
        # create the scroll area
        scroll_area = QScrollArea()
        scroll_area.setMaximumWidth(400)
        scroll_area.setContentsMargins(0, 0, 0, 0)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(w)

        self.side_vbox = QVBoxLayout() # vbox for pack the task  labels
        self.side_vbox.setContentsMargins(0, 0, 0, 0)
        self.side_vbox.setSpacing(0)
        # create the task bars
        data = TaskManger.getTasksForMonth(QDate.currentDate().year() , QDate.currentDate().month())

        for task in data:
            task_label  = Tasklabel(task["title"], task["is_completed"], task["date"])
            task_label.mouseDoubleClickEvent = lambda event, data = task : self.openTask(data)
            self.task_cards.append(task_label)
            self.side_vbox.addWidget(task_label)

        self.side_vbox.addStretch()
        scroll_area.setLayout(self.side_vbox)

        lyt = QVBoxLayout()
        lyt.setContentsMargins(0, 0, 0, 0)
        self.side_panel.setLayout(lyt)
        self.side_panel.layout().addWidget(scroll_area)

        # create the change month and year attributes
        label_1 = QLabel("month")
        label_2 = QLabel("year")

        label_1.setObjectName("label")
        label_2.setObjectName("label")

        month_button = QPushButton(f"{QDate.longMonthName(QDate.currentDate().month())}")
        year_button = QPushButton(f"{QDate.currentDate().year()}")

        month_button.pressed.connect(lambda b = month_button : self.changeMonth(b))
        year_button.pressed.connect(lambda b = year_button : self.changeYear(b))

        month_button.setObjectName("changeButton")
        year_button.setObjectName("changeButton")

        # create the new task button
        new_task_button = QPushButton("+ New Task")
        new_task_button.pressed.connect(lambda  : self.stackLyt.setCurrentIndex(1))
        new_task_button.setObjectName("new_task_button")

        self.side_panel.layout().addWidget(label_1)
        self.side_panel.layout().addWidget(month_button)
        self.side_panel.layout().addWidget(label_2)
        self.side_panel.layout().addWidget(year_button)
        self.side_panel.layout().addSpacing(15)
        self.side_panel.layout().addWidget(new_task_button)

    def changeMonth(self , button : QPushButton):

        text , ok = QInputDialog.getItem(self, "Month Choose Dialog", "Choose Month : ",
                    [QDate.shortMonthName(i) for i in range(1, 13)], 0)
        if ok:
            button.setText(text)
            self.task_month = [QDate.shortMonthName(i) for i in range(1, 13)].index(text) + 1
            # call to change task bar
            self.updateTaskBar()

    def changeYear(self, button : QPushButton):

        year , ok = QInputDialog.getInt(self ,"Year Choose Dialog", "Choose Year : ", QDate.currentDate().year() ,
                                        2000, 2500, 1)
        if ok:
            button.setText(f"{year}")
            self.task_year = year
            # call to the change task bar
            self.updateTaskBar()

    def updateTaskBar(self):

        try:
            data = TaskManger.getTasksForMonth(self.task_year, self.task_month)
            # clear the task bar
            [widget.deleteLater() for widget in self.task_cards]
            self.task_cards.clear()

            for task in data:
                task_label = Tasklabel(task["title"], task["is_completed"], task["date"])
                task_label.mouseDoubleClickEvent = lambda event, data=task: self.openTask(data)
                self.task_cards.append(task_label)
                self.side_vbox.insertWidget(0, task_label)
        except:
            pass
            # QMessageBox.warning(self, "File Not Found Warning", "File for this year and month is removed or crashed!")





    def openTask(self, data):

        label = QLabel(f"{data}")
        label.setWordWrap(True)
        vbox = QVBoxLayout()
        vbox.addWidget(label)

        self.taskViewerPanel.setLayout(vbox)
        self.stackLyt.setCurrentIndex(0)

    def setUpNewTaskPage(self):


        widget = QWidget()
        widget.setObjectName("newTaskPanel")
        self.newTaskPanel.setWidget(widget)
        self.newTaskPanel.setWidgetResizable(True)

        # create the title edit
        title_edit = QLineEdit()
        title_edit.setPlaceholderText("Title")
        title_edit.setObjectName("title_edit")
        # title_edit.returnPressed.connect(lambda : title_edit.set)

        des_edit = QTextEdit()
        des_edit.setPlaceholderText("description about the task")
        des_edit.setMinimumWidth(500)
        des_edit.setMaximumHeight(350)

        # create the end date and time
        end_date_box = QDateEdit()
        end_date_box.setCalendarPopup(True)
        end_date_box.setDate(QDate.currentDate())

        end_time_box = QTimeEdit()
        end_time_box.setTime(QTime.currentTime())

        # create the hbox
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel("End Date and Time"))
        hbox.addWidget(end_date_box)
        hbox.addWidget(end_time_box)

        # create the sub tasks box
        grBox = QGroupBox("Sub Tasks")
        grBox.setMinimumHeight(300)
        # create the vox for this
        sub_tasks_vbox = QVBoxLayout()
        sub_tasks_vbox.setContentsMargins(0, 0, 0, 0)
        grBox.setLayout(sub_tasks_vbox)

        # create the edit for add tasks
        sub_task_edit = QLineEdit()
        sub_task_edit.setVisible(False)
        sub_task_edit.returnPressed.connect(lambda l = sub_tasks_vbox, w = sub_task_edit : self.addSubTask(l, w))
        sub_task_edit.setObjectName("sub_task_edit")
        sub_tasks_vbox.addWidget(sub_task_edit)

        # create the new sub task button bar
        new_subtask_button = QPushButton("+ New sub Task")
        new_subtask_button.setObjectName("newSubTaskButton")
        new_subtask_button.pressed.connect(lambda : sub_task_edit.setVisible(True))
        sub_tasks_vbox.addWidget(new_subtask_button)
        sub_tasks_vbox.addStretch()

        # create the file choose box
        image_box = QGridLayout()
        # create the button for choose the images
        image_choose_button = QPushButton("+ choose images")
        image_choose_button.pressed.connect(lambda l = image_box : self.chooseImages(l))
        image_box.addWidget(image_choose_button, 0, 0)

        save_button = QPushButton("Save")
        save_button.pressed.connect(lambda w1=title_edit , w2 = des_edit , w3 = end_date_box , w4 = end_time_box :
                                    self.saveTask(w1, w2, w3, w4))

        vbox = QVBoxLayout()
        vbox.addWidget(save_button, alignment=Qt.AlignRight)
        vbox.addWidget(title_edit, alignment=Qt.AlignHCenter)
        vbox.addWidget(des_edit)
        vbox.addLayout(hbox)
        vbox.addWidget(grBox)
        vbox.addWidget(QLabel("Choose Images"), alignment=Qt.AlignLeft)
        vbox.addLayout(image_box)


        widget.setLayout(vbox)

    def chooseImages(self, layout : QHBoxLayout):

        # open the file chooser
        files , ok = QFileDialog.getOpenFileNames(self, "Choose Images", "D:/Gallery", "JPG Files(*.jpg);; PNG Files(*.png)")
        if ok:
            i = len(self.choosed_images)
            # add to the list and UI
            [self.choosed_images.append(file) for file in files]
            for file in files:
                # create the label
                imageLabel = QLabel()
                imageLabel.setFixedSize(QSize(300, 300))
                imageLabel.setPixmap(QPixmap(file).scaled(imageLabel.size() , Qt.KeepAspectRatioByExpanding ,Qt.FastTransformation))
                # add to the layout
                layout.addWidget(imageLabel, i//3 + 1, i%3)
                i += 1

    def addSubTask(self, layout : QVBoxLayout, edit : QLineEdit):

        self.sub_tasks_count += 1
        # get the edit text
        text = edit.text()
        self.sub_tasks.append(text)
        # add to the layout
        layout.insertWidget(0, QLabel(f"{self.sub_tasks_count}. {text}"))
        # clear the edit
        edit.clear()
        # hide the sub task edit box
        edit.setVisible(False)

    def saveTask(self, title_edit : QLineEdit , des_edit : QTextEdit , end_date = QDateEdit, end_time = QTimeEdit):

        # create the task manager
        TaskManger.addNewtask(title_edit.text() ,
                                end_date.date() , end_time.time() ,
                                des= des_edit.toPlainText() , sub_tasks=self.sub_tasks , images=self.choosed_images)

        # show the message dialog
        QMessageBox.information(self, "Create new task", "Successfully Save the Yout Task", QMessageBox.StandardButton.Ok)

        # add the new task card to task bar
        task_card = Tasklabel(title_edit.text() , False ,QDate.currentDate().toString("yyyy MMM dd"))
        self.side_vbox.insertWidget(0, task_card)
