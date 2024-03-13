from PyQt5.QtCore import QObject, pyqtSignal
import numpy as np


class FileLoader(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def __init__(self, files_to_load):
        super().__init__()
        self.files_to_load = files_to_load
        self.loading_results = {}

    def run(self):
        for f in self.files_to_load:
            print(">> Loading " + f)
            res = np.genfromtxt(f, filling_values=0.0)
            self.loading_results[f] = res
            # self.progress.emit(i + 1)
        print(">> File loader emit")
        self.finished.emit()

    def get_results(self):
        return self.loading_results
