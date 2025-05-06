import sys
from gui import FileAnalyzerApp
from PyQt5.QtWidgets import QApplication

def main():
    app = QApplication(sys.argv)
    window = FileAnalyzerApp()
    window.show()
    sys.exit(app.exec()) # il codice di uscira di app.exec() viene passato a sys.exit

if __name__ == '__main__':
    main()
