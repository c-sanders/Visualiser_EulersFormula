from PySide6.QtWidgets                       import (QMainWindow,
                                                     QFrame,
                                                     QHBoxLayout)

from SvgMetadataReader.SvgMetadataReader     import  SvgMetadataReader
from VisualiserPanelSide.VisualiserPanelSide import  VisualiserPanelSide
from VisualiserPanelPlot.VisualiserPanelPlot import  VisualiserPanelPlot


class VisualiserMainWindow(QMainWindow) :

    # According to advice from ChatGPT;
    #
    #   - Constructor -> Create widgets
    #   - Initialise  -> Configure, connect, and load data
    #
    #
    # Helper methods could be named as follows;
    #
    #   _create_actions()
    #   _create_menus()
    #   _create_toolbars()
    #   _create_widgets()   *
    #   _create_layouts()
    #   _connect_signals()

    # Call stack trace for method : Constructor
    # =========================================
    #
    # Visualiser_MainWindow.__init__()
    #   │
    #   ├── super().__init__()
    #   ├── Visualiser_MainWindow.__setup_settings()
    #   ├── Visualiser_MainWindow.__create_widgets()
    #   │     ├── VisualiserPanelSide()
    #   │     └── Visualiser_Panel_Plot()
    #   ├── Visualiser_MainWindow.__create_objects()
    #   └── SvgMetadataReader()

    # Call stack trace for method : initialise
    # ========================================
    #
    # Visualiser_MainWindow.initialise()
    #   ├── Visualiser_MainWindow.__create_actions()
    #   ├── Visualiser_MainWindow.__create_menus()
    #   ├── Visualiser_MainWindow.__create_toolbars()
    #   ├── Visualiser_MainWindow.__create_and_configure_layouts()
    #   │     └── Visualiser_MainWindow.__setup_widget_central()
    #   ├── Visualiser_MainWindow.__create_signal_connections
    #   └── Visualiser_MainWindow.__configure
    #         ├── setWindowTitle
    #         ├── panel_side.set_window_main
    #         └── Visualiser_MainWindow.__setup_objects_other


    def __init__(self) :

        nameMethod = self.__class__.__name__ + \
                     "::__init__"


        print(nameMethod + " : Enter")

        super().__init__()

        self._is_initialised = False

        self.__setup_settings()
        self.__create_widgets()
        self.__create_objects()

        print(nameMethod + " : Exit")


    def initialise(self) :

        if self._is_initialised :

            return

        # Create GUI components.

        self.__create_actions()
        self.__create_menus()
        self.__create_toolbars()
        self.__create_and_configure_layouts()
        self.__create_signal_connections()

        # Perform various configuration tasks.

        self.__configure()

        # Initialise child widgets.

        self.panel_side.initialise()
        self.panel_plot.initialise()

        self._is_initialised = True


    def __setup_settings(self) :

        nameMethod = self.__class__.__name__ + \
                     "::__setup_settings"


        print(nameMethod + " : Enter")

        self.titleWindow = "Visualiser"

        print(nameMethod + " : Exit")


    def __create_widgets(self) :

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

        self.panel_side = VisualiserPanelSide()
        self.panel_plot = VisualiserPanelPlot()

        print(nameMethod + " : Exit")


    def __create_objects(self) :

        self.svg_metadata_reader = SvgMetadataReader()


    def __create_actions(self) :

        pass


    def __create_menus(self) :

        pass


    def __create_toolbars(self) :

        pass


    def __create_signal_connections(self) :

        pass


    def __configure(self) :

        """
        Perform various configuration tasks that don't really fit in
        anywhere else.

        Set the title of the app in the window frame and inform the
        side panel of the main window.
        """

        self.setWindowTitle(self.titleWindow)

        self.panel_side.set_window_main(self)

        self.__setup_objects_other()


    def __create_and_configure_layouts(self) :

        """
        Set the layout for the central widget and then set the central widget
        to be the central widget of the main window.

        Once this is done, add the child widgets into the central widget's
        layout.

        :return: NA
        """

        nameMethod = self.__class__.__name__ + \
                     "::__create_and_configure_layouts"


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


    def __setup_objects_other(self) :

        pass
