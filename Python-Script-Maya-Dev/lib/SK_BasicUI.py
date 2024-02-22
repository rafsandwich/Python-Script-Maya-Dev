__author__ = 'rik.joanmiquel'
import os
import sys

# Check shiboken version and load it
try:
    import shiboken2 as shiboken
except ImportError:
    import shiboken as shiboken
# Import Qt for compatibility with maya 2018
# import Qt.QtCore as QtCore
# import Qt.QtWidgets as QtWidgets
import maya.OpenMayaUI as OpenMayaUI

from Qt import QtCore
from Qt import QtWidgets

SETTINGS_FILE = "Settings"

def kill_existing_window(obj):
    """
    Tries to kill the existing window
    :param obj:
    :return:
    """
    for widget in QtWidgets.QApplication.topLevelWidgets():
        try:
            if widget.__class__.__name__ == obj:
                widget.close()
        except Exception as e:
            print(e.message)

def get_maya_window():
    """
    :return: The main maya window to parent to or none if it can't access it
    """
    access_main_window = OpenMayaUI.MQtUtil.mainWindow()

    if access_main_window:
        return shiboken.wrapInstance(int(access_main_window), QtWidgets.QWidget)
    else:
        return None

class SK_QWindow(QtWidgets.QMainWindow):
    """
    Extends QtWidgets.QMainWindow to create a simple Ui which can parent, close and keep settings
    """
    def __init__(self):
        _MainMayaWindow = get_maya_window()
        super(SK_QWindow, self).__init__(_MainMayaWindow)
        kill_existing_window(self.__class__.__name__)

        self.stuffWidget = QtWidgets.QWidget()

        self.mainW = QtWidgets.QWidget()
        self.setCentralWidget(self.mainW)

        self.restore_settings = True

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.settings = None

    def basic_UI(self):
        """
        Very simple basic UI layout
        :return:
        """
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainW.setLayout(mainLayout)
        mainLayout.addWidget(self.stuffWidget)

    def setLayout(self, layout):
        """
        Creates a basic layout to the stuff widget
        """
        self.stuffWidget.setLayout(layout)

    def showUI(self):
        """
        Loads and shows the UI
        """
        self.basic_UI()
        self.UI()
        self.show()
        self.read_settings()

    def closeEvent(self, event):
        """
        Simple close Event with write settings
        :param event:
        :return:
        """
        try:
            self.write_settings()
            event.accept()
        except Exception as e:
            print(e.message)

    def read_settings(self):
        """
        Reads how the window was prior to being closed
        :return:
        """
        self.settings = QtCore.QSettings(SETTINGS_FILE, self.windowTitle())
        if self.restore_settings:
            self.restoreGeometry(self.settings.value("geometry"))
        self.settings.endGroup()

    def write_settings(self):
        """
        stores how the window was prior to being closed
        :return:
        """
        self.settings = QtCore.QSettings(SETTINGS_FILE, self.windowTitle())
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.endGroup()