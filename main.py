from gui import FaceLockApp
from PyQt5.QtWidgets import QApplication
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FaceLockApp()
    window.show()
    sys.exit(app.exec_())
