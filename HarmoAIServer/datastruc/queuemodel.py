from abc import *

"""
이 프로젝트에서 사용할 큐 모델
"""

class QueueModel(metaclass=ABCMeta):

    def __init__(self, maxSize):
        if isinstance(maxSize, int) is False:
            raise TypeError("max size must be integer")
        if maxSize <= 1:
            raise TypeError("max size must be over 1")
        self.maxSize = maxSize
        self.dataContainer = []

    """ 현재 큐가 비어있는지 확인 """
    def isEmpty(self):
        return ( len(self.dataContainer) == 0)
    
    """ 큐 안에 들어가 있는 데이터 갯수 확인 """
    def currentSize(self):
        return len(self.dataContainer)

    """ 맨 앞에 있는 큐 데이터 확인 
        아무것도 없으면 None 반환
    """
    def front(self):
        if self.isEmpty() == True:
            return None
        else:
            return self.dataContainer[0]

    """ 데이터 꺼내기 
        아무것도 없으면 None 반환
    """
    def get(self):
        if self.isEmpty() == True:
            return None
        else:
            returnData = self.dataContainer[0]
            del self.dataContainer[0]
            return returnData
    
    """ 비우기 """
    def clear(self):
        self.dataContainer = []

    """ 여기서부터 가상함수 (직접 구현 필요) """

    # 데이터 삽입
    @abstractmethod
    def put(self, data):
        pass
