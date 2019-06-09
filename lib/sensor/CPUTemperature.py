import subprocess
from . import SensorBase
from ..InterfaceResource import InterfaceResource, InterfaceSetting


class CPUTemperature(SensorBase.SensorBase):
    def __init__(self):
        name = "CPU Temperature"  # set a name for sensor
        comm = InterfaceSetting(InterfaceResource.EXE,
                                None)  # define interface
        super().__init__(name, comm)

    def write(self):
        pass

    def __exec_by_local(self, cmd_str: [str], timeout=1):
        output_list = []
        for entry in cmd_str:
            output = subprocess.Popen(entry.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            try:
                output.wait(timeout)
                output_list.append(output.stdout.read())
            except subprocess.TimeoutExpired:
                output.kill()
                output_list.append(b'')
            finally:
                return output_list

    def check_availability(self):
        cmd_line = ["sensors -v"]
        result = self.__exec_by_local(cmd_str=cmd_line)
        for stream in result:
            if "libsensor" in stream.decode():
                return True
        return False

    def read(self):
        command_str_list = ["sensors -u pch_skylake-virtual-0"]
        output_list = self.__exec_by_local(cmd_str=command_str_list)
        for stream in output_list:
            if "temp1_input:" in stream.decode():
                return stream.decode().split()[-1]
        return "N/A"
