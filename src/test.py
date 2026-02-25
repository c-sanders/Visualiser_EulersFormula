import traceback

from   ServiceStarter.ServiceStarter             import ServiceStarter
from   VisualiserMainWindow.VisualiserMainWindow import VisualiserMainWindow


if __name__ == "__main__" :

    nameMethod = "main"
    debug      = False


    if debug :

        print(nameMethod + " : Enter")

    try :

        # Create an object which will be responsible for starting all of the necessary services.

        service_starter = ServiceStarter()
        service_starter.start_services()

        # Instruct it to start all of the necessary services.

        service_starter.app_set_stylesheet()
        app = service_starter.get_app()

        # Create a main window for the application.

        window = VisualiserMainWindow(app)

        # window.initialise(app)

        window.show()
        app.exec()

        traceback.print_stack()

    except Exception as e:

        print(nameMethod + " : CAUGHT THE FOLLOWING EXCEPTION")
        print(nameMethod + " : " + str(e))

    if debug:

        print(nameMethod + " : Exit")

    exit(False)