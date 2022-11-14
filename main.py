import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QColorDialog
from pathlib import Path

CONFIG_DIRECTORY = str(Path.home()) + "/.config/predator/saved profiles"
path = Path(CONFIG_DIRECTORY)
path.mkdir(parents=True, exist_ok=True)


class Ui_MainWindow(QtWidgets.QWidget):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        cmd = ""
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(100, 0, 601, 61))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.StaticRadioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.StaticRadioButton.setGeometry(QtCore.QRect(30, 80, 106, 23))
        self.StaticRadioButton.setObjectName("StaticRadioButton")
        self.DynamicRadioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.DynamicRadioButton.setGeometry(QtCore.QRect(30, 290, 106, 23))
        self.DynamicRadioButton.setObjectName("DynamicRadioButton")
        self.Zone1Checkbox = QtWidgets.QCheckBox(self.centralwidget)
        self.Zone1Checkbox.setGeometry(QtCore.QRect(100, 160, 90, 23))
        self.Zone1Checkbox.setObjectName("Zone1Checkbox")
        self.BrightSlider = QtWidgets.QSlider(self.centralwidget)
        self.BrightSlider.setGeometry(QtCore.QRect(590, 80, 160, 16))
        self.BrightSlider.setOrientation(QtCore.Qt.Horizontal)
        self.BrightSlider.setObjectName("BrightSlider")
        self.UselessLabel = QtWidgets.QLabel(self.centralwidget)
        self.UselessLabel.setGeometry(QtCore.QRect(510, 80, 81, 16))
        self.UselessLabel.setObjectName("UselessLabel")
        self.Zone2Checkbox = QtWidgets.QCheckBox(self.centralwidget)
        self.Zone2Checkbox.setGeometry(QtCore.QRect(260, 160, 90, 23))
        self.Zone2Checkbox.setObjectName("Zone2Checkbox")
        self.Zone3Checkbox = QtWidgets.QCheckBox(self.centralwidget)
        self.Zone3Checkbox.setGeometry(QtCore.QRect(420, 160, 90, 23))
        self.Zone3Checkbox.setObjectName("Zone3Checkbox")
        self.Zone4Checkbox = QtWidgets.QCheckBox(self.centralwidget)
        self.Zone4Checkbox.setGeometry(QtCore.QRect(600, 160, 90, 23))
        self.Zone4Checkbox.setObjectName("Zone4Checkbox")
        self.Color1RGB = QtWidgets.QLabel(self.centralwidget)
        self.Color1RGB.setGeometry(QtCore.QRect(110, 220, 120, 17))
        self.Color1RGB.setObjectName("Color1RGB")
        self.Color2RGB = QtWidgets.QLabel(self.centralwidget)
        self.Color2RGB.setGeometry(QtCore.QRect(270, 220, 120, 17))
        self.Color2RGB.setObjectName("Color2RGB")
        self.Color3RGB = QtWidgets.QLabel(self.centralwidget)
        self.Color3RGB.setGeometry(QtCore.QRect(430, 220, 120, 17))
        self.Color3RGB.setObjectName("Color3RGB")
        self.Color4RGB = QtWidgets.QLabel(self.centralwidget)
        self.Color4RGB.setGeometry(QtCore.QRect(610, 220, 120, 17))
        self.Color4RGB.setObjectName("Color4RGB")
        self.UselessLabel2 = QtWidgets.QLabel(self.centralwidget)
        self.UselessLabel2.setGeometry(QtCore.QRect(70, 330, 91, 17))
        self.UselessLabel2.setObjectName("UselessLabel2")
        self.UselessLabel_2 = QtWidgets.QLabel(self.centralwidget)
        self.UselessLabel_2.setGeometry(QtCore.QRect(70, 450, 62, 17))
        self.UselessLabel_2.setObjectName("UselessLabel_2")
        self.BreathingCheckbox = QtWidgets.QCheckBox(self.centralwidget, )
        self.BreathingCheckbox.setGeometry(QtCore.QRect(100, 370, 91, 23))
        self.BreathingCheckbox.setObjectName("BreathingCheckbox")
        self.ShiftingCheckbox = QtWidgets.QCheckBox(self.centralwidget)
        self.ShiftingCheckbox.setGeometry(QtCore.QRect(250, 370, 81, 23))
        self.ShiftingCheckbox.setObjectName("ShiftingCheckbox")
        self.WaveCheckbox = QtWidgets.QCheckBox(self.centralwidget)
        self.WaveCheckbox.setGeometry(QtCore.QRect(370, 370, 61, 23))
        self.WaveCheckbox.setObjectName("WaveCheckbox")
        self.NeonCheckbox = QtWidgets.QCheckBox(self.centralwidget)
        self.NeonCheckbox.setGeometry(QtCore.QRect(480, 370, 61, 23))
        self.NeonCheckbox.setObjectName("NeonCheckbox")
        self.ZoomCheckbox = QtWidgets.QCheckBox(self.centralwidget)
        self.ZoomCheckbox.setGeometry(QtCore.QRect(600, 370, 61, 23))
        self.ZoomCheckbox.setObjectName("ZoomCheckbox")
        self.SpeedSlider = QtWidgets.QSlider(self.centralwidget)
        self.SpeedSlider.setGeometry(QtCore.QRect(100, 490, 160, 16))
        self.SpeedSlider.setOrientation(QtCore.Qt.Horizontal)
        self.SpeedSlider.setObjectName("SpeedSlider")
        self.UselessLabel_3 = QtWidgets.QLabel(self.centralwidget)
        self.UselessLabel_3.setGeometry(QtCore.QRect(410, 450, 71, 17))
        self.UselessLabel_3.setObjectName("UselessLabel_3")
        self.DirectLeftButton = QtWidgets.QPushButton(self.centralwidget)
        self.DirectLeftButton.setGeometry(QtCore.QRect(400, 480, 31, 25))
        self.DirectLeftButton.setObjectName("DirectLeftButton")
        self.DirectRightButton = QtWidgets.QPushButton(self.centralwidget)
        self.DirectRightButton.setGeometry(QtCore.QRect(450, 480, 31, 25))
        self.DirectRightButton.setObjectName("DirectRightButton")
        self.LoadButton = QtWidgets.QPushButton(self.centralwidget)
        self.LoadButton.setGeometry(QtCore.QRect(580, 540, 83, 25))
        self.LoadButton.setObjectName("LoadButton")
        self.SaveButton = QtWidgets.QPushButton(self.centralwidget)
        self.SaveButton.setGeometry(QtCore.QRect(700, 540, 83, 25))
        self.SaveButton.setObjectName("SaveButton")

        self.BreathingCheckbox.setEnabled(False)
        self.ShiftingCheckbox.setEnabled(False)
        self.WaveCheckbox.setEnabled(False)
        self.NeonCheckbox.setEnabled(False)
        self.ZoomCheckbox.setEnabled(False)
        self.SpeedSlider.setEnabled(False)
        self.DirectRightButton.setEnabled(False)
        self.DirectLeftButton.setEnabled(False)
        self.Zone1Checkbox.setEnabled(False)
        self.Zone2Checkbox.setEnabled(False)
        self.Zone3Checkbox.setEnabled(False)
        self.Zone4Checkbox.setEnabled(False)

        self.SpeedSlider.setMinimum(1)
        self.SpeedSlider.setMaximum(9)
        self.SpeedSlider.setValue(3)

        self.BrightSlider.setMinimum(0)
        self.BrightSlider.setMaximum(100)
        self.BrightSlider.setValue(100)

        self.StaticRadioButton.clicked.connect(lambda: self.checkRadioButton())
        self.DynamicRadioButton.clicked.connect(lambda: self.checkRadioButton())

        self.Zone1Checkbox.stateChanged.connect(lambda: self.staticZoneColorPick(self.Zone1Checkbox.isChecked(), 0))
        self.Zone2Checkbox.stateChanged.connect(lambda: self.staticZoneColorPick(self.Zone2Checkbox.isChecked(), 1))
        self.Zone3Checkbox.stateChanged.connect(lambda: self.staticZoneColorPick(self.Zone3Checkbox.isChecked(), 2))
        self.Zone4Checkbox.stateChanged.connect(lambda: self.staticZoneColorPick(self.Zone4Checkbox.isChecked(), 3))

        self.BreathingCheckbox.stateChanged.connect(lambda: self.dynamicSelector(self.BreathingCheckbox.isChecked(), 0))
        self.ShiftingCheckbox.stateChanged.connect(lambda: self.dynamicSelector(self.ShiftingCheckbox.isChecked(), 1))
        self.WaveCheckbox.stateChanged.connect(lambda: self.dynamicSelector(self.WaveCheckbox.isChecked(), 2))
        self.NeonCheckbox.stateChanged.connect(lambda: self.dynamicSelector(self.NeonCheckbox.isChecked(), 3))
        self.ZoomCheckbox.stateChanged.connect(lambda: self.dynamicSelector(self.ZoomCheckbox.isChecked(), 4))

        self.LoadButton.clicked.connect(lambda: self.load())

        self.BrightSlider.valueChanged.connect(self.sliderChanged)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def sliderChanged(self):
        bright = int(self.BrightSlider.value())
        os.system(f"sudo ./facer_rgb.py -b {bright}")

    def checkRadioButton(self):
        if self.StaticRadioButton.isChecked():
            # enable static objects
            self.Zone1Checkbox.setEnabled(True)
            self.Zone2Checkbox.setEnabled(True)
            self.Zone3Checkbox.setEnabled(True)
            self.Zone4Checkbox.setEnabled(True)

            # disable dynamic objects
            self.BreathingCheckbox.setEnabled(False)
            self.ShiftingCheckbox.setEnabled(False)
            self.WaveCheckbox.setEnabled(False)
            self.NeonCheckbox.setEnabled(False)
            self.ZoomCheckbox.setEnabled(False)
            self.SpeedSlider.setEnabled(False)
            self.DirectRightButton.setEnabled(False)
            self.DirectLeftButton.setEnabled(False)

        elif self.DynamicRadioButton.isChecked():
            # disable static objects
            self.Zone1Checkbox.setEnabled(False)
            self.Zone2Checkbox.setEnabled(False)
            self.Zone3Checkbox.setEnabled(False)
            self.Zone4Checkbox.setEnabled(False)

            # enable dynamic objects
            self.BreathingCheckbox.setEnabled(True)
            self.ShiftingCheckbox.setEnabled(True)
            self.WaveCheckbox.setEnabled(True)
            self.NeonCheckbox.setEnabled(True)
            self.ZoomCheckbox.setEnabled(True)
            self.SpeedSlider.setEnabled(True)
            self.DirectRightButton.setEnabled(True)
            self.DirectLeftButton.setEnabled(True)

    def staticZoneColorPick(self, checkbox, i):
        if checkbox:
            color = QColorDialog.getColor()
            if i == 0:
                red = color.red()
                green = color.green()
                blue = color.blue()
                self.Color1RGB.setText(str(red) + ", " + str(green) + ", " + str(blue))
                os.system(f"sudo ./facer_rgb.py -m 0 -z 1 -cR {red} -cB {blue} -cG {green} -b 100")
                cmd = f"sudo ./facer_rgb.py -m 0 -z 1 -cR {red} -cB {blue} -cG {green}"
                self.SaveButton.clicked.connect(lambda: self.save(cmd))
            elif i == 1:
                red = color.red()
                green = color.green()
                blue = color.blue()
                self.Color2RGB.setText(str(red) + ", " + str(green) + ", " + str(blue))
                os.system(f"sudo ./facer_rgb.py -m 0 -z 2 -cR {red} -cB {blue} -cG {green}")
                cmd = f"sudo ./facer_rgb.py -m 0 -z 2 -cR {red} -cB {blue} -cG {green}"
                self.SaveButton.clicked.connect(lambda: self.save(cmd))
            elif i == 2:
                red = color.red()
                green = color.green()
                blue = color.blue()
                self.Color3RGB.setText(str(red) + ", " + str(green) + ", " + str(blue))
                os.system(f"sudo ./facer_rgb.py -m 0 -z 3 -cR {red} -cB {blue} -cG {green}")
                cmd = f"sudo ./facer_rgb.py -m 0 -z 3 -cR {red} -cB {blue} -cG {green}"
                self.SaveButton.clicked.connect(lambda: self.save(cmd))
            elif i == 3:
                red = color.red()
                green = color.green()
                blue = color.blue()
                self.Color4RGB.setText(str(red) + ", " + str(green) + ", " + str(blue))
                os.system(f"sudo ./facer_rgb.py -m 0 -z 4 -cR {red} -cB {blue} -cG {green}")
                cmd = f"sudo ./facer_rgb.py -m 0 -z 4 -cR {red} -cB {blue} -cG {green}"
                self.SaveButton.clicked.connect(lambda: self.save(cmd))

    def dynamicSelector(self, checkbox, i):
        if checkbox:
            speed = int(self.SpeedSlider.value())
            if i == 0:
                # Breathing
                self.BreathingCheckbox.setEnabled(True)
                self.ShiftingCheckbox.setEnabled(False)
                self.WaveCheckbox.setEnabled(False)
                self.NeonCheckbox.setEnabled(False)
                self.ZoomCheckbox.setEnabled(False)
                color = QColorDialog.getColor()
                red = color.red()
                green = color.green()
                blue = color.blue()
                os.system(f"sudo ./facer_rgb.py -m 1 -s {speed} -cR {red} -cG {green} -cB {blue}")
                cmd = f"sudo ./facer_rgb.py -m 1 -s {speed} -cR {red} -cG {green} -cB {blue}"
                self.SaveButton.clicked.connect(lambda: self.save(cmd))
            elif i == 1:
                # Shifting
                self.BreathingCheckbox.setEnabled(False)
                self.ShiftingCheckbox.setEnabled(True)
                self.WaveCheckbox.setEnabled(False)
                self.NeonCheckbox.setEnabled(False)
                self.ZoomCheckbox.setEnabled(False)
                os.system(f"sudo ./facer_rgb.py -m 2 -s {speed}")
                cmd = f"sudo ./facer_rgb.py -m 2 -s {speed}"
                self.SaveButton.clicked.connect(lambda: self.save(cmd))
            elif i == 2:
                # Wave
                self.BreathingCheckbox.setEnabled(False)
                self.ShiftingCheckbox.setEnabled(False)
                self.WaveCheckbox.setEnabled(True)
                self.NeonCheckbox.setEnabled(False)
                self.ZoomCheckbox.setEnabled(False)
                os.system(f"sudo ./facer_rgb.py -m 3 -s {speed}")
                cmd = f"sudo ./facer_rgb.py -m 3 -s {speed}"
                self.SaveButton.clicked.connect(lambda: self.save(cmd))
                self.DirectLeftButton.clicked.connect((lambda: self.setDirectLeft(3, speed, 0, 0, 0)))
                self.DirectRightButton.clicked.connect((lambda: self.setDirectRight(3, speed, 0, 0, 0)))
            elif i == 3:
                # Neon
                self.BreathingCheckbox.setEnabled(False)
                self.ShiftingCheckbox.setEnabled(False)
                self.WaveCheckbox.setEnabled(False)
                self.NeonCheckbox.setEnabled(True)
                self.ZoomCheckbox.setEnabled(False)
                color = QColorDialog.getColor()
                red = color.red()
                green = color.green()
                blue = color.blue()
                os.system(f"sudo ./facer_rgb.py -m 4 -s {speed} -cR {red} -cB {blue} -cG {green}")
                cmd = f"sudo ./facer_rgb.py -m 3 -s {speed}"
                self.SaveButton.clicked.connect(lambda: self.save(cmd))
                self.DirectLeftButton.clicked.connect((lambda: self.setDirectLeft(4, speed, red, blue, green)))
                self.DirectRightButton.clicked.connect((lambda: self.setDirectRight(4, speed, red, blue, green)))
            elif i == 4:
                # Zoom
                self.BreathingCheckbox.setEnabled(False)
                self.ShiftingCheckbox.setEnabled(False)
                self.WaveCheckbox.setEnabled(False)
                self.NeonCheckbox.setEnabled(False)
                self.ZoomCheckbox.setEnabled(True)
                color = QColorDialog.getColor()
                red = color.red()
                green = color.green()
                blue = color.blue()
                os.system(f"sudo ./facer_rgb.py -m 5 -s {speed} -cR {red} -cB {blue} -cG {green}")
                cmd = f"sudo ./facer_rgb.py -m 5 -s {speed} -cR {red} -cB {blue} -cG {green}"
                self.SaveButton.clicked.connect(lambda: self.save(cmd))
        elif not checkbox:
            self.BreathingCheckbox.setEnabled(True)
            self.ShiftingCheckbox.setEnabled(True)
            self.WaveCheckbox.setEnabled(True)
            self.NeonCheckbox.setEnabled(True)
            self.ZoomCheckbox.setEnabled(True)

    def setDirectLeft(self, mode, speed, r, g, b):
        d = 1  # Right to the left
        os.system(f"sudo ./facer_rgb.py -d {d} -m {mode} -s {speed} -cR {r} -cB {b} -cG {g}")

    def setDirectRight(self, mode, speed, r, g, b):
        d = 0  # Left to the right
        os.system(f"sudo ./facer_rgb.py -d {d} -m {mode} -s {speed} -cR {r} -cB {b} -cG {g}")

    def save(self, command):
        name, done = QtWidgets.QInputDialog.getText(
            self, 'Save', 'Enter name for your config:')

        if done:
            cmd = command + " " + f"-save {name}"
            os.system(cmd)

    def load(self):
        global filepath
        cfg = []
        for filepath in list(path.glob('*.*')):
            f"\t{filepath.resolve().stem}"
            cfg.append(filepath.stem)

        config, done = QtWidgets.QInputDialog.getItem(
            self, 'Load', 'Select your config:', cfg)

        if done:
            os.system(f"sudo ./facer_rgb.py -load {str(config)}")

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Acer Keyboard Light AKL"))
        self.label.setText(_translate("MainWindow", "Acer Nitro-Predator Keyboard Light"))
        self.StaticRadioButton.setText(_translate("MainWindow", "Static"))
        self.DynamicRadioButton.setText(_translate("MainWindow", "Dynamic"))
        self.Zone1Checkbox.setText(_translate("MainWindow", "Zone 1"))
        self.UselessLabel.setText(_translate("MainWindow", "Brightness"))
        self.Zone2Checkbox.setText(_translate("MainWindow", "Zone 2"))
        self.Zone3Checkbox.setText(_translate("MainWindow", "Zone 3"))
        self.Zone4Checkbox.setText(_translate("MainWindow", "Zone 4"))
        self.Color1RGB.setText(_translate("MainWindow", "Color"))
        self.Color2RGB.setText(_translate("MainWindow", "Color"))
        self.Color3RGB.setText(_translate("MainWindow", "Color"))
        self.Color4RGB.setText(_translate("MainWindow", "Color"))
        self.UselessLabel2.setText(_translate("MainWindow", "Light Effect"))
        self.UselessLabel_2.setText(_translate("MainWindow", "Speed"))
        self.BreathingCheckbox.setText(_translate("MainWindow", "Breathing"))
        self.ShiftingCheckbox.setText(_translate("MainWindow", "Shifting"))
        self.WaveCheckbox.setText(_translate("MainWindow", "Wave"))
        self.NeonCheckbox.setText(_translate("MainWindow", "Neon"))
        self.ZoomCheckbox.setText(_translate("MainWindow", "Zoom"))
        self.UselessLabel_3.setText(_translate("MainWindow", "Direction"))
        self.DirectLeftButton.setText(_translate("MainWindow", "<"))
        self.DirectRightButton.setText(_translate("MainWindow", ">"))
        self.LoadButton.setText(_translate("MainWindow", "Load"))
        self.SaveButton.setText(_translate("MainWindow", "Save"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()

    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
