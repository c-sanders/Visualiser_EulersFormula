import os
import sys

from PySide6.QtCore       import (Qt,
                                  QRectF,
                                  QSizeF,
                                  QEvent)
from PySide6.QtWidgets    import (QApplication,
                                  QMainWindow)
from PySide6.QtGui        import  QPainter
from PySide6.QtSvgWidgets import  QSvgWidget


class SvgWidget(QSvgWidget) :

    def __setup_values(self) :

        nameMethod  = self.__class__.__name__ + \
                      "::__setup_values"


        print(nameMethod + " : Enter")

        # Get the dimensions of the SVG file's coordinate system.
        #
        # Before we can do this however, we first need to get the processing/rendering object which is associated with
        # the SVG file.

        self.processor_svg_file = svg_widget.renderer()

        if not self.processor_svg_file.isValid():

            raise Exception("For whatever reason, the renderer is not valid.")

        view_box = self.processor_svg_file.viewBoxF()  # QRectF

        self.width_svg_file        = view_box.width()
        self.height_svg_file       = view_box.height()
        self.aspect_ratio_svg_file = self.width_svg_file / self.height_svg_file

        self.width_size_hint        = self.sizeHint().width()
        self.height_size_hint       = self.sizeHint().height()
        self.aspect_ratio_size_hint = self.width_size_hint / self.height_size_hint

        self.width_widget_render_area        = self.rect().width()
        self.height_widget_render_area       = self.rect().height()
        self.aspect_ratio_widget_render_area = self.width_widget_render_area / self.height_widget_render_area

        print(nameMethod + " : Exit")


    def __display_size_hint(self) :

        nameMethod  = self.__class__.__name__ + \
                      "::__display_size_hint"


        print(nameMethod + " : Enter")

        print(nameMethod + " : Size hint width        = " + str(self.width_size_hint))
        print(nameMethod + " : Size hint height       = " + str(self.height_size_hint))
        print(nameMethod + " : Size hint aspect ratio = " + str(self.aspect_ratio_size_hint))

        print(nameMethod + " : Exit")

    def __display_diagnostics_svg_file(self) :

        nameMethod  = self.__class__.__name__ + \
                      "::__display_diagnostics_svg_file"


        print(nameMethod + " : Enter")

        print(nameMethod + " : SVG file width        = " + str(self.width_svg_file))
        print(nameMethod + " : SVG file height       = " + str(self.height_svg_file))
        print(nameMethod + " : SVG file aspect ratio = " + str(self.aspect_ratio_svg_file))

        print(nameMethod + " : Exit")


    def __display_diagnostics_widget_render_area(self) :

        nameMethod  = self.__class__.__name__ + \
                      "::__display_diagnostics_widget_render_area"


        print(nameMethod + " : Enter")

        print(nameMethod + " : Widget render area width        = " + str(self.width_widget_render_area))
        print(nameMethod + " : Widget render area height       = " + str(self.height_widget_render_area))
        print(nameMethod + " : Widget render area aspect ratio = " + str(self.aspect_ratio_widget_render_area))

        print(nameMethod + " : Exit")


    def __display_diagnostics_window(self) :

        nameMethod  = self.__class__.__name__ + \
                      "::__display_diagnostics_window"


        print(nameMethod + " : Enter")

        br = self.rect().bottomRight()

        self.aspect_ratio_window = (br.x() + 1) / (br.y() + 1)

        print(nameMethod + " : Bottom right        = (" + str(br.x()) + ", " + str(br.y()) + ")")
        print(nameMethod + " : Window Aspect ratio = " + str(self.aspect_ratio_window))

        print(nameMethod + " : Exit")


    def __display_diagnostics(self) :

        nameMethod  = self.__class__.__name__ + \
                      "::__display_diagnostics"


        print(nameMethod + " : Enter")

        # Display some basic information about this object.

        self.__display_size_hint()
        self.__display_diagnostics_svg_file()
        self.__display_diagnostics_widget_render_area()
        self.__display_diagnostics_window()

        print(nameMethod + " : Exit")


    def __set_current_state(self) :

        pass


    def resizeEvent(self, event) :

        nameMethod  = self.__class__.__name__ + \
                      "::resizeEvent"


        print(nameMethod + " : Enter")

        print(nameMethod + " : Exit")


    def paintEvent(self, event) :

        nameMethod  = self.__class__.__name__ + \
                      "::paintEvent"


        print(nameMethod + " : Enter")

        print(nameMethod + " : Event = " + str(QEvent.Type(event.type())))

        self.__setup_values()
        self.__display_diagnostics()

        # Create a QPainter object.
        #
        # This is a drawing engine that knows how to render an SVG file onto this widget's, i.e. self, render area.

        painter = QPainter(self)

        if not self.processor_svg_file.isValid() :

            return

        # If possible, try and keep the aspect ratio of the image the same. This is to prevent it
        # from looking distorted.
        #
        # What are the new dimensions of

        # Paint the image onto the specified painter object.
        #
        # Centre the image.

        if self.aspect_ratio_widget_render_area > self.aspect_ratio_svg_file :

            print(nameMethod + " : Aspect ratio = Greater than")

            # The width of the render area is too great compared to the height of the render area.
            #
            # Limit the height of the image to the height of the render area.

            height = self.rect().height()
            width  = self.aspect_ratio_svg_file * height

        elif self.aspect_ratio_widget_render_area < self.aspect_ratio_svg_file :

            print(nameMethod + " : Aspect ratio = Less than")

            # The height of the render area is too great compared to the width of the render area.
            #
            # Limit the width of the image to the width of the render area.

            width  = self.rect().width()
            height = width / self.aspect_ratio_svg_file

        else :

            print(nameMethod + " : Aspect ratio = Same")

            width  = self.rect().width()
            height = width / self.aspect_ratio_svg_file

            # rectangle_target = QRectF(0, 0, 512, 576)

        x_start = (width - self.width_svg_file) / 2

        rectangle_target = QRectF(x_start, 0, width - 1, height - 1)

        # renderer.render(painter, QRectF(self.rect()))
        # renderer.render(painter, QRectF(0, 0, 512, 576))

        # Will the target rectangle will be drawn inside the render area?

        # >>>>>

        view_box    = self.processor_svg_file.viewBoxF()
        widget_rect = QRectF(self.rect())

        # Compute the scaling factors for both the x and y directions.
        #
        # The scaling factor measures the ratio of the width or height of the widget's rendering area, to the width or
        # height of the SVG image which is to be rendered into the widget's rendering area.

        scaling_factor_width  = widget_rect.width()  / view_box.width(),
        scaling_factor_height = widget_rect.height() / view_box.height()

        # Select the smaller of the two scaling factor values, otherwise the scaled SVG image will extend beyond the
        # boundary of one of the dimensions of the widget's rendering area.

        scale = min(scaling_factor_width, scaling_factor_height)

        # We can now scale the SVG image appropriately.

        new_w = view_box.width() * scale
        new_h = view_box.height() * scale

        # Get the difference between the widget's rendering area and the newly scaled SVG image.
        #
        # Should only one of these values not be equal to 0?

        delta_x = (widget_rect.width() - new_w)
        delta_y = (widget_rect.height() - new_h)

        # Split these differences in half so that we know how to offset our newly scaled images within the widget's
        # rendering area.

        offset_x = delta_x / 2
        offset_y = delta_y / 2

        # Specify the target rectangle.
        #
        # This tells us whwerabouts within the widgets's rendering area, the newly scaled SVG image should be placed.

        target = QRectF(offset_x, offset_y, new_w, new_h)
        self.processor_svg_file.render(painter, target)

        # <<<<<

        # renderer.render(painter, rectangle_target)

        print(nameMethod + " : Exit")


    def paintEvent_double(self, event) :

        nameMethod  = self.__class__.__name__ + \
                      "::paintEvent_double"

        painter     = QPainter(self)
        widget_rect = QRectF(self.rect())


        print(nameMethod + " : Enter")

        super().__init__()

        # Display some basic dimensions.

        width  = self.width()
        height = self.height()

        aspect_ratio = width/height

        print(nameMethod + " : SVG image onscreen width  = " + str(width))
        print(nameMethod + " : SVG image onscreen height = " + str(height))
        print(nameMethod + " : SVG image aspect ratio    = " + str(aspect_ratio))

        renderer = self.renderer()

        if not renderer.isValid():

            return

        view_box = self.renderer().viewBoxF()

        scaled = view_box

        # Define a new size (e.g., scale by 2x)

        new_width  = view_box.width() * 2
        new_height = view_box.height() * 2

        # Create a new rectangle with the scaled size (maintaining top-left corner)

        scaled_rect = QRectF(view_box.topLeft(), QSizeF(new_width, new_height))

        # scaled.scale(widget_rect.size(), Qt.KeepAspectRatio)

        # renderer.render(painter, QRectF(scaled_rect()))

        target = QRectF(width, height, new_width, new_height)

        # Render the new rectangle to the screen.

        self.renderer().render(painter, target)

        print(nameMethod + " : Exit")


if __name__ == "__main__" :

    nameMethod = "main"


    try :

        app = QApplication(sys.argv)

        svg_widget = MySvgWidget("/home/craig/source_code/python/visualiser_8_Feb_2026/svg/Eulers_formula_(45,8).svg")

        window = QMainWindow()

        window.setCentralWidget(svg_widget)

        window.show()
        app.exec()

    except Exception as e:

        print(nameFunction + " : CAUGHT THE FOLLOWING EXCEPTION")
        print(nameFunction + " : " + str(e))

    exit(False)