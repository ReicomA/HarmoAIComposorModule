from datastruc.requestdata import *
from datastruc.queue_requestdata import *

from datastruc.connectiondata import *
from datastruc.queue_connectiondata import *

from datastruc.config import Config

import sys

# get config info
configRoot = sys.argv[1]
config = Config(configRoot)