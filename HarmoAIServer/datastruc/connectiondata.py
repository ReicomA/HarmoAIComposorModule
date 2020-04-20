from .label.connect_label import *

class ConnectionData:
    def __init__(self, signal, host, serial):

        try:
            self.signal = signal
            # host
            if isinstance(host, str) is False:
                raise TypeError("ip must be string")
            self.host = host
            self.serial = serial
        except Exception as e:
            raise e
