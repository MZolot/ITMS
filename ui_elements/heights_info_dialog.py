import ui_elements.qt_designer_ui.plot_dialog_ui as dialog_ui
from .math_text import *
from PyQt5 import QtWidgets


class HeightCharacteristic:
    def __init__(self, name, formula_text, info_text, computation_function=None):
        self.name = name
        self.formula_text = '$' + formula_text + '$'
        self.info_text = info_text
        self.computation_function = computation_function


class HeightsInfoDialog(QtWidgets.QDialog, dialog_ui.Ui_Dialog):
    def __init__(self, parent, wave_profile):
        super().__init__(parent)
        self.setupUi(self)

        self.dialog_characteristics = [
            HeightCharacteristic(name="N", formula_text="N",
                                 info_text="- number of available run-up measurements (for a particular event)"),
            HeightCharacteristic(name="H_max", formula_text="H_{max}",
                                 info_text="- maximum measured run-up height"),
            HeightCharacteristic(name="H_min", formula_text="H_{min}",
                                 info_text="- minimum measured run-up height"),
            HeightCharacteristic(name="H_avg", formula_text="\\overline{H} = \\frac{1}{N} \\sum_{1}^{N} H_i",
                                 info_text="- average run_up height"),
            HeightCharacteristic(name="H_log", formula_text="\\widetilde{H} = 10^{\\frac{1}{N} * \\sum_{1}^{N} lgH_i}",
                                 info_text="- logarithmic average run-up height"),
            HeightCharacteristic(name="I", formula_text="I = \\frac{1}{2} + log_2 \\overline{H}",
                                 info_text="- tsunami intensity on Soloviev-Imamura scale"),
            HeightCharacteristic(name="I_mod", formula_text="\\widetilde{I} = \\frac{1}{2} + log_2 \\widetilde{H}",
                                 info_text="- modified tsunami intensity on Soloviev-Imamura scale"),
            HeightCharacteristic(name="m", formula_text="m",
                                 info_text="- magnitude of tsunami on Imamura scale"),
        ]
        self.widget = QtWidgets.QWidget()
        self.setup_grid()
        self.vertical_layout.insertWidget(0, self.widget)

        # self.vertical_layout.insertWidget(0, plot.get_widget())
        self.setWindowTitle("Coastal profile info")
        self.adjustSize()
        self.push_button_close.clicked.connect(self.close)

    def setup_grid(self):
        layout = QtWidgets.QGridLayout()
        for i, characteristic in enumerate(self.dialog_characteristics):
            line_edit = QtWidgets.QLineEdit()
            line_edit.setMaximumWidth(70)
            layout.addWidget(line_edit, i, 0)
            formula_label = MathTextLabel(characteristic.formula_text, self)
            # formula_label.setMinimumWidth(150)
            layout.addWidget(formula_label, i, 1)
            info_label = QtWidgets.QLabel(characteristic.info_text)
            layout.addWidget(info_label, i, 2)
        self.widget.setLayout(layout)
