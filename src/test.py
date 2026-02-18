import sys

from PySide6.QtCore             import  QSize
from PySide6.QtWidgets          import (QApplication,
                                        QMainWindow,
                                        QFrame,
                                        QHBoxLayout,
                                        QVBoxLayout,
                                        QSizePolicy,
                                        QPushButton)
from PySide6.QtWebEngineCore    import  QWebEngineSettings
from PySide6.QtWebEngineWidgets import  QWebEngineView

from VisualiserMainWindow.VisualiserMainWindow   import VisualiserMainWindow
from VisualiserSvgWidget.VisualiserSvgWidget     import VisualiserSvgWidget
from VisualiserSvgRenderer.VisualiserSvgRenderer import VisualiserSvgRenderer


if __name__ == "__main__" :

    nameMethod = "main"


    try :

        app = QApplication(sys.argv)

        app.setStyleSheet("""
            QFrame {
                background-color: lightgray;
            }  
        """)

        window = VisualiserMainWindow()

        window.initialise(app)

        window.show()
        app.exec()

    except Exception as e:

        print(nameMethod + " : CAUGHT THE FOLLOWING EXCEPTION")
        print(nameMethod + " : " + str(e))

    exit(False)