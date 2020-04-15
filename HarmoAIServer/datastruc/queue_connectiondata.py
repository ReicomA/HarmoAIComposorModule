from .label.connect_label import *
from .connectiondata import *
from .queuemodel import *

class ConnectionDataQueue(QueueModel):

    def __init__(self, maxSize):
        super().__init__(maxSize)

    def put(self, data):
        # data type  판정
        if isinstance(data, ConnectionData) is False:
            raise TypeError("data must be connectiondata")
        
        # max Size 판정
        if self.currentSize() == self.maxSize:
            raise ValueError("queue is aleady full")
        
        self.dataContainer.append(data)