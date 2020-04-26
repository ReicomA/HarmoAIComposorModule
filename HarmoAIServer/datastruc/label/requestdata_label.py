
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

class RequestDataTypeLabel(Enum):
    """
        서버에 작곡 요청을 할 때 사용하는 
        열거형 클래스
        Json Data를 만들 때 key로 사용된다.
    """
    TYPE = "type"
    IP = "myIP"
    GENRE = "genre"
    TIMESIGNATURE = "timeSignature"
    NOTESIZE = "noteSize"

"""
요청 데이터에 대한 라벨들
    1. 박자(Signature)
    2. 박자(클라이언트로부터 받는 스트링 값)(SignatureFromClient)
    3. 장르(Genre)
    4. 장르(클라이언트로부터 받는 스트링 값)(GenreFromClient)
"""
class Signature(Enum):
    _4_2 = 1
    _4_3 = 2
    _4_4 = 3
    _8_3 = 4
    _8_6 = 5

class Genre(Enum):
    CHOPIN = 1
    BACH = 2
    BEETHOVEN = 3
    SCARLATTI = 4
    BALAD = 5
    NEW_AGE = 6

""" Converter Functions """
def changeSignatureToInteger(signature):
    """
        박자표 값을 서버데이터에 맞게 변환
    """
    for serverSignature in Signature:
        if serverSignature.name == signature:
            return serverSignature.value

    raise ValueError("This is not signature string data")

def changeGenreToInteger(genre):
    """
        장르 값을 서버데이터에 맞게 변환
    """
    resultData = None
    for serverGenre in Genre:
        if serverGenre.name == genre:
            resultData = serverGenre.value
            return resultData
    raise ValueError("This is not genre string data")
