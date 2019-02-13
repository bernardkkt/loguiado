import time
import logging
import multiprocessing
from .InterfaceResource import InterfaceResource


class TaskCentre:
    def __init__(self, log_object, sensor_dict: dict):
        self.log = log_object
        self.end_at = None
        sensor_list = list(sensor_dict.values())
        self.queue = []
        for sensor in sensor_list:
            self.log.write("info", "Found sensor: {}".format(sensor.name))
            if self.queue:
                if sensor.connection.type == InterfaceResource.EXE:
                    self.queue.append({sensor.name: sensor})
                else:
                    for self.queue_dict in self.queue:
                        ombre = self.queue_dict
                        (nome, oggetto) = ombre.popitem()
                        if oggetto.connection.type != sensor.connection.type:
                            self.queue.append({sensor.name: sensor})
                        else:
                            oggetto_config = getattr(oggetto.connection, oggetto.connection.config)
                            sensor_config = getattr(sensor.connection, sensor.connection.config)
                            if oggetto_config != sensor_config:
                                self.queue.append({sensor.name: sensor})
                            else:
                                self.queue_dict[sensor.name] = sensor
            else:
                self.queue.append({sensor.name: sensor})

    def set_end_time(self, end_time):
        if type(end_time) == str:  # Input is time in string
            self.end_at = time.mktime(time.strptime(end_time, "%Y-%m-%d %H:%M:%S"))
        elif type(end_time) == int or type(end_time) == float:  # Input is duration in seconds
            self.end_at = time.time() + end_time
        else:
            raise TypeError("Failed to set period for logger. Please check the format again.")

    def start(self, csv_log_object, period: float):
        runner = MeasurementExec(self.queue)
        runner.init_sensors()  # In case there are still some initialisation steps defined under init function

        # list of sensor name with default sequence
        list_sensor = []
        for entries in self.queue:
            for entry in entries:
                list_sensor.append(entry)
        if "Time" in list_sensor:
            tmp_list = [list_sensor.pop(list_sensor.index("Time"))]
            for element in list_sensor:
                tmp_list.append(element)
            list_sensor = tmp_list

        csv_log_object.register(list_sensor)  # write heading to CSV

        while True:
            next_logging_time = time.time() + period
            readings = runner.run()
            print("")  # print new line
            csv_log_object.write(readings)
            if self.end_at:
                if self.end_at < time.time():
                    break  # Exit loop once reached end time
            while next_logging_time > time.time():
                time.sleep(0.001)  # sleep for 1 millisecond


class MeasurementExec:
    def __init__(self, sensor_queue=None):
        self.result = dict()
        self.sensor_queue = []
        if sensor_queue:
            self.add_sensors(sensor_queue)

    def add_sensors(self, sensor_queue: list):
        self.sensor_queue = sensor_queue

    def get_sensors(self):
        return self.sensor_queue

    def init_sensors(self):
        for x in self.sensor_queue:
            for y in x:
                if hasattr(x[y], "init"):
                    x[y].init()

    def thread(self, sensor_dict: dict):
        result_dict = dict()
        for each in sensor_dict:
            result = sensor_dict[each].read()
            print("{}: {}".format(each, result))
            result_dict[each] = result
        return result_dict

    def run(self):
        self.result = dict()
        pool = multiprocessing.Pool(len(self.sensor_queue))
        dict_result = pool.map(self.thread, self.sensor_queue)
        for element in dict_result:
            self.result.update(element)
        return self.result
