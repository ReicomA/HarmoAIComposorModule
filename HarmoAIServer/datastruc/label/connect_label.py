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

""" Redis Server에 접속할 때 사용하는 문자열 데이터
    각 열거형의 value 값들은 json data를 생성할 때 key로 사용된다.
"""
class ConnectDataKeys(Enum):
    TYPE = "type"
    IP = "myIP"
    SERIAL = "serial"