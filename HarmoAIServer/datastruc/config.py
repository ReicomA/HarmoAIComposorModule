from enum import Enum
import os.path
import json

# Config Name Labels
"""
    서버 설정 파일로 필요시
    추가 가능
"""
class ConfigNameLabels(Enum):
    HOST = "host"
    PORT = "port"
    PSWD = "pswd"
    MAX_QUEUE_SIZE = "max_queue_size"
    MAX_NOTE_SIZE = "max_note_size"
    USE_GPU_VALUE = "use_gpu_value"
    SERIAL = "serial"
    

class Config:
    def __init__(self, configRoot):
        #check root type
        if isinstance(configRoot, str) is False:
            raise TypeError("Config Root must be string")

        # check file exist
        if os.path.isfile(configRoot) is False:
            raise FileNotFoundError("config file is not exist")

        # json set
        try:
            with open(configRoot, 'r') as configFile:
                jsonDataSet = json.load(configFile)

                self.host = jsonDataSet[ConfigNameLabels.HOST.value]
                self.port = jsonDataSet[ConfigNameLabels.PORT.value]
                self.pswd = jsonDataSet[ConfigNameLabels.PSWD.value]
                self.maxQueueSize = jsonDataSet[ConfigNameLabels.MAX_QUEUE_SIZE.value]
                self.maxNoteSize = jsonDataSet[ConfigNameLabels.MAX_NOTE_SIZE.value]
                self.useGpuValue = jsonDataSet[ConfigNameLabels.USE_GPU_VALUE.value]
                self.serial = jsonDataSet[ConfigNameLabels.SERIAL.value]
        except Exception as e:
            raise e

        self.fileRooot = configRoot

