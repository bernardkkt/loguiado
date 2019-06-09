import time
from . import SensorBase
from ..InterfaceResource import InterfaceResource, InterfaceSetting


class Timestamp(SensorBase.SensorBase):
    """
    This sensor module generates timestamps
    """
    def __init__(self):
        name = "Time"  # set a name for sensor
        comm = InterfaceSetting(InterfaceResource.EXE, None)  # define interface
        self.parameters = {"unit": "%Y-%m-%d %H:%M:%S",  # Available options: "sec",
                                                         #                    ".2f",
                                                         #                    "%Y-%m-%d %H:%M:%S"
                           "type": "datetime"}  # Available options: "relative", "datetime"
        self.START_EPOCH = None
        super().__init__(name, comm)

    def _get_time(self):
        return time.time()  # Instantly return a float representing current time

    def write(self):
        pass

    def check_availability(self):
        try:
            self._get_time()
            return True
        except:
            return False

    def read(self):
        val = self._get_time()  # Get time

        if self.START_EPOCH is None:
            self.START_EPOCH = val  # Set offset
        if self.parameters["type"] == "relative":  # Return elapsed time since offset
            if self.parameters["unit"] == "sec":
                return int(val - self.START_EPOCH)
            else:
                return format((val - self.START_EPOCH),
                              self.parameters["unit"])  # Return time in defined decimal place
        elif self.parameters["type"] == "datetime":
            if self.parameters["unit"] == "sec":  # Return epoch time
                return val
            else:  # Return date/time as defined in unit
                return time.strftime(self.parameters["unit"], time.localtime(val))

        raise ValueError("No type defined for Timestamp object")


if __name__ == "__main__":
    pass
