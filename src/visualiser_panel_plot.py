from PySide6.QtCore             import (Qt,
                                        Slot)
from PySide6.QtWidgets          import (QFrame,
                                        QLabel,
                                        QVBoxLayout)
from PySide6.QtGui              import (QPixmap)
from PySide6.QtWebEngineCore    import  QWebEngineSettings
from PySide6.QtWebEngineWidgets import  QWebEngineView

from svg_metadata_reader        import  SvgMetadataReader


class Visualiser_Panel_Plot(QFrame) :

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

        nameMethod = "Visualiser_Panel_Plot::__init__"


        print(nameMethod + " : Enter")

        super().__init__()

        self.filename_plot                 = "/home/craig/source_code/python/Visualiser_EulersFormula/svg/Eulers_formula_(45,8).svg"
        self.plot_title_use_png_or_mathjax = "mathjax"

        # Create and set a layout for this widget.

        layout = QVBoxLayout()

        self.setLayout(layout)

        # Create the child widgets for this widget.

        self.create_child_widgets()

        layout.addWidget(self.plot_title)
        layout.addWidget(self.label_panel_plotView)
        # layout.addWidget()

        self.setup_panel_plotTitle()
        self.setup_panel_plotView()

        print(nameMethod + " : Exit")


    def create_child_widgets(self) :

        self.plot_title           = QWebEngineView()
        self.label_panel_plotView = QLabel()
        self.image                = QPixmap()

        self.svgMetadataReader    = SvgMetadataReader()


    def setup_panel_plotTitle(self) :

        if self.plot_title_use_png_or_mathjax == "mathjax" :

            self.setup_panel_plotTitle_usingMathJax()

        if self.plot_title_use_png_or_mathjax == "png":

            self.setup_panel_plotTitle_usingPngFile()


    def setup_panel_plotTitle_usingMathJax(self):

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


    def setup_panel_plotView(self) :

        nameMethod = "Visualiser_Panel_Plot::setup_panel_plotView"


        print(nameMethod + " : Enter")

        self.slot_update_panel_plotView(self.filename_plot)

        print(nameMethod + " : Exit")


    def setup_panel_plotTitle_usingPngFile(self) :

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

        self.image = QPixmap(filename)

        # if self.image is None :

        #     print(nameMethod + " : self.image = None")

        # else :

        #     print(nameMethod + " : self.image = " + self.image)

        # Get the width, height, and size of the label.

        widthLabelImage  = self.label_panel_plotView.width()
        heightLabelImage = self.label_panel_plotView.height()
        sizeLabelImage   = self.label_panel_plotView.size()

        print(nameMethod + " : Width of image  = " + str(widthLabelImage))
        print(nameMethod + " : Height of image = " + str(heightLabelImage))
        print(nameMethod + " : Size of image   = " + str(sizeLabelImage))

        imageScaled = self.image.scaled(sizeLabelImage,
                                        Qt.AspectRatioMode.KeepAspectRatio,
                                        Qt.TransformationMode.SmoothTransformation)

        self.label_panel_plotView.setPixmap(imageScaled)
        self.label_panel_plotView.setScaledContents(True)

        # I don't think the following line of code is necessary.

        # self.label_panel_plotView.update()

        print("Image label width  = ", widthLabelImage)
        print("Image label height = ", heightLabelImage)

        # TODO : Uncomment this when ready.

        # self.update_panel_side()

        print(nameMethod + " : Exit")
