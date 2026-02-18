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

from VisualiserMainWindow.VisualiserMainWindow_minimal import VisualiserMainWindow
from VisualiserSvgWidget.VisualiserSvgWidget           import VisualiserSvgWidget
from VisualiserSvgRenderer.VisualiserSvgRenderer       import VisualiserSvgRenderer


if __name__ == "__main__" :

    nameMethod = "main"


    try :

        app = QApplication(sys.argv)

        app.setStyleSheet("""
            QFrame {
                background-color: lightgray;
            }  
        """)

        # Method : createWidgets

        # svg_widget_a = VisualiserSvgWidget("/home/craig/source_code/python/visualiser_8_Feb_2026/Visualiser_EulersFormula/src/title_plot.svg")
        svg_widget_a = VisualiserSvgRenderer("/home/craig/source_code/python/visualiser_8_Feb_2026/Visualiser_EulersFormula/src/title_plot.svg")
        svg_widget_b = VisualiserSvgWidget("/home/craig/source_code/python/visualiser_8_Feb_2026/svg/Eulers_formula_(45,8).svg")
        # svg_widget = QSvgWidget("/home/craig/source_code/python/visualiser_8_Feb_2026/svg/Eulers_formula_(45,8).svg")
        # svg_widget.setAspectRatioMode(Qt.KeepAspectRatio)

        # svg_widget_a.setScale(5.0)

        window = VisualiserMainWindow()

        if False :

            frame_topLevel   = QFrame()
            frame_rightPane  = QFrame()
            frame_plotTitle  = QFrame()
            frame_buttons    = QFrame()

            layout_topLevel  = QHBoxLayout(frame_topLevel)
            layout_rightPane = QVBoxLayout(frame_rightPane)
            layout_plotTitle = QVBoxLayout(frame_plotTitle)
            layout_buttons   = QHBoxLayout(frame_buttons)

            layout_topLevel.addWidget(visualiserSidePanel)
            layout_topLevel.addWidget(frame_rightPane)
            layout_topLevel.addWidget(visualiserPanelPlot)

        # VisualiserPanelPlot::__setup_panel_plotTitle_usingMathJax

        # frame_plotTitle.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # plot_title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

        ### window.signal_eventResize.connect(visualiserSidePanel.slot_eventResize)

        # window.setCentralWidget(frame_topLevel)

        window.initialise()

        window.setMinimumSize(751, 820)
        window.resize(751, 820)

        window.show()
        app.exec()

    except Exception as e:

        print(nameMethod + " : CAUGHT THE FOLLOWING EXCEPTION")
        print(nameMethod + " : " + str(e))

    exit(False)