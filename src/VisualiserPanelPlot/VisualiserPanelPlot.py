from PySide6.QtCore             import (Qt,
                                        QRectF,
                                        Slot)
from PySide6.QtWidgets          import (QWidget,
                                        QFrame,
                                        QSizePolicy,
                                        QVBoxLayout)
from PySide6.QtGui              import  QPainter
from PySide6.QtWebEngineCore    import  QWebEngineSettings
from PySide6.QtWebEngineWidgets import  QWebEngineView
from PySide6.QtSvgWidgets       import  QSvgWidget

from SvgMetadataReader.SvgMetadataReader import SvgMetadataReader


class CenteredSvgWidget(QSvgWidget) :

    def paintEvent(self, event) :

        painter = QPainter(self)

        if not self.renderer().isValid():
            return

        view_box = self.renderer().viewBoxF()
        widget_rect = QRectF(self.rect())

        scaled = view_box
        scaled.scale(widget_rect.size(), Qt.KeepAspectRatio)

        x = (widget_rect.width() - scaled.width()) / 2
        y = (widget_rect.height() - scaled.height()) / 2
        target = QRectF(x, y, scaled.width(), scaled.height())

        self.renderer().render(painter, target)


class CenteredSvgWidget_New(QSvgWidget) :

    def paintEvent(self, event):

        nameMethod = self.__class__.__name__ + \
                     "::paintEvent"


        print(nameMethod + " : Enter")

        width  = self.width()
        height = self.height()

        print(nameMethod + " : SVG image onscreen width  = " + str(width))
        print(nameMethod + " : SVG image onscreen height = " + str(height))

        # renderer =

        default_size = self.renderer().defaultSize()

        print(nameMethod + " : SVG image file width  = " + str(default_size.width()))
        print(nameMethod + " : SVG image file height = " + str(default_size.height()))

        painter = QPainter(self)

        renderer = self.renderer()

        if not renderer.isValid():
            return

        view_box = renderer.viewBoxF()
        widget_rect = QRectF(self.rect())

        scale = min(widget_rect.width() / view_box.width(),
                    widget_rect.height() / view_box.height())

        new_width = view_box.width() * scale
        new_height = view_box.height() * scale

        x = (widget_rect.width() - new_width) / 2
        y = (widget_rect.height() - new_height) / 2

        target = QRectF(x, y, new_width, new_height)
        renderer.render(painter, target)

        print(nameMethod + " : Exit")


class AspectRatioSvgWidget(CenteredSvgWidget_New) :

    def resizeEvent(self, event) :

        renderer = self.renderer()

        if not renderer.isValid():
            return super().resizeEvent(event)

        view_box = renderer.viewBoxF()
        widget_w = self.width()
        widget_h = self.height()

        scale = min(widget_w / view_box.width(),
                    widget_h / view_box.height())

        new_w = int(view_box.width() * scale)
        new_h = int(view_box.height() * scale)

        self.setFixedSize(new_w, new_h)



class VisualiserPanelPlot(QFrame) :

    """
    Display a plot and its title.

    The panel consists of:

    - A title rendered either using MathJax or a PNG image.
    - A plot view displaying an SVG image rendered as a pixmap.
    - Metadata extraction from SVG files.

    The widget uses a vertical layout containing:
        1. Plot title view
        2. Plot display label
    """

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
        self.__create_and_configure_layout()
        self.__create_signal_connections()

        # Perform various configuration tasks.

        self.__configure()

        # Initialise child widgets.

        self._is_initialised = True


    # Invoked from : __init__

    def __setup_settings(self) :

        self.filename_plot                 = "/home/craig/source_code/python/visualiser_8_Feb_2026/svg/Eulers_formula_(45,8).svg"
        self.plot_title_use_png_or_mathjax = "mathjax"


    # Invoked from : __init__

    def __create_widgets(self) :

        self.plot_title           = QWebEngineView()
        self.image                = QSvgWidget()


    # Invoked from : __init__

    def __create_objects(self) :

        self.svgMetadataReader = SvgMetadataReader()


    # Invoked from : initialise

    def __create_actions(self) :

        pass


    # Invoked from : initialise

    def __create_menus(self) :

        pass


    # Invoked from : initialise

    def __create_toolbars(self) :

        pass


    # Invoked from : initialise

    def __create_and_configure_layout(self) :

        # Create a layout for this widget, i.e. self, and force this widget
        # to use it.

        layout = QVBoxLayout()

        self.setLayout(layout)

        self.plot_title.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.image.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Tell the layout not to expand self.plot_title, but instead, to give
        # all of the extra space to self.image.

        container = QWidget()

        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.addStretch()
        container_layout.addWidget(self.image, alignment=Qt.AlignCenter)
        container_layout.addStretch()

        layout.addWidget(self.plot_title)
        layout.addWidget(container, stretch=20)

        self.__setup_panel_plotTitle()
        self.__setup_panel_plotView()


    # Invoked from : initialise

    def __create_signal_connections(self) :

        # Perform various configuration tasks.

        pass


    # Invoked from : initialise

    def __configure(self) :

        pass


    def __setup_panel_plotTitle(self) :

        if self.plot_title_use_png_or_mathjax == "mathjax" :

            self.__setup_panel_plotTitle_usingMathJax()

        if self.plot_title_use_png_or_mathjax == "png":

            self.__setup_panel_plotTitle_usingPngFile()


    def __setup_panel_plotTitle_usingMathJax(self):

        nameMethod = "Visualiser_Panel_Plot::createAndConfigure_guiComponents_panel_plot"


        print(nameMethod + " : Enter")

        # file_path = os.path.abspath("plot_title_basic.html")
        # local_url = QUrl.fromLocalFile(file_path)

        with open("/home/craig/source_code/python/visualiser/html/mathjax.html", "r") as file_handle :

            html_mathjax = file_handle.read()

        print(nameMethod + " : ##################################################")
        print(nameMethod + " : ##################################################")
        print(nameMethod + " : html_mathjax = " + html_mathjax)
        print(nameMethod + " : ##################################################")
        print(nameMethod + " : ##################################################")

        # self.plot_title.load(local_url)
        # self.plot_title.setUrl(QUrl.fromLocalFile("/home/craig/source_code/python/Visualiser_EulersFormula/plot_title_basic.html"))
        self.plot_title.setHtml(html_mathjax)

        self.plot_title.settings().setAttribute \
                (
                QWebEngineSettings.WebAttribute.ShowScrollBars,
                False
            )


    def __setup_panel_plotView(self) :

        nameMethod = "Visualiser_Panel_Plot::setup_panel_plotView"


        print(nameMethod + " : Enter")

        self.slot_update_panel_plotView(self.filename_plot)

        print(nameMethod + " : Exit")


    def __setup_panel_plotTitle_usingPngFile(self) :

        # TODO : This panel should be enclosed in a QFrame.

        # self.label_plot_title.setObjectName("./labelNoBorderWhiteBackground")
        self.label_plot_title.setObjectName("./labelNoBorder")

        # Associate a pixmap with the file.

        pixmapTitle = QPixmap(self.filename_titlePlot)

        self.label_plot_title.setPixmap(pixmapTitle)
        self.label_plot_title.setScaledContents(True)


    @Slot(str)
    def slot_update_panel_plotView(self, filename) :

        nameMethod = "MainWindow::slot_update_panel_plotView"


        print(nameMethod + " : Enter")
        print(nameMethod + " : Arg filename = " + filename)

        # Get the metadata from the image file.

        self.parameters = self.svgMetadataReader.get_parameters_from_file(filename)
        self.svgMetadataReader.print_plot_parameters()

        # Open the image file and then load it into the panel_plotView

        self.image.load(filename)

        # if self.image is None :

        #     print(nameMethod + " : self.image = None")

        # else :

        #     print(nameMethod + " : self.image = " + self.image)

        # Get the width, height, and size of the label.

        if False :

            imageScaled = self.image.scaled(sizeLabelImage,
                                            Qt.AspectRatioMode.KeepAspectRatio,
                                            Qt.TransformationMode.SmoothTransformation)

            self.label_panel_plotView.setPixmap(imageScaled)
            self.label_panel_plotView.setScaledContents(True)

        # I don't think the following line of code is necessary.

        # self.label_panel_plotView.update()

        # TODO : Uncomment this when ready.

        # self.update_panel_side()

        print(nameMethod + " : Exit")


    @Slot(str, str, str)
    def slot_svg_metadata_updated(self, base, azimuth, elevation) :

        nameMethod = self.__class__.__name__ + \
                     "::signal_svg_metadata_updated"


        print(nameMethod + " : Enter")

        print(nameMethod + " : base      = " + base)
        print(nameMethod + " : azimuth   = " + azimuth)
        print(nameMethod + " : elevation = " + elevation)

        print(nameMethod + " : Exit")
