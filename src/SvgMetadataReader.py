import sys
import re
from   PyQt6.QtCore    import QFile, QIODevice, QXmlStreamReader
from   PyQt6.QtWidgets import QApplication, QMessageBox


# List of class methods :
#
#   - open_file
#   - close_file
#   - parse_xml_svg
#   - display_plot_parameters
#   - close
#   - getBase
#   - getAzimuth
#   - getElevation
#
#   - read_parameters_from_file
#
#   - __init__
#   - __processToken
#   - __process_li_element
#   - __process_base_element
#   - __process_azimuth_element
#   - __process_elevation_element
#
#
# How to use this class.
#
#   - Create am object of the class
#   - Tell this object which SVG file to use
#   - Invoke the object's parse_xml_svg method


class SvgMetadataReader() :

    def __init__(self, filename_xml_file) :

        self.verbose      = False

        self.filename     = None
        self.file_handle  = None

        self.ns_uri       = None
        self.local_name   = None

        self.reader       = None
        self.token        = None
        self.elementStack = []
        self.base         = None
        self.azimuth      = None
        self.elevation    = None


    def set_filename(self, filename) :

        self.filename    = filename
        self.file_handle = QFile(filename)


    def get_parameters_from_file(self, filename) :

        nameMethod = "SvgMetadataReader::read_parameters_from_file"

        base      = None
        azimuth   = None
        elevation = None


        print(nameMethod + " : Enter")

        try :

            # Set the name of the SVG file then open it.

            self.set_filename(filename)
            self.open_file()

            # Create an XML SAX parser and open it on the SVG file.

            self.create_and_open_sax_reader()

            # Process the SVG file.

            self.process_all_tokens()

            # Close the file now that we have finished with it.

            self.file_handle.close()

        except Exception as e :

            print("Caught an exception : " + str(e))

        print(nameMethod + " : Exit")


        return [base, azimuth, elevation]


    def open_file(self) :

        nameMethod = "SvgMetadataReader::open_file"


        print(nameMethod + " : Enter")

        if not self.file_handle.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text) :

            # Use QMessageBox in a full PyQt app if needed, otherwise print error

            print(nameMethod + " : Exit prematurely due to exception")

            raise Exception("Failed to open file for reading : " + self.filename_xml_file)

        print(nameMethod + " : Exit")


    def create_and_open_sax_reader(self) :

        """ Create an XML SAX parser and open it on the SVG file.

        :return: NA
        :rtype: NA
        """

        nameMethod = "SvgMetadataReader::create_and_open_sax_reader"

        print(nameMethod + " : Enter")

        self.reader = QXmlStreamReader(self.file_handle)

        print(nameMethod + " : Exit")


    def process_all_tokens(self) :

        """Process all of the XML tokens in the SVG file.

        :raises Exception: If an error occurs while processing the SVG file.
        :return: NA
        :rtype: NA
        """

        nameMethod = "SvgMetadataReader::process_all_tokens"


        print(nameMethod + " : Enter")

        while (not self.reader.atEnd()) and \
              (not self.reader.hasError()) :

            self.read_and_process_next_token()

        # Check if an error has occurred while running the loop.

        if self.reader.hasError() :

            print(nameMethod + " : Exit prematurely due to exception")

            raise Exception("Error parsing XML : " + self.reader.errorString())

        print(nameMethod + " : Exit")


    # - Open the SVG file.
    # - Create a new SAX reader to open a stream on the SVG file.
    # - While still possible.
    #     - Read the next token from the stream.
    #     - Process the token which was just read from the stream.
    # - If an error occurred while processing the tokens, then close the stream

    # TODO : Probably delete this method.

    def process_file(self) :

        try :

            # Open the SVG file.

            self.open_file()

            # Create a new SAX reader to open a stream on the XML file.

            self.open_sax_reader()

            #

            self.process_all_tokens()

            # Close the file now that we have finished with it.

            self.file_handle.close()

        except Exception as e :

            print("Caught an exception : " + str(e))


    def read_and_process_next_token(self) :

        nameMethod = "SvgMetadataReader::process_all_tokens"


        print(nameMethod + " : Enter")

        # Read the next token from the stream and then process it.

        self.token = self.reader.readNext()
        self.__processToken()


    def __processToken(self) :

        # Check that the token isn't empty or doesn't exist.

        if self.token is None :

            raise Exception("Token is empty or doesn't exist.")

        if self.verbose:

            print("Token = " + str(self.token))

        # Ascertain the type of the token which was just read.

        if self.reader.isStartElement():

            # We have encountered an opening tag, e.g. <tag>.
            #
            # What about tags like <tag ... />

            self.ns_uri = str(self.reader.namespaceUri())
            self.local_name = str(self.reader.name())

            # Push the tag onto the tag stack.

            self.elementStack.append(self.local_name)

            # print("Number of elements in stack = " + str(len(self.elementStack)))

            if (self.local_name is not None) and \
               (self.local_name == "li"):

                self.process_li_element()

        elif self.token == QXmlStreamReader.TokenType.EndElement:

            # We have encountered a closing tag, e.g. </tag>.
            #
            # Pop the tag from the stack.

            self.elementStack.pop()


    def __process_li_element(self) :

        print("Namespace  = " + self.ns_uri)
        print("Local name = " + self.local_name)
        print("Encountered XML element : li")

        # Get the value of the element.

        value_element = self.reader.readElementText()

        print("    Element value = " + value_element)

        if self.process_base_element() :

            return

        if self.process_azimuth_element() :

            return

        if self.process_elevation_element() :

            return


    def __process_base_element(self) :

        # Check if the value of the element contains the value for : azimuth

        result_search = re.search(r"azimuth", value_element)

        if result_search is not None:

            # The value of the element appears to contain the word "azimuth".

            result_search = re.search(r"\d{1,3}", value_element)
            self.azimuth = result_search.group()

            print("Azimuth = " + self.azimuth)

            return


    def __process_azimuth_element(self):

        # Check if the value of the element contains the value for : elevation

        result_search = re.search(r"elevation", value_element)

        if result_search is None:

            raise Exception("Element value does not contain the following text : elevation")

        else :

            # The value of the element appears to contain the word "elevation".

            result_search = re.search(r"\d{1,3}", value_element)
            self.elevation = result_search.group()

            print("Elevation = " + self.elevation)

            return


    def __process_elevation_element(self):

        # Check if the value of the element contains the value for : base

        result_search = re.search(r"base", value_element)

        if result_search is not None:

            # The value of the element appears to contain the word "elevation".

            result_search = re.search(r"\d{1,3}", value_element)
            self.base = result_search.group()

            print("Base = " + self.base)


    def display_plot_parameters(self) :

        print("Base                   = " + self.base)
        print("View angle : azimuth   = " + self.azimuth)
        print("View angle : elevation = " + self.elevation)


    def get_base(self) :

        return self.base


    def get_azimuth(self):

        return self.azimuth


    def get_elevation(self):

        return self.elevation


if __name__ == "__main__":

    svgMetadataReader = SvgMetadataReader(sys.argv[1])


    # QApplication is required for some Qt functionalities even in console apps.

    app = QApplication(sys.argv)

    # svgMetadataReader.set_filename_svg_file(sys.argv[1])

    plot_parameters = svgMetadataReader.get_parameters_from_file(sys.argv[1])

    if plot_parameters[0] is not None :

        print("Plot parameter : base      = " + plot_parameters[0])

    if plot_parameters[1] is not None:

        print("Plot parameter : azimuth   = " + plot_parameters[1])

    if plot_parameters[2] is not None:

        print("Plot parameter : elevation = " + plot_parameters[2])
