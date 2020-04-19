from enum import Enum

class DataTranslater(Enum):
    CONNECT = 0,
    REQUEST = 1,
    DISCONNECT = -1

"""클라이언트로부터 들어온 데이터를 분석 해서 원하는 형태로 추출"""
class DataTranslater:

    def __init__(self, connectionQueue, requestQueue):
        
        self.connectionQueue = connectionQueue
        self.requestQueue = requestQueue

    def translateData(data):
        if isinstance(data, bytes) is True:
            try:
                dataSet = json.loads(data.decode('utf-8'))
                dataType = dataSet['type']
            
                if isinstance(dataType, int) is True:
                    pass
                else:
                    raise TypeError("Wrong Type")
            # 정확하지 않은 데이터가 발견했을 경우 바로 제거
            except Exception as e:
                return None
        else:
            return None
                
