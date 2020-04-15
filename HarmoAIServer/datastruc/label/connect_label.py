from enum import Enum

class ClientConnectSignal(Enum):
    CONNECT = 1
    DISCONNECT = 2

def changeConnectSignalToInteger(signal):
    for serverSignal in ClientConnectSignal:
        if signal == serverSignal.name:
            return serverSignal.value
    else:
        raise ValueError("This is not string data")