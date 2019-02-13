import enum


class InterfaceResource(enum.Enum):
    RS232 = 0
    I2C = 1
    SPI = 2
    EXE = 3


class InterfaceSetting:
    def __init__(self, connection, parameter):
        self.type = connection
        self.config = None
        self.port = None
        self.bus = None
        self.channel = None

        if connection == InterfaceResource.RS232:
            self.rs232(str(parameter))
        if connection == InterfaceResource.I2C:
            self.i2c(str(parameter))
        if connection == InterfaceResource.SPI:
            self.spi(str(parameter))

    def rs232(self, input):
        self.config = "port"
        self.port = input  # define which tty to use
        pass

    def i2c(self, input):
        self.config = "bus"
        self.bus = input  # define which bus to use
        pass

    def spi(self, input):
        self.config = "channel"
        self.channel = input  # define which channel to use
        pass

    def exe(self):
        pass

