# import sys
import re
from   PySide6.QtCore    import (QFile,
                                 QIODevice,
                                 QXmlStreamReader,
                                 Slot)
# from   PySide6.QtWidgets import QApplication, QMessageBox


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
#   - __process_element_base
#   - __process_element_azimuth
#   - __process_element_elevation
#
#
# How to use this class.
#
#   - Create am object of the class
#   - Tell this object which SVG file to use
#   - Invoke the object's parse_xml_svg method


class SvgMetadataReader() :

    def __init__(self) :

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

        self.debug        = False


    def set_filename(self, filename) :

        self.filename    = filename
        self.file_handle = QFile(filename)


    # - Set the name of the SVG file and then open it.
    # - Create an XML SAX parser and open it on the SVG file.
    # - Process all tokens in the SVG file.
    # - Close the SVG file now that we have finished with it.

    def get_parameters_from_file(self, filename, display_values=False) :

        """

        :param filename:
        :return: A dictionary of parameter-value pairs for the base, azimuth, and elevation.
        """

        nameMethod = "SvgMetadataReader::get_parameters_from_file"


        if self.debug :

            print(nameMethod + " : Enter")

        try :

            # Set the name of the SVG file and then open it.

            self.set_filename(filename)
            self.__open_file()

            # Create an XML SAX parser and open it on the SVG file.

            self.__create_and_open_sax_reader()

            # Process all tokens in the SVG file.

            self.__process_all_tokens()

            # Close the SVG file now that we have finished with it.

            self.file_handle.close()

            if display_values :

                self.print_plot_parameters()

        except Exception as e :

            print("Caught an exception : " + str(e))


        if self.debug :

            print(nameMethod + " : Exit")

        return {"base"      : self.base,
                "azimuth"   : self.azimuth,
                "elevation" : self.elevation}


    def __open_file(self) :

        nameMethod = "SvgMetadataReader::__open_file"


        if self.debug :

            print(nameMethod + " : Enter")

        if not self.file_handle.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text) :

            # Use QMessageBox in a full PyQt app if needed, otherwise print error

            print(nameMethod + " : Exit prematurely due to exception")

            raise Exception("Failed to open file for reading : " + self.filename)

        if self.debug:

            print(nameMethod + " : Exit")


    def __create_and_open_sax_reader(self) :

        """ Create an XML SAX parser and open it on the SVG file.

        :return: NA
        :rtype: NA
        """

        nameMethod = "SvgMetadataReader::__create_and_open_sax_reader"

        if self.debug :

            print(nameMethod + " : Enter")

        self.reader = QXmlStreamReader(self.file_handle)

        if self.debug :

            print(nameMethod + " : Exit")


    def __process_all_tokens(self) :

        """Process all of the XML tokens in the SVG file.

        :raises Exception: If an error occurs while processing the SVG file.
        :return: NA
        :rtype: NA
        """

        nameMethod = "SvgMetadataReader::__process_all_tokens"


        if self.debug :

            print(nameMethod + " : Enter")

        while (not self.reader.atEnd()) and \
              (not self.reader.hasError()) :

            self.__read_and_process_next_token()

        # Check if an error has occurred while running the loop.

        if self.reader.hasError() :

            if self.debug:

                print(nameMethod + " : Exit prematurely due to exception")

            raise Exception("Error parsing XML : " + self.reader.errorString())

        if self.debug :

            print(nameMethod + " : Exit")


    def __read_and_process_next_token(self) :

        nameMethod = "SvgMetadataReader::__read_and_process_next_token"


        # print(nameMethod + " : Enter")

        # Read the next token from the stream and then process it.

        self.token = self.reader.readNext()
        self.__processToken()

        # print(nameMethod + " : Exit")


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

                self.__process_li_element()

        elif self.token == QXmlStreamReader.TokenType.EndElement:

            # We have encountered a closing tag, e.g. </tag>.
            #
            # Pop the tag from the stack.

            self.elementStack.pop()


    def __process_li_element(self) :

        nameMethod  = self.__class__.__name__ + \
                      "::__process_li_element"


        if self.debug :

            print(nameMethod + " : Enter")

            print("Namespace  = " + self.ns_uri)
            print("Local name = " + self.local_name)
            print("Encountered XML element : li")

        # Get the value of the element.

        value_element = self.reader.readElementText()

        if self.debug :

            print(nameMethod + " :   Element value = " + value_element)

        if self.__process_element_base(value_element) :

            return

        if self.__process_element_azimuth(value_element) :

            return

        if self.__process_element_elevation(value_element) :

            return

        if self.debug :

            print(nameMethod + " : Exit")


    def __process_element_base(self, value_element) :
        """

        :param value_element:
        :return:
        """

        # r"\d+(?:\.\d+)
        #
        # \d+       : A digit, repeated one or more times.
        # (?:\.\d+) : A non-capturing group.

        nameMethod  = "SvgMetadataReader::__process_element_base"
        returnValue = False


        if self.debug :

            print(nameMethod + " : Enter")

        # Check if the value of the element contains the value for : base

        result_search = re.search(r"base", value_element)

        if result_search is not None:

            returnValue = True

            # The value of the element appears to contain the word "base".

            result_search = re.search(r"\d+(?:\.\d*)", value_element)

            self.base = result_search.group()

            if self.debug:

                print(nameMethod + " : Base = " + self.base)

        if self.debug:

            print(nameMethod + " : Exit")

        return returnValue


    def __process_element_azimuth(self, value_element):

        nameMethod  = "SvgMetadataReader::__process_element_azimuth"
        returnValue = False


        if self.debug:

            print(nameMethod + " : Enter")

        # Check if the value of the element contains the value for : azimuth

        result_search = re.search(r"azimuth", value_element)

        if result_search is not None:

            returnValue = True

            # The value of the element appears to contain the word "azimuth".

            result_search = re.search(r"\d{1,3}", value_element)
            self.azimuth = result_search.group()

            if self.debug:

                print("Azimuth = " + self.azimuth)

        if self.debug:

            print(nameMethod + " : Exit")

        return returnValue


    def __process_element_elevation(self, value_element):

        nameMethod  = "SvgMetadataReader::__process_element_elevation"
        returnValue = False


        if self.debug :

            print(nameMethod + " : Enter")

        # Check if the value of the element contains the value for : elevation

        result_search = re.search(r"elevation", value_element)

        if result_search is not None:

            returnValue = True

            # The value of the element appears to contain the word "elevation".

            result_search = re.search(r"\d{1,3}", value_element)
            self.elevation = result_search.group()

            if self.debug :

                print("Elevation = " + self.elevation)


        if self.debug :

            print(nameMethod + " : Exit")

        return returnValue


    def display_plot_parameters(self) :

        if self.debug :

            print("Base                   = " + str(self.base))
            print("View angle : azimuth   = " + str(self.azimuth))
            print("View angle : elevation = " + str(self.elevation))


    def print_plot_parameters(self) :

        self.display_plot_parameters()


    def get_base(self) :

        return self.base


    def get_azimuth(self):

        return self.azimuth


    def get_elevation(self):

        return self.elevation


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

        print(nameMethod + " : self.debug = " + str(self.debug))
        print(nameMethod + " : &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        print(nameMethod + " : &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        print(nameMethod + " : &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        print(nameMethod + " : &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        print(nameMethod + " : &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        print(nameMethod + " : &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")

        print(nameMethod + " : Exit")