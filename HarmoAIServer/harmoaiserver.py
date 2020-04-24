from datastruc.requestdata import *
from datastruc.queue_requestdata import *

from datastruc.connectiondata import *
from datastruc.queue_connectiondata import *

from datastruc.config import Config
from serverconnection import ServerConnection

from data_translater import *

# Thread Import
from clientmanagement import ClientManagement
from deeplearningmanagement import DeepLearningManagement

import sys
import time
import signal
import json

if __name__ == "__main__":

    # Signal Handling
    def sighandler(signum, frame):
        # Exit Thread
        conn.close()
        clientManagementThread.shutdown()
        dlThread.shutdown()
        sys.exit()
    
    # get config info
    configRoot = sys.argv[1]
    config = Config(configRoot)
    conn = ServerConnection(config)
    conn.open()

    # dataQueues
    connectionQueue = ConnectionDataQueue(config.maxQueueSize)
    requestQueue = RequestDataQueue(config.maxQueueSize)

    # set Translater
    translater = DataTranslater(connectionQueue, requestQueue)

    # set Threads
    dlThread = DeepLearningManagement(requestQueue, config, conn)
    clientManagementThread = ClientManagement(connectionQueue, config, conn, dlThread)

    # run Threads
    try:
        clientManagementThread.start()
        dlThread.start()
    except Exception as e:
        # 에러 처리
        print(e)
        sys.exit()

    # Main Thread Loop START
    try:
        signal.signal(signal.SIGTERM, sighandler)
        while True:
            data = conn.read()
            transSignal = None
            # Data를 수신 받았을 경우
            if data != None:
                try:
                    if isinstance(data, bytes) is True:
                        transSignal = translater.translateData(data)
                except Exception as e:
                    print("trash data")
                finally:
                    if transSignal == None:
                        print("trash data")
            time.sleep(0.001)
    except KeyboardInterrupt as e:
        conn.close()
        sys.exit()
    
    # test close
    conn.close()


