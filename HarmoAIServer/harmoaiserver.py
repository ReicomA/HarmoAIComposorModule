from datastruc.requestdata import *
from datastruc.queue_requestdata import *

from datastruc.connectiondata import *
from datastruc.queue_connectiondata import *

from datastruc.config import Config
from serverconnection import ServerConnection

import sys
import time
import signal

if __name__ == "__main__":

    # Signal Handling
    def sighandler(signum, frame):
        conn.close()
        sys.exit()
    
    # get config info
    configRoot = sys.argv[1]
    config = Config(configRoot)
    conn = ServerConnection(config)
    conn.open()

    try:
        signal.signal(signal.SIGTERM, sighandler)
        while True:
            print(conn.read())
            time.sleep(0.5)
    except KeyboardInterrupt as e:
        conn.close()
        sys.exit()
    
    # test close
    conn.close()


