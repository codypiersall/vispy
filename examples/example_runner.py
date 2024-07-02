import pathlib
import os
import subprocess
import sys

from PyQt6 import QtWidgets, QtCore, QtGui

app = QtWidgets.QApplication([])

THIS_DIR = pathlib.Path(__file__).parent


class FileList(QtWidgets.QListWidget):
    def __init__(self, files: list[pathlib.Path]):
        super().__init__()

        self.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self._filenames = sorted([str(f) for f in files])
        # remove prefix for display purposes
        prefix = os.path.commonprefix(self._filenames)
        n = len(prefix)

        self._items = []
        self.itemDoubleClicked.connect(self.show_thing)
        self.installEventFilter(self)
        for f in self._filenames:
            item = QtWidgets.QListWidgetItem(f[n:])
            item.setData(1, f)
            self._items.append(item)
            self.addItem(item)

    def show_thing(self, item: QtWidgets.QListWidgetItem):
        subprocess.Popen([sys.executable, item.data(1)])

    def keyPressEvent(self, e):
        super().keyPressEvent(e)
        if e.key() == QtCore.Qt.Key.Key_Return:
            current = self.selectedItems()
            if current:
                self.show_thing(current[0])


class ConsoleWidget(QtWidgets.QTextEdit):
    pass


class VispyExampleViewer(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self._main_window = QtWidgets.QMainWindow()
        self._main_window.setMinimumSize(400, 800)
        self.files_dock = QtWidgets.QDockWidget()
        self.files_widget = FileList(list(THIS_DIR.rglob("*.py")))
        policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.files_widget.setSizePolicy(policy)
        self.files_dock.setWidget(self.files_widget)

        self.console_dock = QtWidgets.QDockWidget()
        self._main_window.addDockWidget(
            QtCore.Qt.DockWidgetArea.LeftDockWidgetArea, self.files_dock
        )
        # self.console_widget = ConsoleWidget()
        # self.console_dock.setWidget(self.console_widget)
        # self._main_window.addDockWidget(
        #     QtCore.Qt.DockWidgetArea.BottomDockWidgetArea, self.console_dock
        # )
        self.setCentralWidget(self._main_window)


mw = VispyExampleViewer()
mw.show()
app.exec()
