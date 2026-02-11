from PySide6.QtCore    import (Qt,
                               QSize,
                               Slot)

from PySide6.QtWidgets import (QFrame,
                               QPushButton,
                               QVBoxLayout,
                               QLabel,
                               QSpinBox,
                               QGroupBox,
                               QRadioButton,
                               QButtonGroup)


class VisualiserPanelSide(QFrame) :

    # Call stack trace for method : Constructor
    # =========================================
    #
    # Visualiser_Panel_Side.__init__
    # │
    # ├── QFrame.__init__
    # ├── Visualiser_Panel_Side.__setup_settings
    # ├── Visualiser_Panel_Side.__create_widgets
    # │     ├── create_and_configure_widgets_plot_parameters
    # │     ├── create_and_configure_widgets_viewing_angle
    # │     ├── create_and_configure_widgets_playback_controls
    # │     └── create_and_configure_widgets_other
    # └── Visualiser_Panel_Side.__create_objects

    # Call stack trace for method : initialise
    # ========================================
    #
    # Visualiser_Panel_Side.initialise
    # ├── Visualiser_Panel_Side.__create_actions
    # ├── Visualiser_Panel_Side.__create_menus
    # ├── Visualiser_Panel_Side.__create_toolbars
    # ├── Visualiser_Panel_Side.__create_and_configure_layouts
    # │     ├── setup_group_box_parameters
    # │     ├── setup_group_box_viewing_angle
    # │     ├── setup_group_box_playback_controls
    # │     ├── setup_remaining_controls
    # │     └── setupEventHandlers_buttons
    # ├── Visualiser_Panel_Side.__create_signal_connections
    # └── Visualiser_Panel_Side.__configure


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

        nameMethod = self.__class__.__name__ + \
                     "::initialise"


        print(nameMethod + " : Enter")

        if self._is_initialised :

            return

        # Create GUI components.

        print(nameMethod + " : Exit")

        self.__create_actions()
        self.__create_menus()
        self.__create_toolbars()
        self.__create_and_configure_layouts()
        self.__create_signal_connections()

        # Perform various configuration tasks.

        self.__configure()

        self._is_initialised = True

        print(nameMethod + " : Exit")


    def __setup_settings(self) :

        self.file_path = None

        self.run_animation                           = True
        self.display_button_run                      = True
        self.grab_screenshot_including_window_border = False

        self.title_plotParameters         = "Plot parameters :"
        self.title_viewingAngle           = "Viewing angle :"
        self.title_viewingAngle_elevation = "Elevation"
        self.title_viewingAngle_azimuth   = "Azimuth"

        self.title_playbackControl        = "Playback controls :"

        self.plot_title_use_png_or_mathjax    = "mathjax"

        self.playAnimationInSeparateThread    = True
        self.grabScreenshots                  = False
        self.useLayoutSimuLab                 = False
        self.playForward                      = True

        self.size_buttons                     = QSize(100, 30)

        self.tool_tip_button_play_stop     = ("Name : self.pushButton_playStop"
                                              "Connects to the method : MainWindow::toggleEventAnimationLoop"
                                             )
        self.tool_tip_button_play_forward  = ("Name : self.pushButton_forward\n"
                                              "Connects to the method : MainWindow::playAnimationForward"
                                             )
        self.tool_tip_button_play_backward = ("Name : self.pushButton_backward\n"
                                              "Connects to the method : MainWindow::playAnimationBackward"
                                             )
        self.tool_tip_button_exit          = ("Name : self.pushButton_exit\n"
                                              "Connects to the method : MainWindow::shutdown_routine"
                                             )

        # Delay between frames in seconds, i.e. 50ms

        self.delayBetweenFrames = 0.05
        self.filename_titlePlot = "./Plot_label.png"

        if not self.file_path :

            self.filename_plot = "./svg/Eulers_formula_(45,0).svg"

        else :

            self.filename_plot = file_path.as_posix()


    def set_window_main(self, window_main):

        nameMethod = self.__class__.__name__ + \
                     "::set_window_main"


        print(nameMethod + " : Enter")

        self.window_main = window_main

        print(nameMethod + " : Exit")


    def __create_widgets(self) :

        self.create_and_configure_widgets_plot_parameters()
        self.create_and_configure_widgets_viewing_angle()
        self.create_and_configure_widgets_playback_controls()
        self.create_and_configure_widgets_other()


    def __create_objects(self) :

        pass


    def __create_actions(self) :

        pass


    def __create_menus(self) :

        pass


    def __create_toolbars(self) :

        pass


    def __create_and_configure_layouts(self) :

        nameMethod = self.__class__.__name__ + \
                     "::__create_and_configure_layouts"


        print(nameMethod, " : Enter")

        layout = QVBoxLayout(self)

        self.setup_group_box_parameters()
        self.setup_group_box_viewing_angle()
        self.setup_group_box_playback_controls()

        self.setup_remaining_controls()

        self.setupEventHandlers_buttons()

        print(nameMethod, " : Exit")


    def __create_signal_connections(self) :

        pass


    def create_and_configure_widgets_plot_parameters(self) :

        # ============================================================
        # Components that comprise : Plot parameters
        # ============================================================

        #   - Create components

        self.title_base         = QLabel("Base")
        self.label_base         = QLabel("2.718")

        #   - Configure components

        self.title_base.setObjectName("labelNoBorder")
        self.label_base.setObjectName("labelWithBorder")


    def create_and_configure_widgets_viewing_angle(self) :

        # ============================================================
        # Components that comprise : Viewing angle
        # ============================================================

        #   - Create components

        self.viewAngleElevLabel = QLabel(self.title_viewingAngle_elevation)
        self.elevationLabel     = QLabel("45\u00B0")
        self.viewAngleAzimLabel = QLabel(self.title_viewingAngle_azimuth)
        self.azimuthLabel       = QLabel("0\u00B0")

        #   - Configure components

        self.viewAngleElevLabel.setObjectName("labelNoBorder")
        self.viewAngleAzimLabel.setObjectName("labelNoBorder")

        self.elevationLabel.setObjectName("labelWithBorder")
        self.azimuthLabel.setObjectName("labelWithBorder")

        self.viewAngleElevLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.elevationLabel.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.azimuthLabel.setAlignment(Qt.AlignmentFlag.AlignRight)


    def create_and_configure_widgets_playback_controls(self) :

        # ============================================================
        # Components that comprise : Playback controls
        # ============================================================

        #   - Create components

        # layout_playbackControl.addWidget(self.labelPlayDirection)
        # layout_playbackControl.addWidget(self.labelCurrentPlayDirection)

        self.radioButtonGroup = QButtonGroup()

        self.radioButton_playForward  = QRadioButton("Forward")
        self.radioButton_playBackward = QRadioButton("Backward")

        self.radioButton_playForward.setChecked(True)
        self.radioButton_playBackward.setChecked(False)

        self.label_playback      = QLabel("Playback")

        self.delayFrameLabel     = QLabel("Frame delay (in ms)")
        self.delayFrame          = QSpinBox()

        self.pushButton_playStop = QPushButton("Play")

        # self.labelPlayDirection = QLabel("Current direction")
        # self.labelPlayDirection.setObjectName("labelNoBorder")

        # self.labelCurrentPlayDirection = QLabel("Forward")

        # self.pushButton_backward = QPushButton("<")
        # self.pushButton_forward  = QPushButton(">")

        #   - Configure components

        self.delayFrame.setRange(10, 10000)  # Min = 10ms | Max = 10,000ms = 10s
        self.delayFrame.setSingleStep(10)
        self.delayFrame.setValue(50)

        self.delayFrameLabel.setObjectName("labelNoBorder")
        self.delayFrame.setObjectName("spinBox")

        self.label_playback.setObjectName("labelNoBorder")

        self.label_base.setAlignment(Qt.AlignmentFlag.AlignRight)

        # self.labelCurrentPlayDirection.setObjectName("labelWithBorder")
        # self.labelCurrentPlayDirection.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Play/Stop button

        self.pushButton_playStop.setFixedSize(self.size_buttons)

        self.groupBox_playbackControl = QGroupBox(self.title_playbackControl)
        self.layout_playbackControl   = QVBoxLayout()

        self.groupBox_playbackControl.setObjectName("groupBox_blackText")
        self.groupBox_playbackControl.setLayout(self.layout_playbackControl)


    def create_and_configure_widgets_other(self) :

        # Other components

        self.pushButton_shutdown   = QPushButton("Shutdown")
        self.pushButton_screenshot = QPushButton("Screenshot")
        self.pushButton_exit       = QPushButton("Exit")

        # self.pushButton_forward.setToolTip(self.tool_tip_button_play_forward)
        # self.pushButton_backward.setToolTip(self.tool_tip_button_play_backward)

        self.pushButton_exit.setToolTip(self.tool_tip_button_exit)

        self.pushButton_playStop.setToolTip(self.tool_tip_button_play_forward)
        self.pushButton_shutdown.setToolTip("Connects to the method : MainWindow::shutdownAnimationThread")


    def setup_remaining_controls(self) :

        nameMethod = self.__class__.__name__ + \
                     "::setup_remaining_controls"


        print(nameMethod, " : Enter")

        # Add the Play and Exit buttons to the side panel.

        self.layout().addStretch(1)
        self.layout().addWidget(self.pushButton_playStop, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.layout().addStretch(1)
        self.layout().addWidget(self.pushButton_screenshot,     alignment=Qt.AlignmentFlag.AlignHCenter)
        self.pushButton_screenshot.setFixedSize(self.size_buttons)

        print(nameMethod + " : self.pushButton_screenshot.width  = " + str(self.pushButton_screenshot.width()))
        print(nameMethod + " : self.pushButton_screenshot.height = " + str(self.pushButton_screenshot.height()))

        self.layout().addStretch(1)
        self.layout().addWidget(self.pushButton_exit,     alignment=Qt.AlignmentFlag.AlignHCenter)
        self.pushButton_exit.setFixedSize(self.size_buttons)

        # pushButton_forward.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # pushButton_backward.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # self.frame_panel_side.setLayout(self.layout_panel_side)
        self.setFixedWidth(200)

        # self.layout_panel_sideAndPlot.addLayout(self.layout_panel_side)
        # self.layout_panel_sideAndPlot.addWidget(self.frame_panel_side)

        # Setup button event handlers.

        # self.setupEventHandlers_buttons()

        print(nameMethod, " : Exit")


    def setup_group_box_parameters(self) :

        groupBox_plotParameters = QGroupBox(self.title_plotParameters)
        layout_plotParameters   = QVBoxLayout()


        groupBox_plotParameters.setObjectName("groupBox_blackText")
        groupBox_plotParameters.setLayout(layout_plotParameters)

        # Base

        layout_plotParameters.addWidget(self.title_base)
        layout_plotParameters.addWidget(self.label_base)

        self.layout().addWidget(groupBox_plotParameters)


    def setup_group_box_viewing_angle(self):

        # Controls that relate to;
        #
        #   - view angle

        groupBox_viewingAngle = QGroupBox(self.title_viewingAngle)
        layout_viewingAngle = QVBoxLayout()


        groupBox_viewingAngle.setObjectName("groupBox_blackText")
        groupBox_viewingAngle.setLayout(layout_viewingAngle)

        layout_viewingAngle.addWidget(self.viewAngleElevLabel)
        layout_viewingAngle.addWidget(self.elevationLabel)
        layout_viewingAngle.addWidget(self.viewAngleAzimLabel)
        layout_viewingAngle.addWidget(self.azimuthLabel)

        self.layout().addWidget(groupBox_viewingAngle)


    # Controls that relate to;
    #
    #   - playback direction and control

    def setup_group_box_playback_controls(self) :

        self.layout_playbackControl.addWidget(self.radioButton_playForward,  alignment=Qt.AlignmentFlag.AlignLeft)
        self.layout_playbackControl.addWidget(self.radioButton_playBackward, alignment=Qt.AlignmentFlag.AlignLeft)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)  # Set the frame shape to a horizontal line
        line.setFrameShadow(QFrame.Shadow.Sunken)  # Set the shadow effect

        self.layout_playbackControl.addWidget(line)

        # layout_playbackControl.addWidget(self.pushButton_backward, alignment=Qt.AlignmentFlag.AlignHCenter)
        # layout_playbackControl.addWidget(self.pushButton_forward, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.layout_playbackControl.addWidget(self.delayFrameLabel)
        self.layout_playbackControl.addWidget(self.delayFrame)

        self.layout().addWidget(self.groupBox_playbackControl)


    def setupEventHandlers_buttons(self):

        # self.pushButton_forward.clicked.connect(self.playAnimationForward)
        # self.pushButton_backward.clicked.connect(self.playAnimationBackward)

        # self.pushButton_playStop.clicked.connect(self.toggleEventPlayAnimationLoop)

        # self.pushButton_shutdown.clicked.connect(self.shutdownAnimationThread)

        self.pushButton_exit.clicked.connect(self.window_main.close)


    def shutdown_routine(self) :

        nameMethod = self.__class__.__name__ + \
                     "::shutdown_routine"


        print(nameMethod, " : ========================================")
        print(nameMethod, " : Enter")
        print(nameMethod, " : ========================================")

        # Inform the play loop thread that it should shutdown.

        # self.event_shutdownAnimationLoop.set()
        # self.event_playAnimationLoop.set()

        # Wait for the play loop thread to finalise its tasks and shutdown.

        # print(nameMethod, " : Waiting to join with the animation thread")

        # Check that the animation loop thread is actually running. It should be, as
        # it is started directly from __main__.

        # print(nameMethod, " : Animation loop thread = ", self.threadAnimationLoop)

        # self.threadAnimationLoop.join()

        # Parent widget          = QFrame
        # Parent - parent widget = Visualiser_MainWindow

        # self.window_main.close()

        print(nameMethod, " : Exit")


    def __configure(self) :

        """
        Perform various configuration tasks that don't really fit in
        anywhere else.
        """

        pass


    @Slot(str, str, str)
    def __signal_svg_metadata_updated(self, base, azimuth, elevation):

        nameMethod = self.__class__.__name__ + \
                     "::__signal_svg_metadata_updated"


        print(nameMethod + " : Enter")

        # This function is the slot that runs when the signal is received

        print(nameMethod + " : base = " + base)

        print(nameMethod + " : Exit")