import sys
import threading
import time
import re

from pathlib import Path

from PyQt6.QtCore       import Qt
from PyQt6.QtWidgets    import QApplication, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QGraphicsEllipseItem, \
                               QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QFrame, QSpinBox,         \
                               QGroupBox, QRadioButton, QButtonGroup
from PyQt6.QtGui        import QBrush, QPen, QColor, QPixmap, QAction
from PyQt6.QtSvgWidgets import QGraphicsSvgItem

from ZoomableGraphicsView import ZoomableGraphicsView


useCustomStylesheet = False


class MainWindow(QMainWindow):

    #
    # __init__ : (Class constructor)
    #   |
    #   |- self.createAndConfigureGuiComponents
    #   |    |- self.createAndConfigureGuiComponents_sidePanel
    #   |    |- self.createAndConfigureGuiComponents_viewPanel
    #   |
    #   |- self.setupWindow_main
    #   |    |- self.setupMenubar
    #   |    |- self.setupPanel_side
    #   |    |    |- self.setupPanel_plotParameters()
    #   |    |    |- self.setupPanel_viewingAngle()
    #   |    |    |- self.setupPanel_playbackControls()
    #   |    |    |- self.setupEventHandlers_buttons
    #   |    |- self.setupWindow_plot
    #   |    |    |- self.setupWindow_plot_title
    #   |    |    |- self.setupPlotWindow_view
    #   |
    #   |- self.configureMainWindow
    #
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    #
    # Animation thread
    # ================
    #
    # __main__
    #   |- self.startAnimationLoopInOwnThread
    #        |- self.startAnimationLoop
    #             |- self.playFramesForward | self.playFramesBackward
    #                  |- self.updateImageViewer



    def __init__(self, ctorNumber):

        super().__init__()

        # Set various settings.

        self.setSettings()

        # Create and configure;
        #
        #   - GUI components
        #   - threading components

        self.createAndConfigureGuiComponents()
        self.createAndConfigureThreadingComponents()

        # Setup the GUI main window.

        self.setupWindow_main()

        # Clear threading events.

        self.clearThreadingEvents()

        self.configureMainWindow()


    def setSettings(self) :

        self.titleWindow = "Visualizer for Euler's formula"

        self.title_plotParameters         = "Plot parameters :"
        self.title_viewingAngle           = "Viewing angle :"
        self.title_viewingAngle_elevation = "Elevation"
        self.title_viewingAngle_azimuth   = "Azimuth"

        self.title_playbackControl        = "Playback controls :"

        self.playAnimationInSeparateThread    = True
        self.grabScreenshots                  = False
        self.useLayoutSimuLab                 = False
        self.playForward                      = True

        # Delay between frames in seconds, i.e. 50ms

        self.delayBetweenFrames = 0.05
        self.filename_titlePlot = "./Plot_label.png"
        self.filename_plot      = "./svg/Eulers_formula_(45,0).svg"


    def createAndConfigureGuiComponents(self) :

        self.createAndConfigureGuiComponents_menubar()

        self.createAndConfigureGuiComponents_dataVisualizationPanel()


    def createAndConfigureGuiComponents_menubar(self) :

        # Remember that the menuBar is provided by QMainWindow object.

        self.menubar = self.menuBar()

        self.exitAction = QAction('&Exit', self)
        self.newAction = QAction("&New", self)


    def createAndConfigureGuiComponents_dataVisualizationPanel(self) :

        self.createAndConfigureGuiComponents_sidePanel()
        self.createAndConfigureGuiComponents_viewPanel()


    def createAndConfigureGuiComponents_sidePanel(self) :

        # Central widget and its layout

        self.centralWidget       = QFrame()
        self.centralWidgetLayout = QHBoxLayout()

        # View angle components

        self.label_playback = QLabel("Playback")

        self.viewAngleElevLabel = QLabel(self.title_viewingAngle_elevation)
        self.elevationLabel     = QLabel("45\u00B0")
        self.viewAngleAzimLabel = QLabel(self.title_viewingAngle_azimuth)
        self.azimuthLabel       = QLabel("0\u00B0")

        self.base               = QLabel("Base")
        self.baseLabel          = QLabel("2.718")

        self.delayFrameLabel    = QLabel("Frame delay (in ms)")
        self.delayFrame         = QSpinBox()
        self.delayFrame.setRange(10, 10000)  # Min = 10ms | Max = 10,000ms = 10s
        self.delayFrame.setSingleStep(10)
        self.delayFrame.setValue(50)

        self.delayFrameLabel.setObjectName("labelNoBorder")
        self.delayFrame.setObjectName("spinBox")

        self.label_playback.setObjectName("labelNoBorder")

        self.viewAngleElevLabel.setObjectName("labelNoBorder")
        self.viewAngleAzimLabel.setObjectName("labelNoBorder")

        self.elevationLabel.setObjectName("labelWithBorder")
        self.azimuthLabel.setObjectName("labelWithBorder")

        self.base.setObjectName("labelNoBorder")
        self.baseLabel.setObjectName("labelWithBorder")

        self.viewAngleElevLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.elevationLabel.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.azimuthLabel.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.baseLabel.setAlignment(Qt.AlignmentFlag.AlignRight)

        # Play direction components

        self.labelPlayDirection = QLabel("Current direction")
        self.labelPlayDirection.setObjectName("labelNoBorder")

        self.labelCurrentPlayDirection = QLabel("Forward")
        self.labelCurrentPlayDirection.setObjectName("labelWithBorder")
        self.labelCurrentPlayDirection.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.pushButton_backward = QPushButton("<")
        self.pushButton_forward  = QPushButton(">")

        # Play/Stop button

        self.pushButton_playStop = QPushButton("Play")

        # Other coomponents

        self.pushButton_shutdown = QPushButton("Shutdown")
        self.pushButton_exit     = QPushButton("Exit")

        self.pushButton_forward.setToolTip("Name : self.pushButton_forward\n"
                                           "Connects to the method : MainWindow::playAnimationForward")
        self.pushButton_backward.setToolTip("Name : self.pushButton_backward\n"
                                            "Connects to the method : MainWindow::playAnimationBackward")

        self.pushButton_exit.setToolTip("Name : self.pushButton_exit\n"
                                        "Connects to the method : MainWindow::shutdownRoutine")

        self.pushButton_playStop.setToolTip("Connects to the method : MainWindow::toggleEventAnimationLoop")
        self.pushButton_shutdown.setToolTip("Connects to the method : MainWindow::shutdownAnimationThread")


    def createAndConfigureGuiComponents_viewPanel(self) :

        # Labels to hold;
        #
        #   - the title of the image
        #   - the image

        self.labelTitleImage = QLabel()
        self.labelImage      = QLabel()
        self.image           = QPixmap()


    def createAndConfigureThreadingComponents(self) :

        # Create threading events that will be used by the animation thread.

        self.event_playAnimationLoop    = threading.Event()
        self.eventShutdownAnimationLoop = threading.Event()


    def clearThreadingEvents(self) :

        self.event_playAnimationLoop.clear()
        self.eventShutdownAnimationLoop.clear()


    """ Create a new thread of execution and start the play loop running in it.

        :param NA

        :returns: NA

        :rtype: NA

        Invoked by : __main__

        Create the vertically oriented side panel then add a number of buttons and labels to
        it. Once this has been done, configure the buttons and labels.
    """

    def startAnimationLoopInOwnThread(self) :

        if self.playAnimationInSeparateThread :

            # Create a new thread to run the play loop in.

            self.threadAnimationLoop = threading.Thread(target=self.startAnimationLoop, args=())

            # Start this new thread running.

            self.threadAnimationLoop.start()

        else :

            self.event_playAnimationLoop.set()

            self.startAnimationLoop()


    """ Run a loop which plays the frames. 

        :param NA

        :returns: NA

        :rtype: NA

        Invoked by : startAnimationLoopInOwnThread

        Run a loop which plays the frames.
    """

    def startAnimationLoop(self) :

        nameMethod = "MainWindow::startAnimationLoop"


        self.counter  = 0

        print(nameMethod, " : Enter")

        # Continue to execute this loop under 2 conditions;
        #
        #   - the counter is <= 360
        #   - the specified event still gives us permission to proceed.

        print(nameMethod, " : self.event_playAnimationLoop         = ", self.event_playAnimationLoop.is_set())
        print(nameMethod, " : self.eventShutdownAnimationLoop = ", self.eventShutdownAnimationLoop.is_set())

        try :

            print(nameMethod, "Waiting to get the go ahead from event : eventPlayAnimationLoop")

            # TODO : Maybe use a threading queue here.

            while self.event_playAnimationLoop.wait() :

                # What caused us to proceed?
                #
                #   - self.event_playAnimationLoop
                #
                #       or
                #
                #   - self.eventShutdownAnimationLoop

                if self.eventShutdownAnimationLoop.is_set() :

                    raise Exception("Received a request to shutdown the animation loop thread.")

                # not (self.eventShutdownAnimationLoop.wait()) :

                print("Have started another iteration of the innermost while loop.")

                if self.playForward :

                    self.playFramesForward()

                else :

                    self.playFramesBackward()

                # End of if statement.

                # Don't clear the run loop event as the animation may have been
                # stopped part way through and then had its direction changed.

            # End of while loop : wait on both loop events

        except Exception :

            print(nameMethod, " : Caught an exception")

        print(nameMethod, " : Exit")


    def playFramesForward(self) :

        nameMethod = "MainWindow::playFramesForward"

        exitLoop = False

        # Play the frames forward.

        if (self.counter < 0) or (self.counter > 360):

            self.counter = 0

        while (self.playForward == True) and \
              (self.counter <= 360) and \
              (self.event_playAnimationLoop.wait()) :

              # not (self.eventShutdownAnimationLoop.wait()):

            print(nameMethod, " : Play forward")

            print(nameMethod, " : Counter = ", self.counter)

            # Wait a certain amount of time, then display the next image.

            print(nameMethod, " : Sleep delay in ms = ", self.delayFrame.value() * 0.001)

            time.sleep(self.delayFrame.value() * 0.001)
            self.updateImageViewer(45, self.counter)

            # Check to see if we should we save an image of the main window at this point.

            if self.grabScreenshots :

                try:

                    # Create a new thread to perform the screen capture task.

                    self.thread_grabAndSaveScreenshot = threading.Thread(target=self.grabAndSaveScreenshot, args=())

                    # Start this new thread running.

                    self.thread_grabAndSaveScreenshot.start()

                    self.thread_grabAndSaveScreenshot.join()

                except Exception as e:

                    print("Exception caught : ", str(e))

            self.counter = self.counter + 1

            print(nameMethod, " : Counter = ", self.counter)

            if self.eventShutdownAnimationLoop.is_set() :

                # We need to terminate this thread of execution.

                raise Exception("Received a request to shutdown the animation loop thread.")

        # End of while loop : 3 conditions

        print(nameMethod, "Have exited counter based while loop : <= 360")

        self.pushButton_playStop.setText("Play")
        self.pushButton_playStop.update()

        # Clear the run event.

        if self.counter > 360 :

            print("About to clear the run event.")

            self.event_playAnimationLoop.clear()

        print("About to exit out of the clause : if playForward")


    def playFramesBackward(self) :

        # Play the animation backward.

        if (self.counter < 0) or (self.counter > 360) :

            self.counter = 360

        while (self.playForward == False) and \
              (self.counter >= 0)              and \
              (self.event_playAnimationLoop.wait()) and \
              not (self.eventShutdownAnimationLoop.wait()) :

            print("MainWindow::startTimer : Play backward")

            print("Counter = ", counter)

            # Wait a certain amount of time, then display the next image.

            time.sleep(self.delayBetweenFrames)
            self.updateImageViewer(45, counter)

            self.counter = self.counter - 1

            print("Counter = ", counter)

        # End of counter based while loop.

        print("End of counter based while loop.")

        self.pushButton_playStop.setText("Play")
        self.pushButton_playStop.update()

        print("About to exit out of the clause : else playForward")


    def grabAndSaveScreenshot(self) :

        nameMethod = "MainWindow::grabAndSaveScreenshot"


        print(nameMethod, " : Enter")

        screenshot = self.grab()

        counterFormatted = "{:0{}d}".format(self.counter, 3)

        screenshot.save("screenshot_" + str(counterFormatted) + ".png")

        print(nameMethod, " : Exit")


    """ Configure the GUI's main window. 

        :param NA

        :returns: NA

        :rtype: NA

        Invoked by : The class constructor. 

        Resize the main window and set its title.
    """

    def configureMainWindow(self) :

        self.resize(500, 500)
        # self.setGeometry(100, 100, 300, 200)  # x, y, width, height
        self.setWindowTitle(self.titleWindow)


    """ Setup the layout for the main window. 

        :param NA

        :returns: NA

        :rtype: NA

        Invoked by : The class constructor. 

        Set the central widget for the main window and set the layout for the
        central widget. Once this is done, setup the top-level components of the
        main window. 
    """

    def setupWindow_main(self) :

        # Set the central widget for the main window and set the layout for the
        # central widget.

        self.setCentralWidget(self.centralWidget)
        self.centralWidget.setLayout(self.centralWidgetLayout)

        # Setup the top-level components of the main window.

        self.setupMenubar()

        self.setupDataVisualizationWindow()


    def setupMenubar(self) :

        # Add menus to the main window's menu bar.

        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.triggered.connect(self.shutdownRoutine)

        self.newAction.setShortcut("Ctrl+N")
        self.newAction.triggered.connect(self.newFile)

        self.fileMenu = self.menubar.addMenu('&File')
        self.helpMenu = self.menubar.addMenu('&Help')

        self.fileMenu.addAction(self.newAction)
        self.fileMenu.addAction(self.exitAction)


    # Invoked by : setupMainWindow

    def setupDataVisualizationWindow(self):

        self.setupPanel_side()
        self.setupWindow_plot()


    def shutdownRoutine(self) :

        nameMethod = "MainWindow::shutdownRoutine"


        print(nameMethod, " : ========================================")
        print(nameMethod, " : Enter")
        print(nameMethod, " : ========================================")

        # Inform the play loop thread that it should shutdown.

        self.eventShutdownAnimationLoop.set()
        self.event_playAnimationLoop.set()

        # Wait for the play loop thread to finalise its tasks and shutdown.

        print(nameMethod, " : Waiting to join with the animation thread")

        # Check that the animation loop thread is actually running. It should be, as
        # it is started directly from __main__.

        print(nameMethod, " : Animation loop thread = ", self.threadAnimationLoop)

        self.threadAnimationLoop.join()

        self.close()

        print(nameMethod, " : Exit")


    """ Setup the side panel.

        :param NA

        :returns: NA

        :rtype: NA

        Invoked by : setupDataVisualizationWindow
        
        Create the vertically oriented side panel then add a number of buttons and labels to
        it. Once this has been done, configure the buttons and labels.
    """

    def setupPanel_side(self) :

        self.layout_sidePanel = QVBoxLayout()


        # Add the necessary group boxes to the side panel.

        self.setupPanel_plotParameters()
        self.setupPanel_viewingAngle()
        self.setupPanel_playbackControls()

        # Add the Play and Exit buttons to the side panel.

        self.layout_sidePanel.addStretch(1)
        self.layout_sidePanel.addWidget(self.pushButton_playStop, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.layout_sidePanel.addStretch(1)
        self.layout_sidePanel.addWidget(self.pushButton_exit,     alignment=Qt.AlignmentFlag.AlignHCenter)

        # pushButton_forward.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # pushButton_backward.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.centralWidgetLayout.addLayout(self.layout_sidePanel)

        # Setup button event handlers.

        self.setupEventHandlers_buttons()


    # Controls that relate to;
    #
    #   - plot parameters

    def setupPanel_plotParameters(self) :

        groupBox_plotParameters = QGroupBox(self.title_plotParameters)
        layout_plotParameters = QVBoxLayout()


        groupBox_plotParameters.setObjectName("groupBox_blackText")
        groupBox_plotParameters.setLayout(layout_plotParameters)

        layout_plotParameters.addWidget(self.base)
        layout_plotParameters.addWidget(self.baseLabel)

        self.layout_sidePanel.addWidget(groupBox_plotParameters)


    def setupPanel_viewingAngle(self):

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

        self.layout_sidePanel.addWidget(groupBox_viewingAngle)


    # Controls that relate to;
    #
    #   - playback direction and control

    def setupPanel_playbackControls(self) :

        groupBox_playbackControl = QGroupBox(self.title_playbackControl)
        layout_playbackControl   = QVBoxLayout()


        groupBox_playbackControl.setObjectName("groupBox_blackText")
        groupBox_playbackControl.setLayout(layout_playbackControl)

        # layout_playbackControl.addWidget(self.labelPlayDirection)
        # layout_playbackControl.addWidget(self.labelCurrentPlayDirection)

        radioButton_playForward  = QRadioButton("Forward")
        radioButton_playBackward = QRadioButton("Backward")

        radioButton_playForward.setChecked(True)
        radioButton_playBackward.setChecked(False)

        radioButtonGroup = QButtonGroup()

        layout_playbackControl.addWidget(radioButton_playForward,  alignment=Qt.AlignmentFlag.AlignLeft)
        layout_playbackControl.addWidget(radioButton_playBackward, alignment=Qt.AlignmentFlag.AlignLeft)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)  # Set the frame shape to a horizontal line
        line.setFrameShadow(QFrame.Shadow.Sunken)  # Set the shadow effect

        layout_playbackControl.addWidget(line)

        # layout_playbackControl.addWidget(self.pushButton_backward, alignment=Qt.AlignmentFlag.AlignHCenter)
        # layout_playbackControl.addWidget(self.pushButton_forward, alignment=Qt.AlignmentFlag.AlignHCenter)

        layout_playbackControl.addWidget(self.delayFrameLabel)
        layout_playbackControl.addWidget(self.delayFrame)

        self.layout_sidePanel.addWidget(groupBox_playbackControl)


    def setupEventHandlers_buttons(self) :

        self.pushButton_forward.clicked.connect(self.playAnimationForward)
        self.pushButton_backward.clicked.connect(self.playAnimationBackward)

        self.pushButton_playStop.clicked.connect(self.toggleEventPlayAnimationLoop)

        self.pushButton_shutdown.clicked.connect(self.shutdownAnimationThread)

        self.pushButton_exit.clicked.connect(self.shutdownRoutine)


    def shutdownAnimationThread(self) :

        nameMethod = "MainWindow::shutdownAnimationThread"


        print(nameMethod, " : Enter")

        print(nameMethod, " : Event status was = ", self.eventShutdownAnimationLoop.is_set())

        if self.eventShutdownAnimationLoop.is_set() :

            self.eventShutdownAnimationLoop.clear()

        else :

            self.eventShutdownAnimationLoop.set()

        print(nameMethod, " : Event status now = ", self.eventShutdownAnimationLoop.is_set())

        print(nameMethod, " : Exit")


    """ Update settings that pertain to playing tha animation backward.

        :param NA

        :returns: NA

        :rtype: NA
        
        Invoked by : pushButton_backward.clicked()
        
        Set the play backward flag to true and update the play direction label accordingly.
    """

    def playAnimationBackward(self):

        print("MyMainWindow::playAnimationBackward : Enter")

        self.playForward = False
        self.labelCurrentPlayDirection.setText("Backward")

        print("MyMainWindow::playAnimationBackward : Exit")


    """ Update settings that pertain to playing tha animation forward.

        :param NA

        :returns: NA

        :rtype: NA

        Invoked by : pushButton_forward.clicked()
        
        Set the play forward flag to true and update the play direction label accordingly.  
    """

    def playAnimationForward(self):

        print("MyMainWindow::playAnimationForward : Enter")

        self.playForward = True
        self.labelCurrentPlayDirection.setText("Forward")

        print("MyMainWindow::playAnimationForward : Exit")


    """ Toggle the event which instructs the play loop to start or stop.

        :param NA

        :returns: NA

        :rtype: NA

        Invoked by : pushButton_playStop.clicked
    """

    def toggleEventPlayAnimationLoop(self) :

        nameMethod = "MainWindow::toggleEventPlayAnimationLoop"


        print(nameMethod, " : Enter")

        print(nameMethod, "self.event_playAnimationLoop was = ", self.event_playAnimationLoop.is_set())

        if self.event_playAnimationLoop.is_set() :

            # The infinite event loop currently has permission to run.
            #
            # Revoke this permission and set the button label to "Play".

            self.event_playAnimationLoop.clear()
            self.pushButton_playStop.setText("Play")

        else :

            # The infinite event loop doesn't currently have permission to run.
            #
            # Reinstate this permission and set the button label to "Stop".

            self.event_playAnimationLoop.set()
            self.pushButton_playStop.setText("Stop")

        print(nameMethod, "self.event_playAnimationLoop now = ", self.event_playAnimationLoop.is_set())

        # Instruct self.pushButton_playStop to update itself.

        self.pushButton_playStop.update()

        print(nameMethod, " : Exit")


    def createAndPopulateScene(self):

        # Create a scene and a view to go with it.

        # self.createScene()

        sceneTitle = GraphicsScene()
        viewTitle  = GraphicsView(sceneTitle)

        scene = QGraphicsScene()
        # scene.setSceneRect(0, 0, 300, 200)  # Define scene boundaries
        view = ZoomableGraphicsView(scene)

        layoutSceneAndTitle.addWidget(viewTitle)
        layoutSceneAndTitle.addWidget(view)

        self.centralWidgetLayout.addWidget(view)
        # self.centralWidgetLayout.addWidget(frameSceneAndTitle)

        # Open an SVG file and add its image to the scene.

        svg_item = QGraphicsSvgItem("./svg/rectangle.svg")
        svg_item.setFlag(QGraphicsSvgItem.ItemIsMovable)

        scene.addItem(svg_item)

        # Open another SVG file and add its image to the scene as well.

        svg_item = QGraphicsSvgItem("./svg/circle.svg")
        svg_item.setFlag(QGraphicsSvgItem.ItemIsMovable)

        scene.addItem(svg_item)

        if False :

            # Create an image of a rectangle and add it to the scene.

            rect = QGraphicsRectItem(50, 50, 100, 50)
            rect.setBrush(QBrush(QColor("red")))
            rect.setPen(QPen(Qt.black, 2))
            rect.setFlag(QGraphicsRectItem.ItemIsMovable)  # Make it movable

            scene.addItem(rect)

            # Create an image of a circle and add it to the scene.

            ellipse = QGraphicsEllipseItem(180, 70, 80, 80)
            ellipse.setBrush(QBrush(QColor("blue")))
            ellipse.setPen(QPen(Qt.black, 2))

            scene.addItem(ellipse)


    def setupWindow_plot(self) :

        self.setupWindow_plot_title()
        self.setupPlotWindow_view()

        frameTitleAndScene  = QFrame()
        layoutTitleAndScene = QVBoxLayout()

        frameTitleAndScene.setLayout(layoutTitleAndScene)

        layoutTitleAndScene.addWidget(self.labelTitleImage)
        # layoutTitleAndScene.addWidget(labelSpacer)
        layoutTitleAndScene.addWidget(self.labelImage)

        self.centralWidgetLayout.addWidget(frameTitleAndScene)


    def setupWindow_plot_title(self) :

        # self.labelTitleImage.setObjectName("./labelNoBorderWhiteBackground")
        self.labelTitleImage.setObjectName("./labelNoBorder")

        # Associate a pixmap with the file.

        pixmapTitle = QPixmap(self.filename_titlePlot)

        self.labelTitleImage.setPixmap(pixmapTitle)
        self.labelTitleImage.setScaledContents(True)


    def setupPlotWindow_view(self) :

        print("Filename = ", self.filename_plot)

        self.image.load((self.filename_plot))

        # Get the current

        widthLabelImage  = self.labelImage.width()
        heightLabelImage = self.labelImage.height()

        sizeLabelImage = self.labelImage.size()

        print("Image label width  = ", widthLabelImage)
        print("Image label height = ", heightLabelImage)

        imageScaled = self.image.scaled(sizeLabelImage,
                                        Qt.AspectRatioMode.KeepAspectRatio,
                                        Qt.TransformationMode.SmoothTransformation)

        self.labelImage.setPixmap(self.image)
        self.labelImage.setScaledContents(True)


    # Invoked by : MyMainWindow::startTimer

    def updateImageViewer(self, elevation, counter) :

        print("MainWindow::updateImageViewer : Enter")

        filename = "./svg/Eulers_formula_(45," + str(counter) + ").svg"
        print("Filename = ", filename)

        # It seems you can't just load a new image into the QPixmap. You need to reload the QPixmap into the QLabel
        # before you update it.

        self.image = QPixmap(filename)
        self.labelImage.setPixmap(self.image)

        self.labelImage.update()

        # Update the elevation and azimuth fields as well.

        self.elevationLabel.setText("45\u00B0")
        self.azimuthLabel.setText(str(counter) + "\u00B0")

        print("MainWindow::updateImageViewer : Exit")


    def createScene(self) :

        print("MainWindow::createScene : Enter")


    def newFile(self):

        print("New File action triggered!")


    def on_button_click(self) :

        print("Button was clicked")


    def ctor_0(self):

        super().__init__()

        # Create a QPushButton and add it to the layout.

        pushButton_1 = QPushButton("Button 1")
        self.centralWidgetLayout.addWidget(pushButton_1)


    def ctor_1(self) :

        if False :

            super().__init__()


            # Display the scene using a QGraphicsView object.

            self.view = QGraphicsView(self.scene)

            # self.setCentralWidget(self.scene)

            self.view.setWindowTitle("PyQt QGraphicsScene Example")
            self.view.resize(400, 300)
            self.view.show()

            # app.exec_()


if __name__ == "__main__" :

    count_commandLineArgs = len(sys.argv)


    try :

        # Check if any command line args have been passed to this program.

        print("Number of command line args  = ", count_commandLineArgs)

        if count_commandLineArgs == 2 :

            # Assume that the command line arg which was passed in at position 1, is the name of a file to load.

            print("Name of file to load = ", sys.argv[1])

            file_path = Path(sys.argv[1])

            if not file_path.is_file() :

                raise Exception("Specified file doesn't seem to exist.")

            # Continue on as specified file appears to exist.

        app = QApplication(sys.argv)

        # Check if this program should be using a custom stylesheet.

        if useCustomStylesheet :

            try:

                with open("StylesheetCraig.qss", "r") as file:

                    app.setStyleSheet(file.read())

            except FileNotFoundError :

                print("Stylesheet file 'StylesheetCraig.qss' not found.")

        window = MainWindow(0)
        window.show()

        # Create a new thread to run the animation loop in.

        window.startAnimationLoopInOwnThread()

        # Start the GUI running.

        sys.exit(app.exec())

    except Exception as e :

        print("Exception caught : ", str(e))
