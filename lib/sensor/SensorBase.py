class SensorBase:
    def __init__(self):
        pass

    def read(self):
        pass

    def write(self):
        pass


class SensorResource(SensorBase):
    def sensor_list(self):
        pass

    def check_availability(self):
        pass

    def get_param(self):
        pass

    def set_param(self):
        pass