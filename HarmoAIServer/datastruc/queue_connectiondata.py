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

from .label.connect_label import *
from .connectiondata import *
from .queuemodel import *

""" 클라이언트로부터 받는 연결 요청 데이터를 저장하는 구조
    queuemodel.py의 QueueModel로부터 상속을 받는다.
"""
class ConnectionDataQueue(QueueModel):
    """ 클라이언트로부터 받는 연결 요청 데이터를 저장하는 구조
        queuemodel.py의 QueueModel로부터 상속을 받는다.
    """
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