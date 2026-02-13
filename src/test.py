import sys

from PySide6.QtWidgets          import (QApplication,
                                        QMainWindow,
                                        QFrame,
                                        QHBoxLayout,
                                        QVBoxLayout,
                                        QSizePolicy)
from PySide6.QtWebEngineCore    import  QWebEngineSettings
from PySide6.QtWebEngineWidgets import  QWebEngineView

from VisualiserSvgWidget.VisualiserSvgWidget     import VisualiserSvgWidget
from VisualiserSvgRenderer.VisualiserSvgRenderer import VisualiserSvgRenderer
from VisualiserPanelSide.VisualiserPanelSide     import VisualiserPanelSide


if __name__ == "__main__" :

    nameMethod = "main"


    try :

        app = QApplication(sys.argv)

        # Method : createWidgets

        # svg_widget_a = VisualiserSvgWidget("/home/craig/source_code/python/visualiser_8_Feb_2026/Visualiser_EulersFormula/src/title_plot.svg")
        svg_widget_a = VisualiserSvgRenderer("/home/craig/source_code/python/visualiser_8_Feb_2026/Visualiser_EulersFormula/src/title_plot.svg")
        svg_widget_b = VisualiserSvgWidget("/home/craig/source_code/python/visualiser_8_Feb_2026/svg/Eulers_formula_(45,8).svg")
        # svg_widget = QSvgWidget("/home/craig/source_code/python/visualiser_8_Feb_2026/svg/Eulers_formula_(45,8).svg")
        # svg_widget.setAspectRatioMode(Qt.KeepAspectRatio)

        # svg_widget_a.setScale(5.0)

        window = QMainWindow()

        visualiserSidePanel = VisualiserPanelSide()
        visualiserSidePanel.set_window_main(window)
        visualiserSidePanel.initialise()

        frame_topLevel   = QFrame()
        frame_rightPane  = QFrame()
        frame_plotTitle  = QFrame()
        layout_topLevel  = QHBoxLayout(frame_topLevel)
        layout_rightPane = QVBoxLayout(frame_rightPane)
        layout_plotTitle = QVBoxLayout(frame_plotTitle)

        layout_topLevel.addWidget(visualiserSidePanel)
        layout_topLevel.addWidget(frame_rightPane)

        plot_title = QWebEngineView()

        with open("/home/craig/source_code/python/visualiser_8_Feb_2026/Visualiser_EulersFormula/src/html/mathjax.html", "r") as file_handle :

            html_mathjax = file_handle.read()

        print(nameMethod + " : ##################################################")
        print(nameMethod + " : ##################################################")
        print(nameMethod + " : html_mathjax = " + html_mathjax)
        print(nameMethod + " : ##################################################")
        print(nameMethod + " : ##################################################")

        # self.plot_title.load(local_url)
        # self.plot_title.setUrl(QUrl.fromLocalFile("/home/craig/source_code/python/Visualiser_EulersFormula/plot_title_basic.html"))
        plot_title.setHtml(html_mathjax)

        plot_title.settings().setAttribute \
                (
                QWebEngineSettings.WebAttribute.ShowScrollBars,
                False
            )

        if False :
            frame_plotTitle.setStyleSheet("""
                border: 1px solid black;   /* thickness, style, color */
                border-radius: 5px;        /* optional rounded corners */
                padding: 5px;              /* space inside the border */
            """)
        else :
            frame_plotTitle.setFrameShape(QFrame.Box)
            frame_plotTitle.setLineWidth(1)
            frame_plotTitle.setMidLineWidth(0)

            frame_plotTitle.setStyleSheet("""
                border:        1px solid black;  /* border thickness and color */
                border-radius: 5px;              /* rounded corners */
                padding:       5px;              /* space inside the frame */
            """)

        # frame_plotTitle.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # plot_title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

        plot_title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        plot_title.setFixedHeight(80)  # adjust to taste

        frame_plotTitle.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

        layout_plotTitle.addWidget(plot_title)

        svg_widget_b.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout_rightPane.addWidget(frame_plotTitle)
        # layout.addWidget(svg_widget_a, stretch=1)
        layout_rightPane.addWidget(svg_widget_b)

        window.setCentralWidget(frame_topLevel)

        window.show()
        app.exec()

    except Exception as e:

        print(nameMethod + " : CAUGHT THE FOLLOWING EXCEPTION")
        print(nameMethod + " : " + str(e))

    exit(False)