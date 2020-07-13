import inspect

from lib import logger
from lib import sensor
from lib.sensor import *
from lib import dispatcher


def main():
    # TODO: Add support for arguments with argsparse.
    # Initialise logging module
    main_logger = logger.EventLogger(name=__name__)
    main_logger.write("debug", "Program starts.")

    # Add available sensors to a dictionary: dict_key is str, dict_value is sensor object
    sensors = {}
    if sensor.__all__:  # if sensor module file exists under lib/sensor folder
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

    # Exit the application if no usable sensor
    if not sensors:
        main_logger.write("error", "Sensor list is empty. No usable sensor is available.")
        raise Exception("Sensor list is zero. No usable sensor is available.")

    # Initialise CSV writer
    csv = logger.WriterCSV()

    # Send sensors to execution engine
    engine = dispatcher.TaskCentre(sensors)
    sensor_queue_list = []
    for sens in engine.queue:
        for sen in sens:
            sensor_queue_list.append(sen)
    main_logger.write("debug", "Loaded modules: {}".format(";".join(z for z in sensor_queue_list)))
    main_logger.write("info", "First level elements in the list will be executed concurrently.")
    engine.set_end_time(60)
    try:
        engine.start(csv, 1)
    finally:
        csv.shutdown()
    main_logger.write("info", "Ended.")


if __name__ == '__main__':
    main()
