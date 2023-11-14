import sys
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QFont # Added import
from PyQt5.QtWidgets import (QApplication, QGridLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget)
import math
import win32gui, win32con
the_program_to_hide = win32gui.GetForegroundWindow()
win32gui.ShowWindow(the_program_to_hide , win32con.SW_HIDE)
class CylinderFillVolume(QWidget):
    def __init__(self):
        super().__init__()

        # Create widgets
        self.fill_height_label = QLabel("Fill Height of Dip (cm)")
        self.fill_height_entry = QLineEdit()
        self.fill_height_entry.setFixedWidth(200) # set width to 200 pixels
        self.fill_height_entry.setFont(QFont("Arial", 18)) # set font to Arial, size 18
        self.calculate_button = QPushButton("Calculate")
        self.result_label = QLabel("")

        # Increase font size of labels
        self.fill_height_label.setFont(QFont("Arial", 14))
        self.result_label.setFont(QFont("Arial", 14))

        # Increase font size of buttons
        self.calculate_button.setFont(QFont("Arial", 14))

        # Create layout
        layout = QGridLayout()
        layout.addWidget(self.fill_height_label, 0, 0)
        layout.addWidget(self.fill_height_entry, 0, 1)
        layout.addWidget(self.calculate_button, 1, 1)
        layout.addWidget(self.result_label, 2, 0)

        # Set layout
        self.setLayout(layout)
        self.setWindowTitle("Fuel Tank Filled Volume Calculator")
        self.setGeometry(100, 100, 400, 100) # Added window size

        # Change the color of the button
        self.calculate_button.setStyleSheet("background-color: lightblue") # change to desired color

        # Connect signals and slots
        self.calculate_button.clicked.connect(self.calculate)

    def horizontal_cylinder_volume(self, V):
        d = 259.080 # diameter in cm
        l = 365.758 # length in cm
        r = d/2
        cylinder_volume = math.pi * (r ** 2) * l
        return cylinder_volume

    @pyqtSlot()
    def calculate(self):
        fill_height = float(self.fill_height_entry.text())
        result = self.cylinder_fill_volume(fill_height)
        result = result/1000  # converting cm^3 to liters
        self.result_label.setText(f"Filled Volume: {result:.2f} liters")

    def cylinder_fill_volume(self, f):
        d = 259.080 # diameter in cm
        l = 365.758 # length in cm
        r = d/2
        m = (d/2) - f
        if f > (d/2):
            theta = 2 * math.acos(m/r)
            segment_area = (1/2) * r**2 * (theta - math.sin(theta))
            segment_volume = segment_area * l
            tank_volume = math.pi * r**2 * l
            fill_volume = segment_area * l

        else:
            theta = 2 * math.acos(m/r)
            segment_area = (1/2) * r**2 * (theta - math.sin(theta))
            fill_volume = segment_area * l
        return fill_volume

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = CylinderFillVolume()
    widget.show()
    sys.exit(app.exec_())

