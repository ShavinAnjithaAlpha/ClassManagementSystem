from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QStackedLayout, QVBoxLayout
from PyQt5.QtCore import Qt, QSize, QDate

from widgets.register_widgets.registor_widget import RegisterWidget
from widgets.register_widgets.current_class_bar import ClassBar

class Registor(QWidget):
    def __init__(self):
        super(Registor, self).__init__()

        # create the class bar widget
        class_bar = ClassBar()
        class_bar.registor_signal.connect(self.openNewRegistor)
        # create the stack layout for pack the other widgets
        self.stack_lyt = QStackedLayout()

        # crate the main laoyut
        vbox = QVBoxLayout()
        vbox.addWidget(class_bar)
        vbox.addLayout(self.stack_lyt)
        vbox.addStretch()

        self.setLayout(vbox)

    def openNewRegistor(self, cls_id : int):

        if self.stack_lyt.count() > 0:
            self.stack_lyt.widget(0).deleteLater()

        # create teh new register widget
        register_widget = RegisterWidget(cls_id, QDate.currentDate().year())

        self.stack_lyt.addWidget(register_widget)



