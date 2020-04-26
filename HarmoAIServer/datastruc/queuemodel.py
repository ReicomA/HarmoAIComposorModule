
# Copyright SweetCase Project, Re_Coma(Ha Jeong Hyun). All Rights Reserved.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#      http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from abc import *
import threading

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
        self.queueMutex = threading.Lock()

    """  global에서 사용하면 안되는 함수 """
    def lockMutex(self):
        self.queueMutex.acquire()
    
    def unLockMutex(self):
        self.queueMutex.release()

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
        self.queueMutex.acquire()
        if self.isEmpty() == True:
            self.queueMutex.release()
            return None
        else:
            self.queueMutex.release()
            return self.dataContainer[0]

    """ 데이터 꺼내기 
        아무것도 없으면 None 반환
    """
    def get(self):
        if self.isEmpty() == True:
            return None
        else:
            self.queueMutex.acquire()

            returnData = self.dataContainer[0]
            del self.dataContainer[0]
            
            self.queueMutex.release()
            return returnData
    
    """ 비우기 """
    def clear(self):
        self.queueMutex.acquire()
        self.dataContainer = []
        self.queueMutex.release()

    """ 여기서부터 가상함수 (직접 구현 필요) """

    # 데이터 삽입
    @abstractmethod
    def put(self, data):
        pass
