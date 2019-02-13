from lib import logger
from lib import sensor
from lib.sensor import *
from lib import dispatcher
import logging
import inspect


def main():
    # TODO Add support for arguments with argsparse.
    # Initialise logging module
    main_logger = logger.EventLogger(name=__name__)
    main_logger.write("debug", "Program starts.")

    # Add available sensors to a dictionary
    sensors = {}
    if len(sensor.__all__):
        for module in sensor.__all__:
            for obs, y in inspect.getmembers(eval(module)):
                if inspect.isclass(y) and inspect.getmodule(y) == eval(module):
                    oggetto = y()
                    if oggetto.check_availability():
                        sensors[module] = oggetto
                    else:
                        main_logger.write("error", "Sensor {} is not ready.".format(module))
    else:
        main_logger.write("error", "No module found.")

    csv = logger.WriterCSV()  # Initialise CSV writer

    # Send sensors to execution engine
    engine = dispatcher.TaskCentre(main_logger, sensors)
    main_logger.write("info", "Loaded modules: {}".format(engine.queue))
    main_logger.write("info", "First level elements in the list will be executed concurrently.")
    engine.set_end_time(60)
    try:
        engine.start(csv, 1)
    finally:
        csv.shutdown()
    main_logger.write("info", "Ended.")
    return


if __name__ == '__main__':
    main()
