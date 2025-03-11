import sys
from gui import FileAnalyzerApp
from PyQt5.QtWidgets import QApplication

def main():
    app = QApplication(sys.argv)
    window = FileAnalyzerApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
