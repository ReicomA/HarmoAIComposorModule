from .label.connect_label import *

class ConnectionData:
    def __init__(self, signal, host):

        try:
            self.signal = changeConnectSignalToInteger(signal)
            # host
            if isinstance(host, str) is False:
                raise TypeError("ip must be string")
            self.host = host
        except Exception as e:
            raise e
