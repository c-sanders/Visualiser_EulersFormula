from   PySide6.QtCore    import (QObject,
                                 Signal,
                                 Slot)

import numpy             as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class PlotGenerator(QObject) :

    finished = Signal()
    progress = Signal(int, int, str)


    def __init__(self, dirname) :

        nameMethod = self.__class__.__name__ + \
                     "::__init__"


        print(nameMethod + " : Enter")

        super().__init__()

        if not dirname.endswith("/") :

            dirname += "/"

        self.dirname = dirname

        self.proceed_with_plots = True

        print(nameMethod + " : Exit")


    @Slot()
    def stop(self) :

        nameMethod = self.__class__.__name__ + \
                     "::stop"



        print(nameMethod + " : Enter")

        self.proceed_with_plots = False

        print(nameMethod + " : Exit")


    @Slot()
    def run(self) :

        nameMethod = self.__class__.__name__ + \
                     "::run"


        print(nameMethod + " : }}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}")
        print(nameMethod + " : }}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}")
        print(nameMethod + " : }}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}")
        print(nameMethod + " : Enter")
        print(nameMethod + " : }}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}")
        print(nameMethod + " : }}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}")
        print(nameMethod + " : }}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}")

        self.generate_plots()

        print(nameMethod + " : Exit")
