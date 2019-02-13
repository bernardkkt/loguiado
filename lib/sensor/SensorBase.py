from .. import InterfaceResource


class SensorBase:
    def __init__(self, name: str, comm: InterfaceResource.InterfaceSetting):
        self.name = name
        self.connection = comm

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
