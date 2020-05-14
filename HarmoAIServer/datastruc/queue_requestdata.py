# -*- coding: utf-8 -*-
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
        self.lockMutex()
        self.dataContainer.append(data)
        self.unLockMutex()
    