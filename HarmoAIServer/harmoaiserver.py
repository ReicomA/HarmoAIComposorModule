from datastruc.requestdata import *
from datastruc.queue_requestdata import *

from datastruc.connectiondata import *
from datastruc.queue_connectiondata import *

from datastruc.config import Config
from serverconnection import ServerConnection

import sys
import time

# get config info
configRoot = sys.argv[1]
config = Config(configRoot)
conn = ServerConnection(config)
conn.open()

try:
    while True:
        print(conn.read())
        time.sleep(0.5)
except KeyboardInterrupt as e:
    conn.close()
    sys.exit()

# test close
conn.close()