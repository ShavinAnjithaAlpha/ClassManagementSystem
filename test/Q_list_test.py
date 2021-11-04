from PyQt5.QtCore import QModelIndex, Qt, QSize, QAbstractListModel, QMargins
from PyQt5.QtGui import QPainter, QColor, QPen, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QListView, QListWidget, QHBoxLayout, QListWidgetItem, \
    QStyledItemDelegate, QStyleOptionViewItem


class delegate(QStyledItemDelegate):
    def __init__(self):
        super(delegate, self).__init__()

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex) -> None:

        # get the data from model index
        text = index.model().data(index, Qt.DisplayRole)

        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing)
        # draw the text
        painter.setBrush(QColor(0, 0, 100))
        painter.setPen(QColor(250, 0, 0))

        # painter.setPen(QColor(100, 0, 0))
        painter.drawRoundedRect(option.rect, 25, 35)
        painter.setBrush(QColor(0, 0, 250))
        # painter.drawEllipse(option.rect.marginsRemoved(QMargins(2, 2, 2, 2)))
        painter.setFont(QFont("segoe UI", 25))
        painter.drawText(option.rect.center() , text)


    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex) -> QSize:

        text = index.model().data(index, Qt.DisplayRole)
        font_size = QApplication.fontMetrics()
        rect = font_size.boundingRect(option.rect, Qt.TextWordWrap, text)
        rect.marginsAdded(QMargins(50, 50, 50, 50))
        return QSize(rect.width(), 100)


class model(QAbstractListModel):
    def __init__(self, name_list: list):
        super(model, self).__init__()
        self.name_list = name_list

    def data(self, index: QModelIndex, role: int):

        if role == Qt.DisplayRole:
            return self.name_list[index.row()]

    def rowCount(self, parent: QModelIndex) -> int:

        return len(self.name_list)


if __name__ == "__main__":
    app = QApplication([])
    widget = QListView()
    widget.setModel(model(["shavin", "reshani", "kasun", "pytha"]))
    widget.setItemDelegate(delegate())


    widget.show()
    app.exec_()