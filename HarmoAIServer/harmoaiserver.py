from datastruc.requestdata import *
from datastruc.queue_requestdata import *

from datastruc.connectiondata import *
from datastruc.queue_connectiondata import *

from datastruc.config import Config
from serverconnection import ServerConnection

import sys
import time
import signal
import json

if __name__ == "__main__":

    """ 테스트용 코드 입니다
        클라이언트 테스트가 끝나면 실제 구현에 들어갈 예정
    """

    # Signal Handling
    def sighandler(signum, frame):
        conn.close()
        sys.exit()
    
    # get config info
    configRoot = sys.argv[1]
    config = Config(configRoot)
    conn = ServerConnection(config)
    conn.open()

    connectionQueue = ConnectionDataQueue(config.maxQueueSize)
    requestQueue = RequestDataQueue(config.maxQueueSize)

    translater = DataTranslater(connectionQueue, requestQueue)

    try:
        signal.signal(signal.SIGTERM, sighandler)
        while True:
            data = conn.read()
            # Data를 수신 받았을 경우
            if data != None:
                try:
                    if isinstance(data, bytes) is True:
                        dataStr = data.decode('utf-8')
                        dataSet = json.loads(dataStr)
                        print(dataSet['type'])
                except Exception as e:
                    print(e)
                    print("trash data")
            
            time.sleep(0.001)
    except KeyboardInterrupt as e:
        conn.close()
        sys.exit()
    
    # test close
    conn.close()


