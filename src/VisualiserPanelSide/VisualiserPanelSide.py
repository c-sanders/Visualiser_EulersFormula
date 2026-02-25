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
                               QButtonGroup,
                               QDial)
from PySide6.QtGui     import (QPalette,
                               QColor)


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
    # │     ├── create_and_configure_widgets_window_dimensions
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
    # │     ├── setup_group_box_frame_delay
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

        self.debug = False

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

        self.title_playbackControl         = "Playback controls :"
        self.title_playbackDirection       = "Playback direction :"
        self.title_frameDelay              = "Frame delay (in ms)"
        self.title_windowDimensions        = "Window dimensions :"
        self.title_windowDimensions_width  = "Width (in pixels)"
        self.title_windowDimensions_height = "Height (in pixels)"
        self.title_pane_dial               = "Imaginary number :"

        self.plot_title_use_png_or_mathjax    = "mathjax"

        self.playAnimationInSeparateThread    = True
        self.grabScreenshots                  = False
        self.useLayoutSimuLab                 = False
        self.playForward                      = True

        self.size_buttons                     = QSize(100, 30)
        self.size_dials                       = QSize(100, 100)

        self.tool_tip_button_play_stop     = ("Name : self.pushButton_playStop"
                                              "Connects to the method : MainWindow::toggleEventAnimationLoop"
                                             )
        self.tool_tip_button_play_forward  = ("Name : self.pushButton_forward\n"
                                              "Connects to the method Azimuth: MainWindow::playAnimationForward"
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
        self.create_and_configure_widgets_window_dimensions()
        self.create_and_configure_widgets_pane_dial()
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
        self.setup_group_box_frame_delay()
        self.setup_group_box_window_dimensions()

        self.setup_remaining_controls()

        self.setupEventHandlers_buttons()

        print(nameMethod, " : Exit")


    def __create_signal_connections(self) :

        self.pushButton_remove.clicked.connect(self.__slot_remove_button_from_layout)


    def create_and_configure_widgets_plot_parameters(self) :

        # ============================================================
        # Components that comprise : Plot parameters
        # ============================================================

        #   - Create components

        self.title_base         = QLabel("Base")
        self.label_base         = QLabel("2.718")

        #   - Configure components

        self.label_base.setObjectName("label_whiteBackground")


    def create_and_configure_widgets_viewing_angle(self) :

        # ============================================================
        # Components that comprise : Viewing angle
        # ============================================================

        #   - Create components

        self.viewAngleElevLabel = QLabel(self.title_viewingAngle_elevation)
        self.elevationLabel     = QLabel("45\u00B0")
        self.viewAngleAzimLabel = QLabel(self.title_viewingAngle_azimuth)
        self.azimuthLabel       = QLabel("0\u00B0")

        # TODO : Finish implementing the following.

        self.dimensionsWindowLabel = QLabel("Window dimensions")
        # self.azimuthLabel       = QLabel("0\u00B0")

        #   - Configure components

        self.viewAngleElevLabel.setObjectName("labelNoBorder")
        self.viewAngleAzimLabel.setObjectName("labelNoBorder")

        self.elevationLabel.setObjectName("label_whiteBackground")
        self.azimuthLabel.setObjectName("label_whiteBackground")

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

        self.groupBox_playbackControl = QGroupBox(self.title_playbackControl)
        self.layout_playbackControl   = QVBoxLayout(self.groupBox_playbackControl)
        self.groupBox_playbackControl.setObjectName("groupBox_blackText")

        self.groupBox_playbackDirection = QGroupBox(self.title_playbackDirection)
        self.layout_playbackDirection   = QVBoxLayout(self.groupBox_playbackDirection)
        self.groupBox_playbackDirection.setObjectName("groupBox_blackText")

        # self.groupBox_playbackControl.setLayout(self.layout_playbackControl)

        self.groupBox_frameDelay = QGroupBox(self.title_frameDelay)
        self.layout_frameDelay   = QVBoxLayout(self.groupBox_frameDelay)

        self.groupBox_frameDelay.setObjectName("groupBox_blackText")


    def create_and_configure_widgets_window_dimensions(self) :

        # Screen dimensions

        #   - Create components

        self.label_title_windowDimensions_width  = QLabel(self.title_windowDimensions_width)
        self.label_value_windowDimensions_width  = QLabel("---")
        self.label_title_windowDimensions_height = QLabel(self.title_windowDimensions_height)
        self.label_value_windowDimensions_height = QLabel("---")

        self.groupBox_windowDimensions = QGroupBox(self.title_windowDimensions)
        self.layout_windowDimensions   = QVBoxLayout(self.groupBox_windowDimensions)

        self.label_value_windowDimensions_width.setObjectName("label_whiteBackground")
        self.label_value_windowDimensions_height.setObjectName("label_whiteBackground")

        self.label_value_windowDimensions_width.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.label_value_windowDimensions_height.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.layout_windowDimensions.addWidget(self.label_title_windowDimensions_width)
        self.layout_windowDimensions.addWidget(self.label_value_windowDimensions_width)
        self.layout_windowDimensions.addWidget(self.label_title_windowDimensions_height)
        self.layout_windowDimensions.addWidget(self.label_value_windowDimensions_height)


    def create_and_configure_widgets_other(self) :

        # Other components

        self.pushButton_playStop = QPushButton("Play")
        self.pushButton_shutdown = QPushButton("Remove me")
        self.pushButton_remove   = QPushButton("Remove")

        # Play/Stop button

        self.pushButton_playStop.setFixedSize(self.size_buttons)

        # self.pushButton_forward.setToolTip(self.tool_tip_button_play_forward)
        # self.pushButton_backward.setToolTip(self.tool_tip_button_play_backward)

        # self.pushButton_exit.setToolTip(self.tool_tip_button_exit)

        self.pushButton_playStop.setToolTip(self.tool_tip_button_play_forward)
        self.pushButton_shutdown.setToolTip("Connects to the method : MainWindow::shutdownAnimationThread")


    def create_and_configure_widgets_pane_dial(self) :

        nameMethod = self.__class__.__name__ + \
                     "::create_and_configure_widgets_pane_dial"

        dial  = QDial()
        label = QLabel("---")

        self.groupBox_pane_dial    = QGroupBox(self.title_pane_dial)
        layout_pane_dial = QVBoxLayout(self.groupBox_pane_dial)

        label.setObjectName("label_whiteBackground")
        label.setAlignment(Qt.AlignmentFlag.AlignRight)

        print(nameMethod, " : Enter")

        # Configure the dial.

        dial.setRange(0, 100)
        dial.setNotchesVisible(True)
        dial.setFixedSize(self.size_dials)
        dial.setWrapping(True)

        # Configure the notches that are associated with the dial.

        palette = dial.palette()
        palette.setColor(QPalette.Dark, QColor("black"))  # Notch color
        palette.setColor(QPalette.Shadow, QColor("black"))  # Sometimes used too
        dial.setPalette(palette)

        layout_pane_dial.addWidget(dial, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout_pane_dial.addWidget(label)

        print(nameMethod, " : Exit")


    def setup_remaining_controls(self) :

        nameMethod = self.__class__.__name__ + \
                     "::setup_remaining_controls"


        print(nameMethod, " : Enter")

        # Add the Play and Exit buttons to the side panel.

        self.layout().addStretch(1)
        # self.layout().addWidget(self.pushButton_playStop, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.layout().addWidget(self.pushButton_playStop, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.layout().addWidget(self.groupBox_pane_dial)

        self.layout().addStretch(2)
        # self.layout().addWidget(self.pushButton_remove, alignment=Qt.AlignmentFlag.AlignHCenter)
        # self.layout().addStretch(1)
        # self.layout().addWidget(self.pushButton_screenshot, alignment=Qt.AlignmentFlag.AlignHCenter)
        # self.pushButton_screenshot.setFixedSize(self.size_buttons)

        # print(nameMethod + " : self.pushButton_screenshot.width  = " + str(self.pushButton_screenshot.width()))
        # print(nameMethod + " : self.pushButton_screenshot.height = " + str(self.pushButton_screenshot.height()))

        # self.layout().addStretch(1)
        # self.layout().addWidget(self.pushButton_exit,     alignment=Qt.AlignmentFlag.AlignHCenter)
        # self.pushButton_exit.setFixedSize(self.size_buttons)

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
        self.layout_plotParameters   = QVBoxLayout()


        groupBox_plotParameters.setObjectName("groupBox_blackText")
        groupBox_plotParameters.setLayout(self.layout_plotParameters)

        # Base

        self.layout_plotParameters.addWidget(self.title_base)
        self.layout_plotParameters.addWidget(self.label_base)

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

        self.layout_plotParameters.addWidget(groupBox_viewingAngle)

        # self.layout().addWidget(groupBox_viewingAngle)


    # Controls that relate to;
    #
    #   - playback direction and control

    def setup_group_box_playback_controls(self) :

        self.title_playbackDirection      = "Playback direction :"

        self.layout_playbackDirection.addWidget(self.radioButton_playForward,  alignment=Qt.AlignmentFlag.AlignLeft)
        self.layout_playbackDirection.addWidget(self.radioButton_playBackward, alignment=Qt.AlignmentFlag.AlignLeft)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)  # Set the frame shape to a horizontal line
        line.setFrameShadow(QFrame.Shadow.Sunken)  # Set the shadow effect

        self.layout_playbackControl.addWidget(self.groupBox_playbackDirection)

        self.layout().addWidget(self.groupBox_playbackControl)


    def setup_group_box_frame_delay(self) :

        # layout_playbackControl.addWidget(self.pushButton_backward, alignment=Qt.AlignmentFlag.AlignHCenter)
        # layout_playbackControl.addWidget(self.pushButton_forward, alignment=Qt.AlignmentFlag.AlignHCenter)

        # self.layout_frameDelay.addWidget(self.delayFrameLabel)
        self.layout_frameDelay.addWidget(self.delayFrame)

        # self.layout_playbackControl.addWidget(self.pushButton_playStop)

        self.layout_playbackControl.addWidget(QLabel(self.title_frameDelay))
        self.layout_playbackControl.addWidget(self.delayFrame)


    def setup_group_box_window_dimensions(self) :

        self.layout().addWidget(self.groupBox_windowDimensions)


    def setupEventHandlers_buttons(self):

        # self.pushButton_forward.clicked.connect(self.playAnimationForward)
        # self.pushButton_backward.clicked.connect(self.playAnimationBackward)

        # self.pushButton_playStop.clicked.connect(self.toggleEventPlayAnimationLoop)

        # self.pushButton_shutdown.clicked.connect(self.shutdownAnimationThread)

        # self.pushButton_exit.clicked.connect(self.window_main.close)

        pass


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

        self.setStyleSheet("""
            QGroupBox {
                background-color: lightgray;
            }
            
            QFrame {
                background-color: lightgray;
            }
            
            QPushButton {
                background-color: lightgray;
            }
            
            QLabel#label_whiteBackground {
                background-color: white;
            }
            
            QSpinBox {
                qproperty-alignment: AlignRight;
            }
        """)


    @Slot(str, str, str)
    def slot_svg_metadata_updated(self, base, azimuth, elevation):

        nameMethod = self.__class__.__name__ + \
                     "::__signal_svg_metadata_updated"


        if self.debug :

            print(nameMethod + " : Enter")

            # This function is the slot that runs when the signal is received

            print(nameMethod + " : base      = " + base)
            print(nameMethod + " : azimuth   = " + azimuth)
            print(nameMethod + " : elevation = " + elevation)

        self.label_base.setText(base)

        if self.debug:

            print(nameMethod + " : Exit")


    @Slot(str, str)
    def slot_eventResize(self, width_window_main, height_window_main) :

        nameMethod = self.__class__.__name__ + \
                     "::slot_eventResize"


        print(nameMethod + " : Enter")

        print(nameMethod + " : (width, height) = (" + width_window_main + ", " + height_window_main + ")")

        self.label_value_windowDimensions_width.setText(width_window_main)
        self.label_value_windowDimensions_height.setText(height_window_main)

        print(nameMethod + " : Exit")


    @Slot()
    def slot_debug_toggle(self):

        nameMethod = self.__class__.__name__ + \
                     "::slot_debug_toggle"


        print(nameMethod + " : &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        print(nameMethod + " : &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        print(nameMethod + " : &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        print(nameMethod + " : &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        print(nameMethod + " : &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        print(nameMethod + " : &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        print(nameMethod + " : Enter")
        print(nameMethod + " : &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        print(nameMethod + " : &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        print(nameMethod + " : &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        print(nameMethod + " : &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        print(nameMethod + " : &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        print(nameMethod + " : &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")

        if not self.debug :

            self.debug = True

        else :

            self.debug = False

        print(nameMethod + " : Exit")


    @Slot()
    def __slot_remove_button_from_layout(self):

        nameMethod = self.__class__.__name__ + \
                     "::__slot_remove_button_from_layout"


        print(nameMethod + " : Enter")

        self.layout().removeWidget(self.pushButton_remove)
        self.pushButton_remove.setParent(None)
        # self.update()

        print(nameMethod + " : Exit")