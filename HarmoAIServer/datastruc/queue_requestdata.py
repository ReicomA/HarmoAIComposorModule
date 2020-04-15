from .label.requestdata_label import *
from .requestdata import *
from .queuemodel import *

# RequestData의 큐 클래스
class RequestDataQueue(QueueModel):

    def __init__(self, maxSize):
        super().__init__(maxSize)
    
    def put(self, data):
        # data type 판정
        if isinstance(data, RequestData) is False:
            raise TypeError("data must be RequestData")
        
        # maxSize 판정
        if self.currentSize() == self.maxSize:
            raise ValueError("queue is aleady full")
        
        # data 삽입
        self.dataContainer.append(data)
        
    