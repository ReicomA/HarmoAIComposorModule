
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
            """ PT.1 Read Data """
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
                
                """ PT.2 Check SendData """
            time.sleep(0.001)
    except KeyboardInterrupt as e:
        conn.close()
        sys.exit()
    
    # test close
    conn.close()


