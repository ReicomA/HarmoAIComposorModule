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

import threading
import time
import string
import random

from datastruc.connectiondata import *
from datastruc.queue_connectiondata import *
from datastruc.config import Config

from data_translater import DataTranslaterTypeLabel
from serverconnection import *

from deeplearningmanagement import DeepLearningManagement

class ClientManagement(threading.Thread):
    """ 유저 연결 여부를 관리하는 클래스 """

    def __init__(self, connectionQueue, config, connection, dlManagement):
        # TODO 전처리 수행
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.connectionQueue = connectionQueue
        self.config = config
        self.shutdownSignal = False
        self.conn = connection
        self.dlManagement = dlManagement

    # 쓰레드 종료
    def shutdown(self):
        self.shutdownSignal = True

    # read From ConnectionQueue
    def read(self):
        return self.connectionQueue.get()
        
    # check Serial
    def checkSerial(self, data):
        if isinstance(data, ConnectionData) is False:
            raise TypeError("data must be ConnectionData")
        else:
            return self.config.serial == data.serial

    def connectClient(self, data):
        
        # 동일한 호스트가 있는지 판정
        if self.conn.conn.hexists(ServerConnectionKeyLabels.IPMAP.value, data.host) is False:

            isNewKeyUnique = False
            newKey = None
            # 고유한 키가 뜰 때 까지 반복
            while isNewKeyUnique is False:
                                
                # 일단 true로 전환
                # 키를 생성하고 같은게 존재하면 False로 변환
                isNewKeyUnique = True
                newKey = self.makeRandomKey()

                # key 리스트 가져오기
                keyList = self.conn.conn.hvals(ServerConnectionKeyLabels.IPMAP.value)

                for item in keyList:
                    if item.decode('utf-8') == newKey:
                        isNewKeyUnique = False
                        break

            self.conn.conn.hset(ServerConnectionKeyLabels.IPMAP.value, data.host, newKey)


    def disConnectClient(self, data):
        # 호스트 유무 확인
        if self.conn.conn.hexists(ServerConnectionKeyLabels.IPMAP.value, data.host) is True:
            self.conn.conn.hdel(ServerConnectionKeyLabels.IPMAP.value, data.host)
            print("delete")


    """ UserKey를 생성하는 함수 """
    def makeRandomKey(self):
        resultKey = ""
        stringPool = string.ascii_letters
        for i in range(0, 9):
            resultKey += random.choice(stringPool)
        return resultKey

    # Start시 실제로 사용하는 부분
    def run(self):
        while self.shutdownSignal is False:
            # data 추출
            data = self.read()
            if data != None:
                # Serial Check
                if self.checkSerial(data) is False:
                    # TODO Log Module로 에러 데이터 전송
                    pass
                else:
                    if data.signal == DataTranslaterTypeLabel.CONNECT.value:
                        self.connectClient(data)
                    elif data.signal == DataTranslaterTypeLabel.DISCONNECT.value:
                        self.disConnectClient(data)
                    else:
                        # TODO LogModule로 에러 데이터 전송
                        print(data.signal)
                        pass
            else:
                time.sleep(0.001)
        
        # TODO shutdownSignal이 True가 될 때 뒷처리 수행
