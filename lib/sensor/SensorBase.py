from .. import InterfaceResource
from .. import logger

sensor_logger = logger.EventLogger(name=__name__)


class SensorBase:
    def __init__(self, name: str, comm: InterfaceResource.InterfaceSetting):
        self.name = name
        self.connection = comm
        sensor_logger.write("debug", "Registered {}, using {} interface".format(
            self.name,
            self.connection.type))

    def read(self):
        raise NotImplementedError()

    def write(self):
        raise NotImplementedError()

    # def sensor_list(self):
    #     raise NotImplementedError()

    def check_availability(self):
        raise NotImplementedError()

    # def get_param(self):
    #     raise NotImplementedError()
    #
    # def set_param(self):
    #     raise NotImplementedError()


if __name__ == "__main__":
    print("Nothing to run.")
