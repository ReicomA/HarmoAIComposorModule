from enum import Enum

class RequestDataTypeLabel(Enum):
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
    else:
        raise ValueError("This is not signature string data")

def changeGenreToInteger(genre):
    """
        장르 값을 서버데이터에 맞게 변환
    """
    for serverGenre in Genre:
        if serverGenre.name == genre:
            return serverGenre.value
    else:
        raise ValueError("This is not genres string data")