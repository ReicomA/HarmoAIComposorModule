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

class ConnectionData:
    """
        클라이언트로부터 받는 연결관련 데이터셋
        signal: 연결/연결종료/요청
        host: 클라이언트 주소
        serial: 암구호.
    """
    def __init__(self, signal, host, serial):

        try:
            self.signal = signal
            # host
            if isinstance(host, str) is False:
                raise TypeError("ip must be string")
            self.host = host
            self.serial = serial
        except Exception as e:
            raise e
