import os
import time
import logging


class EventLogger:
    def __init__(self, name=__name__, log_level=logging.DEBUG, log_to_file=False):
        self.log = logging.getLogger(name)

        self.log.setLevel(log_level)

        handler = logging.StreamHandler()
        seq = logging.Formatter('%(levelname)-9s:: %(message)s [%(name)s]')
        handler.setLevel(log_level)
        handler.setFormatter(seq)
        self.log.addHandler(handler)

        if log_to_file:
            path = "LOG-{}.log".format(int(time.time()))
            file = logging.FileHandler(filename=path)
            file.setFormatter(seq)
            file.setLevel(log_level)
            self.log.addHandler(file)

    def write(self, level, message):
        if hasattr(self.log, level):
            getattr(self.log, level)(message)

    @staticmethod
    def shutdown():
        logging.shutdown()


class WriterCSV:
    def __init__(self, path=None):
        # Too lazy to write new CSV wrapper, hence dump it to logging
        self.writer = logging.getLogger("READING")
        logging.addLevelName(100, "STREAM")
        self.writer.setLevel(100)

        file = logging.FileHandler(filename=self._create_file(path))
        spec = logging.Formatter('%(message)s')
        file.setLevel(100)
        file.setFormatter(spec)
        self.writer.addHandler(file)

        self.csvheader = None

    @staticmethod
    def shutdown():
        logging.shutdown()

    def register(self, entry: list):
        if not len(entry):
            raise ValueError("The list contains no measurement.")
        self.csvheader = entry
        self.writer.log(100, ",".join(entry))

    def write(self, entry: dict):
        if self.csvheader:
            line_str = []
            for head in self.csvheader:
                line_str.append(str(entry[head]))
            self.writer.log(100, ",".join(line_str))
        else:
            raise ValueError("No measurement has been registered.")

    def _create_file(self, path):
        filename = path if path else time.strftime("%Y%m%d-%H%M%S")  # Define file name
        filename = filename if filename.endswith(".csv") else filename + ".csv"  # Add file extension
        full_path = os.path.abspath(filename)
        if not os.access(os.path.dirname(full_path), os.W_OK):
            raise PermissionError("Unable to save log file to destination")
        return full_path


if __name__ == '__main__':
    pass

