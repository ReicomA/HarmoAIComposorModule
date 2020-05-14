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

from enum import Enum
import json

from datastruc.label.connect_label import ConnectDataKeys
from datastruc.connectiondata import ConnectionData
from datastruc.label.requestdata_label import *
from datastruc.requestdata import RequestData

class DataTranslaterTypeLabel(Enum):
    CONNECT = 0
    REQUEST = 1
    DISCONNECT = -1

"""클라이언트로부터 들어온 데이터를 분석 해서 원하는 형태로 추출
"""
class DataTranslater:

    def __init__(self, connectionQueue, requestQueue):
        
        self.connectionQueue = connectionQueue
        self.requestQueue = requestQueue

    def translateData(self, data):
        """
            데이터를 스캔해서
            해당 큐에 삽입

            리턴값은 type값, 옳지 않은 데이터가 추출될 경우
            None 처리
        """
        if isinstance(data, bytes) is True:
            try:
                dataSet = json.loads(data.decode('utf-8'))
                dataType = dataSet['type']
                
                # type Data가 맞을 경우
                if isinstance(dataType, int) is True:

                    """ 연결, 해제 요청 클라이언트 """
                    if (dataType == DataTranslaterTypeLabel.CONNECT.value) or \
                        (dataType == DataTranslaterTypeLabel.DISCONNECT.value):

                        """ 데이터 추출 """
                        connectionData = ConnectionData(
                            dataType,
                            dataSet[ConnectDataKeys.IP.value],
                            dataSet[ConnectDataKeys.SERIAL.value]
                        )
                        
                        """ 데이터 큐로 전달 """
                        self.connectionQueue.put(connectionData)
                        return dataType

                    elif dataType == DataTranslaterTypeLabel.REQUEST.value:

                        requestData = RequestData(
                            dataSet[RequestDataTypeLabel.IP.value],
                            dataSet[RequestDataTypeLabel.GENRE.value],
                            dataSet[RequestDataTypeLabel.TIMESIGNATURE.value],
                            dataSet[RequestDataTypeLabel.NOTESIZE.value]
                        )
                        self.requestQueue.put(requestData)
                        return dataType
                    else:
                        raise TypeError("Wrong dataType")
                else:
                    raise TypeError("Wrong Type")
            # 정확하지 않은 데이터가 발견했을 경우 바로 제거
            except Exception as e:
                """ TODO 로그모듈 추가시 로그파일로 저장 요청"""
                print(e)
                return None
        else:
            return None
                
