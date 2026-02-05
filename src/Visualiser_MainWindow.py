from PySide6.QtWidgets     import (QMainWindow, QFrame, QHBoxLayout)

from svg_metadata_reader   import SvgMetadataReader
from Visualiser_Panel_Side import Visualiser_Panel_Side
from visualiser_panel_plot import Visualiser_Panel_Plot


class Visualiser_MainWindow(QMainWindow) :

    def __init__(self) :

        nameMethod = self.__class__.__name__ + \
                     "::__init__"


        print(nameMethod + " : Enter")

        super().__init__()

        self.setup_settings()

        self.create_and_configure_child_widgets()
        self.setup_widget_central()
        self.setup_widgets_other()

        print(nameMethod + " : Exit")


    def setup_settings(self) :

        nameMethod = self.__class__.__name__ + \
                     "::setup_settings"


        print(nameMethod + " : Enter")

        self.svg_metadata_reader = SvgMetadataReader()

        print(nameMethod + " : Exit")


    def create_and_configure_child_widgets(self) :

        """
        Create the central widget for the object and create the central
        widget's child widgets.

        Create a new QFrame which will be used as this object's central
        widget.

        :return: NA
        """

        nameMethod = self.__class__.__name__ + \
                     "::create_and_configure_child_widgets"


        print(nameMethod + " : Enter")

        self.widget_central  = QFrame()

        self.panel_side = Visualiser_Panel_Side()
        self.panel_plot = Visualiser_Panel_Plot()

        print(nameMethod + " : Exit")


    def setup_widget_central(self) :

        """
        Set the central widget for the object and set the layout for the
        central widget.

        Create a new QHBoxLayout and set it to be the layout for this object's
        central widget. Only 2 widgets are added into this layout; the side
        panel and the plot panel.

        :return: NA
        """

        nameMethod = self.__class__.__name__ + \
                     "::setup_widget_central"


        print(nameMethod + " : Enter")

        # Create the layout for the object's central widget and instruct the
        # central widget to use it.

        layout = QHBoxLayout()

        self.widget_central.setLayout(layout)

        # Set the central widget for this object.

        self.setCentralWidget(self.widget_central)

        # Add the child widgets into the central widget's layout.

        layout.addWidget(self.panel_side)
        layout.addWidget(self.panel_plot)

        print(nameMethod + " : Exit")


    def setup_widgets_other(self) :

        self.panel_side.set_window_main(self)
