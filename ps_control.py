from PyQt5 import QtCore, QtGui, QtWidgets
import nidaqmx
from time import sleep
import sys
import nidaqmx.system
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget
from math import e, sin

import diploe_field_ML as dipfield
import beam_energy_ML as beamenergy


gorcakic_solenoid = 5
gorcakic_dipole = 2

sol_value = 0
dip_value = 0

max_sol = 10

max_dip = 5
min_dip = -5

degauss_time = 7
degauss_freq = 20


class WinForm(QWidget):
    def __init__(self, parent=None):
        super(WinForm, self).__init__(parent)

    def setupUi(self, window):
        window.setObjectName("window")
        window.resize(956, 561)
        font = QtGui.QFont()
        font.setPointSize(16)
        window.setFont(font)
        window.setMouseTracking(False)
        window.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(189, 189, 189, 255), stop:0.842105 rgba(255, 255, 255, 255));")
        self.widget = QtWidgets.QWidget(window)
        self.widget.setObjectName("widget")
        self.solenoid = QtWidgets.QFrame(self.widget)
        self.solenoid.setGeometry(QtCore.QRect(10, 10, 371, 521))
        self.solenoid.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(160, 160, 160, 255), stop:0.842105 rgba(255, 255, 255, 255));")
        self.solenoid.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.solenoid.setFrameShadow(QtWidgets.QFrame.Raised)
        self.solenoid.setObjectName("solenoid")
        self.solenoid_title = QtWidgets.QLabel(self.solenoid)
        self.solenoid_title.setGeometry(QtCore.QRect(20, 20, 341, 61))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.solenoid_title.setFont(font)
        self.solenoid_title.setStyleSheet("background-color: rgb(185, 185, 185);")
        self.solenoid_title.setIndent(30)
        self.solenoid_title.setOpenExternalLinks(False)
        self.solenoid_title.setObjectName("solenoid_title")
        self.lcd_solenoid = QtWidgets.QLCDNumber(self.solenoid)
        self.lcd_solenoid.setGeometry(QtCore.QRect(20, 90, 151, 81))
        self.lcd_solenoid.setAutoFillBackground(False)
        self.lcd_solenoid.setStyleSheet("color: rgb(18, 223, 14);\n"
                                        "background-color: rgb(0, 0, 0);")
        self.lcd_solenoid.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lcd_solenoid.setFrameShadow(QtWidgets.QFrame.Plain)
        self.lcd_solenoid.setSmallDecimalPoint(False)
        self.lcd_solenoid.setDigitCount(4)
        self.lcd_solenoid.setMode(QtWidgets.QLCDNumber.Dec)
        self.lcd_solenoid.setSegmentStyle(QtWidgets.QLCDNumber.Filled)
        self.lcd_solenoid.setProperty("value", 0.0)
        self.lcd_solenoid.setProperty("intValue", 0)
        self.lcd_solenoid.setObjectName("lcd_solenoid")
        self.value_solenoid = QtWidgets.QDoubleSpinBox(self.solenoid)
        self.value_solenoid.setGeometry(QtCore.QRect(20, 210, 151, 51))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.value_solenoid.setFont(font)
        self.value_solenoid.setMouseTracking(False)
        self.value_solenoid.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.value_solenoid.setAcceptDrops(False)
        self.value_solenoid.setWrapping(False)
        self.value_solenoid.setFrame(True)
        self.value_solenoid.setAccelerated(False)
        self.value_solenoid.setProperty("showGroupSeparator", False)
        self.value_solenoid.setDecimals(2)
        self.value_solenoid.setMaximum(max_sol)
        self.value_solenoid.setSingleStep(0.01)
        self.value_solenoid.setObjectName("value_solenoid")
        self.set_solenoid = QtWidgets.QCommandLinkButton(self.solenoid)
        self.set_solenoid.setGeometry(QtCore.QRect(20, 310, 101, 48))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.set_solenoid.setFont(font)
        self.set_solenoid.setAutoFillBackground(False)
        self.set_solenoid.setStyleSheet("background-color: rgb(0, 255, 0);\n"
                                        "")
        self.set_solenoid.setAutoDefault(False)
        self.set_solenoid.setDefault(True)
        self.set_solenoid.setObjectName("set_solenoid")
        self.label = QtWidgets.QLabel(self.solenoid)
        self.label.setGeometry(QtCore.QRect(170, 210, 31, 51))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiLight")
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setAutoFillBackground(False)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.solenoid)
        self.label_2.setGeometry(QtCore.QRect(170, 90, 31, 81))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiLight")
        font.setPointSize(24)
        self.label_2.setFont(font)
        self.label_2.setAutoFillBackground(False)
        self.label_2.setObjectName("label_2")
        self.lcd_solenoid_field = QtWidgets.QLCDNumber(self.solenoid)
        self.lcd_solenoid_field.setGeometry(QtCore.QRect(220, 90, 101, 51))
        self.lcd_solenoid_field.setAutoFillBackground(False)
        self.lcd_solenoid_field.setStyleSheet("color: rgb(18, 223, 14);\n"
                                              "background-color: rgb(0, 0, 0);")
        self.lcd_solenoid_field.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lcd_solenoid_field.setFrameShadow(QtWidgets.QFrame.Plain)
        self.lcd_solenoid_field.setSmallDecimalPoint(False)
        self.lcd_solenoid_field.setDigitCount(4)
        self.lcd_solenoid_field.setMode(QtWidgets.QLCDNumber.Dec)
        self.lcd_solenoid_field.setSegmentStyle(QtWidgets.QLCDNumber.Filled)
        self.lcd_solenoid_field.setProperty("value", 0.0)
        self.lcd_solenoid_field.setProperty("intValue", 0)
        self.lcd_solenoid_field.setObjectName("lcd_solenoid_field")
        self.label_5 = QtWidgets.QLabel(self.solenoid)
        self.label_5.setGeometry(QtCore.QRect(320, 90, 41, 51))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiLight")
        font.setPointSize(18)
        self.label_5.setFont(font)
        self.label_5.setAutoFillBackground(False)
        self.label_5.setObjectName("label_5")
        self.dipole = QtWidgets.QFrame(self.widget)
        self.dipole.setGeometry(QtCore.QRect(380, 10, 391, 521))
        self.dipole.setAutoFillBackground(False)
        self.dipole.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(160, 160, 160, 255), stop:0.842105 rgba(255, 255, 255, 255));")
        self.dipole.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.dipole.setFrameShadow(QtWidgets.QFrame.Raised)
        self.dipole.setObjectName("dipole")
        self.dipole_title = QtWidgets.QLabel(self.dipole)
        self.dipole_title.setGeometry(QtCore.QRect(20, 20, 361, 61))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.dipole_title.setFont(font)
        self.dipole_title.setStyleSheet("background-color: rgb(185, 185, 185);")
        self.dipole_title.setIndent(30)
        self.dipole_title.setOpenExternalLinks(False)
        self.dipole_title.setObjectName("dipole_title")
        self.lcd_dipole = QtWidgets.QLCDNumber(self.dipole)
        self.lcd_dipole.setGeometry(QtCore.QRect(20, 90, 151, 81))
        self.lcd_dipole.setAutoFillBackground(False)
        self.lcd_dipole.setStyleSheet("color: rgb(18, 223, 14);\n"
                                      "background-color: rgb(0, 0, 0);")
        self.lcd_dipole.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lcd_dipole.setFrameShadow(QtWidgets.QFrame.Plain)
        self.lcd_dipole.setSmallDecimalPoint(False)
        self.lcd_dipole.setDigitCount(4)
        self.lcd_dipole.setMode(QtWidgets.QLCDNumber.Dec)
        self.lcd_dipole.setSegmentStyle(QtWidgets.QLCDNumber.Filled)
        self.lcd_dipole.setProperty("value", 0.0)
        self.lcd_dipole.setProperty("intValue", 0)
        self.lcd_dipole.setObjectName("lcd_dipole")
        self.value_dipole = QtWidgets.QDoubleSpinBox(self.dipole)
        self.value_dipole.setGeometry(QtCore.QRect(20, 210, 151, 51))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.value_dipole.setFont(font)
        self.value_dipole.setMouseTracking(False)
        self.value_dipole.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.value_dipole.setAcceptDrops(False)
        self.value_dipole.setAutoFillBackground(True)
        self.value_dipole.setWrapping(False)
        self.value_dipole.setFrame(True)
        self.value_dipole.setAccelerated(False)
        self.value_dipole.setProperty("showGroupSeparator", False)
        self.value_dipole.setDecimals(2)
        self.value_dipole.setMaximum(max_dip)  # dip_max, min
        self.value_dipole.setMinimum(min_dip)
        self.value_dipole.setSingleStep(0.01)
        self.value_dipole.setObjectName("value_dipole")
        self.set_dipole = QtWidgets.QCommandLinkButton(self.dipole)
        self.set_dipole.setGeometry(QtCore.QRect(20, 310, 101, 48))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.set_dipole.setFont(font)
        self.set_dipole.setAutoFillBackground(False)
        self.set_dipole.setStyleSheet("background-color: rgb(0, 255, 0);\n"
                                      "")
        self.set_dipole.setCheckable(True)
        self.set_dipole.setAutoDefault(False)
        self.set_dipole.setDefault(True)
        self.set_dipole.setObjectName("set_dipole")
        self.degauss_dipole = QtWidgets.QCommandLinkButton(self.dipole)
        self.degauss_dipole.setGeometry(QtCore.QRect(20, 450, 261, 51))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.degauss_dipole.setFont(font)
        self.degauss_dipole.setAutoFillBackground(False)
        self.degauss_dipole.setStyleSheet("background-color: rgb(0, 0, 255);")
        self.degauss_dipole.setCheckable(True)
        self.degauss_dipole.setAutoDefault(False)
        self.degauss_dipole.setDefault(True)
        self.degauss_dipole.setObjectName("degauss_dipole")
        self.progress_dipole = QtWidgets.QProgressBar(self.dipole)
        self.progress_dipole.setGeometry(QtCore.QRect(20, 400, 301, 21))
        self.progress_dipole.setProperty("value", 0)
        self.progress_dipole.setObjectName("progress_dipole")
        self.label_3 = QtWidgets.QLabel(self.dipole)
        self.label_3.setGeometry(QtCore.QRect(170, 90, 31, 81))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiLight")
        font.setPointSize(24)
        self.label_3.setFont(font)
        self.label_3.setAutoFillBackground(False)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.dipole)
        self.label_4.setGeometry(QtCore.QRect(170, 210, 31, 51))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiLight")
        font.setPointSize(16)
        self.label_4.setFont(font)
        self.label_4.setAutoFillBackground(False)
        self.label_4.setObjectName("label_4")
        self.lcd_dipole_field = QtWidgets.QLCDNumber(self.dipole)
        self.lcd_dipole_field.setGeometry(QtCore.QRect(220, 90, 101, 51))
        self.lcd_dipole_field.setAutoFillBackground(False)
        self.lcd_dipole_field.setStyleSheet("color: rgb(18, 223, 14);\n"
                                            "background-color: rgb(0, 0, 0);")
        self.lcd_dipole_field.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lcd_dipole_field.setFrameShadow(QtWidgets.QFrame.Plain)
        self.lcd_dipole_field.setSmallDecimalPoint(False)
        self.lcd_dipole_field.setDigitCount(4)
        self.lcd_dipole_field.setMode(QtWidgets.QLCDNumber.Dec)
        self.lcd_dipole_field.setSegmentStyle(QtWidgets.QLCDNumber.Filled)
        self.lcd_dipole_field.setProperty("value", 0.0)
        self.lcd_dipole_field.setProperty("intValue", 0)
        self.lcd_dipole_field.setObjectName("lcd_dipole_field")
        self.lcd_beam_energy = QtWidgets.QLCDNumber(self.dipole)
        self.lcd_beam_energy.setGeometry(QtCore.QRect(220, 150, 101, 51))
        self.lcd_beam_energy.setAutoFillBackground(False)
        self.lcd_beam_energy.setStyleSheet("color: rgb(18, 223, 14);\n"
                                           "background-color: rgb(0, 0, 0);")
        self.lcd_beam_energy.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lcd_beam_energy.setFrameShadow(QtWidgets.QFrame.Plain)
        self.lcd_beam_energy.setSmallDecimalPoint(False)
        self.lcd_beam_energy.setDigitCount(4)
        self.lcd_beam_energy.setMode(QtWidgets.QLCDNumber.Dec)
        self.lcd_beam_energy.setSegmentStyle(QtWidgets.QLCDNumber.Filled)
        self.lcd_beam_energy.setProperty("value", 0.0)
        self.lcd_beam_energy.setProperty("intValue", 0)
        self.lcd_beam_energy.setObjectName("lcd_beam_energy")
        self.label_6 = QtWidgets.QLabel(self.dipole)
        self.label_6.setGeometry(QtCore.QRect(320, 90, 61, 51))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiLight")
        font.setPointSize(18)
        self.label_6.setFont(font)
        self.label_6.setAutoFillBackground(False)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.dipole)
        self.label_7.setGeometry(QtCore.QRect(320, 150, 61, 51))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiLight")
        font.setPointSize(18)
        self.label_7.setFont(font)
        self.label_7.setAutoFillBackground(False)
        self.label_7.setObjectName("label_7")
        self.connect_button = QtWidgets.QPushButton(self.widget)
        self.connect_button.setGeometry(QtCore.QRect(780, 30, 161, 71))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.connect_button.setFont(font)
        self.connect_button.setStyleSheet("background-color: rgb(141, 141, 141);")
        self.connect_button.setCheckable(True)
        self.connect_button.setObjectName("connect_button")
        self.disconnect_button = QtWidgets.QPushButton(self.widget)
        self.disconnect_button.setGeometry(QtCore.QRect(780, 120, 161, 71))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.disconnect_button.setFont(font)
        self.disconnect_button.setStyleSheet("background-color: rgb(141, 141, 141);")
        self.disconnect_button.setCheckable(True)
        self.disconnect_button.setObjectName("disconnect_button")
        self.status = QtWidgets.QLabel(self.widget)
        self.status.setGeometry(QtCore.QRect(780, 210, 161, 51))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.status.setFont(font)
        self.status.setStyleSheet("background-color: rgb(0, 0, 0);\n"
                                  "color: rgb(0, 255, 0);")
        self.status.setObjectName("status")
        window.setCentralWidget(self.widget)
        self.menubar = QtWidgets.QMenuBar(window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 956, 26))
        self.menubar.setObjectName("menubar")
        window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(window)
        self.statusbar.setObjectName("statusbar")
        window.setStatusBar(self.statusbar)

        self.retranslateUi(window)
        QtCore.QMetaObject.connectSlotsByName(window)
        self.disconnect_button.setDisabled(True)
        self.set_solenoid.setDisabled(True)
        self.set_dipole.setDisabled(True)
        self.degauss_dipole.setDisabled(True)
        self.connect_button.isDown()

        self.timer = QTimer()
        self.timer.timeout.connect(lambda: self.daq_get_sol(0))
        self.timer.timeout.connect(lambda: self.daq_get_dip(1))
        # self.timer.start(500)
        self.add_functions()

    def retranslateUi(self, window):
        _translate = QtCore.QCoreApplication.translate
        window.setWindowTitle(_translate("window", "MainWindow"))
        self.solenoid_title.setText(_translate("window", "Solenoid"))
        self.set_solenoid.setText(_translate("window", "Set"))
        self.label.setText(_translate("window", "A"))
        self.label_2.setText(_translate("window", "A"))
        self.label_5.setText(_translate("window", "mT"))
        self.dipole_title.setText(_translate("window", "Dipole"))
        self.set_dipole.setText(_translate("window", "Set"))
        self.degauss_dipole.setText(_translate("window", "DeGauss Procedure"))
        self.label_3.setText(_translate("window", "A"))
        self.label_4.setText(_translate("window", "A"))
        self.label_6.setText(_translate("window", "mT"))
        self.label_7.setText(_translate("window", "MeV"))
        self.connect_button.setText(_translate("window", "Connect"))
        self.disconnect_button.setText(_translate("window", "Disconnect"))
        self.status.setText(_translate("window", "Disconnected"))

    def add_functions(self):
        self.connect_button.clicked.connect(lambda: self.on_click_connect())
        self.disconnect_button.clicked.connect(lambda: self.on_click_disconnect())
        self.set_solenoid.clicked.connect(lambda: self.sol_value_set())
        self.set_dipole.clicked.connect(lambda: self.dip_value_set())
        self.degauss_dipole.clicked.connect(lambda: self.deGauss())

    def daq_get_sol(self, get_channel):
        if self.daq_valid():
            t = f'{get_channel}task'
            t = nidaqmx.Task()
            t.ai_channels.add_ai_voltage_chan(physical_channel=f'Dev1/ai{get_channel}')
            t.start()
            value = t.read()
            t.stop()
            t.close()
            # print(value)
            self.lcd_solenoid.display(value * gorcakic_solenoid)

    def daq_set_sol(self, get_channel):
        if self.daq_valid():
            k = f'{get_channel}tasks'
            k = nidaqmx.Task()
            k.ao_channels.add_ao_voltage_chan(physical_channel=f'Dev1/ao{get_channel}', min_val=0,
                                              max_val=max_sol / gorcakic_solenoid)
            k.start()
            # print(self.value_solenoid.text())
            k.write(sol_value / gorcakic_solenoid, auto_start=False)
            k.stop()
            k.close()

    def sol_value_set(self):
        global sol_value
        self.set_solenoid.setDisabled(True)
        self.set_dipole.setDisabled(True)
        self.degauss_dipole.setDisabled(True)
        self.disconnect_button.setDisabled(True)
        # if eval(self.value_solenoid.text()) > sol_value:
        while sol_value <= eval(self.value_solenoid.text()):
            sol_value += 0.01
            sleep(0.01)
            self.daq_set_sol(0)
        sol_value = eval(self.value_solenoid.text())
        self.daq_set_sol(0)
        self.set_solenoid.setDisabled(False)
        self.set_dipole.setDisabled(False)
        self.degauss_dipole.setDisabled(False)
        self.disconnect_button.setDisabled(False)
        self.lcd_solenoid_field.display(self.solenoid_field())

    def daq_get_dip(self, get_channel):
        if self.daq_valid():
            t = f'{get_channel}task'
            t = nidaqmx.Task()
            t.ai_channels.add_ai_voltage_chan(physical_channel=f'Dev1/ai{get_channel}')
            t.start()
            value = t.read()
            t.stop()
            t.close()
            # print(value)
            self.lcd_dipole.display(value * gorcakic_dipole)

    def daq_set_dip(self, get_channel):
        if self.daq_valid():
            k = f'{get_channel}tasks'
            k = nidaqmx.Task()
            k.ao_channels.add_ao_voltage_chan(physical_channel=f'Dev1/ao{get_channel}', min_val=0,
                                              max_val=max_dip / gorcakic_dipole)
            k.start()
            # print(self.value_dipole.text())
            k.write(dip_value / gorcakic_dipole, auto_start=False)
            k.stop()
            k.close()

    def dip_value_set(self):
        global dip_value
        self.set_dipole.setDisabled(True)
        self.degauss_dipole.setDisabled(True)
        self.set_solenoid.setDisabled(True)
        self.disconnect_button.setDisabled(True)
        # if eval(self.value_dipole.text()) > dip_value:
        while dip_value <= eval(self.value_dipole.text()):
            dip_value += 0.01
            sleep(0.01)
            self.daq_set_dip(1)
        dip_value = eval(self.value_dipole.text())
        self.daq_set_dip(1)
        if dip_value == 0:
            self.lcd_dipole.display('0')
        self.set_dipole.setDisabled(False)
        self.degauss_dipole.setDisabled(False)
        self.set_solenoid.setDisabled(False)
        self.disconnect_button.setDisabled(False)
        self.lcd_dipole_field.display(self.dipole_field())
        self.lcd_beam_energy.display(self.beam_energy())

    def deGauss(self):
        global dip_value
        self.set_dipole.setDisabled(True)
        self.degauss_dipole.setDisabled(True)
        self.set_solenoid.setDisabled(True)
        self.disconnect_button.setDisabled(True)
        i = 0
        while i < degauss_time:
            self.progress_dipole.setProperty("value", ((i / degauss_time) * 100))
            dip_value = ((e ** (-i)) * sin(degauss_freq * i)) * (max_dip / gorcakic_dipole)
            self.daq_set_dip(1)
            i += 0.01
            sleep(0.1)
        dip_value = 0
        self.daq_set_dip(1)
        if dip_value == 0:
            self.lcd_dipole_field.display('0')
            self.lcd_dipole.display('0')
        self.set_dipole.setDisabled(False)
        self.degauss_dipole.setDisabled(False)
        self.set_solenoid.setDisabled(False)
        self.disconnect_button.setDisabled(False)

    def solenoid_field(self):
        if float(self.value_solenoid.text()) == 0:
            return 0
        else:
            return float(self.value_solenoid.text()) * 22.2 + 1.2

    def dipole_field(self):
        if float(self.value_dipole.text()) == 0:
            return 0
        else:
            return dipfield.dip_field(float(self.value_dipole.text()))


    def beam_energy(self):
        return beamenergy.beam_energy(float(self.value_dipole.text()))

    def on_click_connect(self):
        if self.daq_valid():
            self.timer.start(500)
            self.status.setText('Connected')
            self.set_solenoid.setDisabled(False)
            self.set_dipole.setDisabled(False)
            self.connect_button.setDisabled(True)
            self.disconnect_button.setDisabled(False)
            self.degauss_dipole.setDisabled(False)

        else:
            self.connect_button.setDisabled(False)
            self.disconnect_button.setDisabled(True)

    def on_click_disconnect(self):
        global sol_value
        global dip_value
        sol_value = 0
        dip_value = 0
        self.timer.stop()
        self.daq_disconnect()
        self.lcd_solenoid.display('0')
        self.lcd_dipole.display('0')
        self.lcd_solenoid_field.display('0')
        self.lcd_dipole_field.display('0')
        self.lcd_beam_energy.display('0')
        self.status.setText('Disconnected')
        self.connect_button.setDisabled(False)
        self.disconnect_button.setDisabled(True)
        self.set_solenoid.setDisabled(True)
        self.set_dipole.setDisabled(True)
        self.degauss_dipole.setDisabled(True)

    def daq_valid(self):
        try:
            task1 = nidaqmx.Task()
            task1.ao_channels.add_ao_voltage_chan(physical_channel='Dev1/ao0:1')
            task1.start()
            task1.stop()
            task1.close()
            return True
        except Exception:
            self.status.setText('Daq_er')
            self.lcd_solenoid.display('0')
            self.lcd_dipole.display('0')
            self.lcd_solenoid_field.display('0')
            self.lcd_dipole_field.display('0')
            self.lcd_beam_energy.display('0')
            self.connect_button.setDisabled(False)
            self.disconnect_button.setDisabled(True)
            self.set_solenoid.setDisabled(True)
            self.set_dipole.setDisabled(True)
            self.timer.stop()
            return False

    def daq_disconnect(self):
        if self.daq_valid():
            task = nidaqmx.Task()
            task.ao_channels.add_ao_voltage_chan(physical_channel='Dev1/ao0:1')
            task.start()
            task.write([[0], [0]], auto_start=False)
            task.stop()
            task.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = WinForm()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec_())
