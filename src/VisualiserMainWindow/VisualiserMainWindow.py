import os

from pathlib                                         import  Path

from PySide6.QtCore                                  import (QSize,
                                                             QThread,
                                                             Signal,
                                                             Slot)
from PySide6.QtGui                                   import  QAction
from PySide6.QtWidgets                               import (QMainWindow,
                                                             QFrame,
                                                             QHBoxLayout,
                                                             QFileDialog)

from VisualiserPanelSide.VisualiserPanelSide         import  VisualiserPanelSide
from VisualiserPanelPlot.VisualiserPanelPlot         import  VisualiserPanelPlot
from VisualiserAnimationLoop.VisualiserAnimationLoop import  VisualiserAnimationLoop

from PlotGenerators.PlotGenerator_EulersFormula      import  PlotGenerator_EulersFormula


class VisualiserMainWindow(QMainWindow) :

    signal_eventResize = Signal(str, str)


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

    # MAIN
    # THREAD
    # ────────────
    # __init__()
    # ├── setup_settings
    # ├── create_objects
    # ├── setup_ui
    # ├── connect_signals
    # ├── create_threading_components
    # │     └── thread.start()
    # ├── restore_settings
    # └── initialise()
    #       ├── setup_layouts
    #       ├── setup_signal_connections
    #       ├── configure
    #       ├── initialise_child_widgets
    #       ├── setMinimumSize
    #       └── resize()
    #
    # EVENT LOOP STARTS
    # ├── resizeEvent()
    # │     └── emit resize signal
    # ├── paintEvent()
    # │     └── emit resize signal
    # └── other events
    #
    # WORKER THREAD
    # ──────────────
    # run()
    # └── finished → cleanup

    def __init__(self, app) :

        """
        Constructor for class VisualiserMainWindow.

        This method does very little work itself. Instead, it delegates most of
        its work to a number of smaller and more focussed, private helper
        methods.

        :param app: A reference to the GUI QApplication object.
        :type app: QtWidgets.QApplication
        :return: NA
        """

        nameMethod = self.__class__.__name__ + \
                     "::__init__"


        print(nameMethod + " : Enter")

        super().__init__()

        self._is_initialised = False

        # Perform tasks that the UI might rely upon.
        #
        #   - set settings
        #   - create objects

        self.__setup_settings()
        self.__create_objects()

        self.__setup_ui()
        self.__create_threading_components()

        # What is the following method meant to do exactly?

        self.__restore_settings()

        self.initialise(app)

        self.worker_animation.moveToThread(self.thread_animation)
        self.thread_animation.start()
        print(nameMethod + " : Have created a worker thread")

        self.__set_window_sizes()

        print(nameMethod + " : Exit")


    def __setup_ui(self) :

        """
        Setup the UI for this object.

        This method does very little work itself. Instead, it delegates most of
        its work to a number of smaller and specialist, private helper methods.

        :param: NA
        :return: NA
        """

        self.__create_widgets()
        self.__create_actions()
        self.__create_menus()
        self.__create_toolbars()


    def initialise(self, app) :

        nameMethod = self.__class__.__name__ + \
                     "::initialise"


        print(nameMethod + " : Enter")

        if self._is_initialised :

            return

        self.app = app

        # Create GUI components.

        self.__setup_layouts()

        self.__connect_signals()

        # Perform various configuration tasks.

        self.__configure()

        self.initialise_child_widgets()

        self._is_initialised = True

        print(nameMethod + " : Exit")


    def initialise_child_widgets(self) :

        nameMethod = self.__class__.__name__ + \
                     "::initialise_child_widgets"


        print(nameMethod + " : Enter")

        self.panel_side.initialise()
        self.panel_plot.initialise(self.app)

        print(nameMethod + " : Exit")


    def __setup_settings(self) :

        nameMethod = self.__class__.__name__ + \
                     "::__setup_settings"


        print(nameMethod + " : Enter")

        self.titleWindow           = "Visualiser"
        self.width_window_minimum  = 960
        self.height_window_minimum = 820
        self.size_window_minimum   = QSize(self.width_window_minimum, self.height_window_minimum)

        self.filename_list_svg_file = "/home/craig/source_code/python/visualiser_8_Feb_2026/list_svg_files.txt"

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

        self.app                 = None


    def __create_actions(self) :

        # new_action = QAction("New", self)
        # new_action.setShortcut("Ctrl+N")

        # open_action = QAction("Open", self)
        # open_action.setShortcut("Ctrl+O")

        self.exit_action = QAction("Exit", self)
        self.exit_action.setShortcut("Ctrl+Q")


        self.generate_plots_0_action = QAction("Generate Plots - e Base", self)
        self.generate_plots_1_action = QAction("Generate Plots - Varying Base", self)

        self.about_action = QAction("About", self)


    def __create_menus(self) :

        menu_bar = self.menuBar()

        # Create menus.

        file_menu  = menu_bar.addMenu("&File")
        tools_menu = menu_bar.addMenu("&Tools")
        help_menu  = menu_bar.addMenu("&Help")

        # Add actions to File menu.

        # file_menu.addAction(new_action)
        # file_menu.addAction(open_action)
        # file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

        # Add actions to Tools menu.

        tools_menu.addAction(self.generate_plots_0_action)
        tools_menu.addAction(self.generate_plots_1_action)

        # Add actions to Help menu.

        help_menu.addAction(self.about_action)


    def __create_toolbars(self) :

        pass


    def __connect_signals(self) :

        nameMethod = self.__class__.__name__ + \
                     "::__connect_signals"


        print(nameMethod + " : Enter")

        try :

            self.exit_action.triggered.connect(self.close)

            # Connect signal to slot
            # Signal : VisualiserAnimationLoop : signal_svg_metadata_updated
            # Slot   : VisualiserPanelSide     : __signal_svg_metadata_updated

            # self.worker_animation.connect(self.panel_plot.slot_svg_metadata_updated)

            self.signal_eventResize.connect(self.panel_side.slot_eventResize)

            self.thread_animation.started.connect(self.worker_animation.run)
            self.worker_animation.finished.connect(self.thread_animation.quit)
            self.worker_animation.finished.connect(self.worker_animation.deleteLater)
            self.thread_animation.finished.connect(self.thread_animation.deleteLater)

            # self.signal_eventResize.emit(str(width), str(height))

            self.worker_animation.signal_svg_metadata_updated.connect(self.panel_side.slot_svg_metadata_updated)

            self.generate_plots_1_action.triggered.connect(self.generate_plots_varying_base)

        except Exception as e :

            print(nameMethod + " : &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
            print(nameMethod + " : &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
            print(nameMethod + " : &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
            print(nameMethod + " : CAUGHT THE FOLLOWING EXCEPTION")
            print(nameMethod + " : &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
            print(nameMethod + " : &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
            print(nameMethod + " : &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
            print(nameMethod + " : " + str(e))


    def generate_plots_varying_base(self) :

        nameMethod = self.__class__.__name__ + \
                     "::generate_plots_varying_base"


        print(nameMethod + " : Enter")

        directory = QFileDialog.getExistingDirectory(
            self,
            "Select a folder to save plots into",
            ""  # Starting directory (optional)
        )

        print(nameMethod + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print(nameMethod + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print(nameMethod + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print(nameMethod + " : Directory name = " + directory)
        print(nameMethod + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print(nameMethod + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print(nameMethod + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

        path_directory = Path(directory)

        if not path_directory.exists() :

            raise Exception("Method " + nameMethod + " says : Directory does not exist = " + directory)

        if not path_directory.is_dir() :

            raise Exception("Method " + nameMethod + " says : Is not a directory = " + directory)

        if not os.access(path_directory, os.W_OK) :

            raise Exception("Method " + nameMethod + " says : Do not have write permission to the directory = " + directory)

        # Generate the plots, saving them into the directory which was just selected.from

        # Put this code into a separate thread.
        #
        # Use a progress bar to inform the user.

        print(nameMethod + " : @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print(nameMethod + " : @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print(nameMethod + " : @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print(nameMethod + " : About to create a new thread")
        print(nameMethod + " : @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print(nameMethod + " : @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print(nameMethod + " : @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

        self.thread_plot_generator = QThread()
        self.worker_plot_generator = PlotGenerator_EulersFormula(directory)

        progress = QProgressBar()
        progress.setRange(0, 360)  # min, max
        progress.setValue(0)
        progress.show()
        progress.display()

        self.thread_plot_generator.started.connect(self.worker_plot_generator.run)
        self.worker_plot_generator.progress.connect(self.update_progress)
        self.worker_plot_generator.finished.connect(self.thread_plot_generator.quit)
        self.worker_plot_generator.finished.connect(self.worker_plot_generator.deleteLater)
        self.thread_plot_generator.finished.connect(self.thread_plot_generator.deleteLater)

        # self.worker_animation.moveToThread(self.thread_animation)
        # self.thread_animation.start()
        # print(nameMethod + " : Have created a worker thread")

        print(nameMethod + " : @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print(nameMethod + " : @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print(nameMethod + " : @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print(nameMethod + " : About to move object to thread")
        print(nameMethod + " : @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print(nameMethod + " : @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print(nameMethod + " : @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

        self.worker_plot_generator.moveToThread(self.thread_plot_generator)

        print(nameMethod + " : @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print(nameMethod + " : @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print(nameMethod + " : @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print(nameMethod + " : About to start the new thread")
        print(nameMethod + " : @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print(nameMethod + " : @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print(nameMethod + " : @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

        self.thread_plot_generator.start()

        print(nameMethod + " : //////////////////////////////////////////////////")
        print(nameMethod + " : //////////////////////////////////////////////////")
        print(nameMethod + " : //////////////////////////////////////////////////")
        print(nameMethod + " : Should have started the new thread")
        print(nameMethod + " : //////////////////////////////////////////////////")
        print(nameMethod + " : //////////////////////////////////////////////////")
        print(nameMethod + " : //////////////////////////////////////////////////")

        # plot_generator_EulersFormula = PlotGenerator_EulersFormula(directory)

        # plot_generator_EulersFormula.generate_plots()


        print(nameMethod + " : Exit")


    def __create_threading_components(self) :

        """
        Create the necessary threading components.
        """

        nameMethod = self.__class__.__name__ + \
                     "::__create_threading_components"


        print(nameMethod + " : Enter")

        # Create a new thread of execution and a new object of class
        # VisualiserAnimationLoop. Once this is done, start the object
        # running in the new thread of execution.

        self.thread_animation = QThread()
        self.worker_animation = VisualiserAnimationLoop(self.filename_list_svg_file)

        print(nameMethod + " : Exit")


    def __restore_settings(self) :

        """
        Set any user state settings that should be restored from the
        previous session in which this program ran.

        :return: NA
        """

        pass


    def __set_window_sizes(self) :

        self.setMinimumSize(self.size_window_minimum)
        self.resize(self.size_window_minimum)


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


    def __setup_layouts(self) :

        """
        Set the layout for the central widget and then set the central widget
        to be the central widget of the main window.

        Once this is done, add the child widgets into the central widget's
        layout.

        :return: NA
        """

        nameMethod = self.__class__.__name__ + \
                     "::__setup_layouts"


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


    # def paintEvent(self, event) :
    #
    #     nameMethod = self.__class__.__name__ + \
    #                  "::paintEvent"
    #
    #
    #     print(nameMethod + " : Enter")
    #
    #     super().paintEvent(event)
    #
    #     # Send out a signal.
    #
    #     width  = self.width()
    #     height = self.height()
    #
    #     # According to ChatGPT, you should not emit signals from within
    #     # this event. It should be for rendering only.
    #
    #     self.signal_eventResize.emit(str(width), str(height))
    #
    #     print(nameMethod + " : Exit")


    def resizeEvent(self, event) :

        nameMethod = self.__class__.__name__ + \
                     "::resizeEvent"


        print(nameMethod + " : Enter")

        super().resizeEvent(event)

        # Send out a signal.

        width  = self.width()
        height = self.height()

        self.signal_eventResize.emit(str(width), str(height))

        print(nameMethod + " : Exit")


    @Slot(str, str)
    def slot_eventResize(self, width, height) :

        nameMethod = self.__class__.__name__ + \
                     "::slot_eventResize"


        print(nameMethod + " : Enter")

        print(nameMethod + " : (width, height) = (" + width + ", " + height + ")")

        print(nameMethod + " : Exit")

    @Slot(int)
    def update_progress(self, progress_final, progress_value) :

        nameMethod = self.__class__.__name__ + \
                     "::slot_eventResize"


        print(nameMethod + " : Enter")

        print(nameMethod + " : Progress = " + str(progress_value) + "/" + str(progress_final))

        print(nameMethod + " : Exit")