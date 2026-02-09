import os
import sys

from PySide6.QtWidgets                         import (QApplication,
                                                       QMainWindow)

from VisualiserMainWindow.VisualiserMainWindow import VisualiserMainWindow


run_animation             = True
file_path                 = ""
useCustomStylesheet       = False
filename_customStylesheet = "StylesheetCraig.qss"

use_frame_set_Eulers_formula_flyaround    = True
use_frame_set_Eulers_formula_varying_base = True


def processCommandLineArgs() :

    global file_path

    nameMethod            = "processCommandLineArgs"
    count_commandLineArgs = len(sys.argv)


    print(nameMethod + " : Enter")

    # Check if any command line args have been passed to this program.

    print(nameMethod + " : Number of command line args  = ", count_commandLineArgs)

    if count_commandLineArgs == 2:

        # Assume that the command line arg which was passed in at position 1, is the name of a file to load.

        print(nameMethod + " : Name of file to load = ", sys.argv[1])

        file_path = Path(sys.argv[1])

        print(nameMethod + " : file_path = ", file_path)

        if not file_path.is_file():

            raise Exception("Specified file doesn't seem to exist.")

    print(nameMethod + " : Exit")


def configureOS() :

    os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--disable-gpu"


def configureCSS(app) :

    nameMethod = "configureCSS"


    print(nameMethod + " : Enter")

    # Check if this program should be using a custom stylesheet.

    if useCustomStylesheet:

        try:

            with open(filename_customStylesheet, "r") as file:

                app.setStyleSheet(file.read())

        except FileNotFoundError:

            print("Stylesheet file 'StylesheetCraig.qss' not found.")


    print(nameMethod + " : Exit")


if __name__ == "__main__" :

    nameFunction = "main"


    try :

        processCommandLineArgs()

        configureOS()

        app = QApplication(sys.argv)

        configureCSS(app)

        print(nameFunction + " : Have configured CSS")

        if use_frame_set_Eulers_formula_flyaround :

            print(nameFunction + " : use_frame_set_Eulers_formula_flyaround")

        elif use_frame_set_Eulers_formula_varying_base :

            print(nameFunction + " : use_frame_set_Eulers_varying_base")

        print(nameFunction, " : file_path = ", file_path)

        # Create a main window object and then initialise it.

        print(nameFunction, " : About to create a Visualiser_MainWindow")

        window = VisualiserMainWindow()
        window.initialise()

        print(nameFunction, " : Have created a Visualiser_MainWindow")

        # Configure the main window object and then instruct it to show itself.

        window.show()

        # Instruct the Qt application framework to begin execution.

        app.exec()

    except Exception as e:

        print(nameFunction + " : CAUGHT THE FOLLOWING EXCEPTION")
        print(nameFunction + " : " + str(e))

    exit(False)