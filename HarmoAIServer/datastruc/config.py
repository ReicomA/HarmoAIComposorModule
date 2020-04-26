
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
import os.path
import json

# Config Name Labels
"""
    서버 설정 파일로 필요시
    추가 가능
"""
class ConfigNameLabels(Enum):
    """
        서버를 설정하기 위한 Config.json의 key들
        
        HOST: Redis 서버의 주소
        PORT: Redis Server를 접속하기 위한 포트
        PSWD: Redis Server를 접속하기 위한 패스워드
        MAX_QUEUE_SIZE: 각 시스템의 큐의 최대 크기를 설정
        MAX_NOTE_SIZE: AI 시스템이 최대로 작곡할 수 잇는 노트의 갯수(TODO 연구 필요)
        SERIAL: 연결관련 확인용 인증코드
        MODELS: AI 모델이 저장되어 있는 위치들(장르에  따라 다름)
        TMP_DIR = AI 작곡을 마치고 클라이언트로 보내기 전에 임시로 저장되는 파일의 위치
    """
    HOST = "host"
    PORT = "port"
    PSWD = "pswd"
    MAX_QUEUE_SIZE = "max_queue_size"
    MAX_NOTE_SIZE = "max_note_size"
    USE_GPU_VALUE = "use_gpu_value"
    SERIAL = "serial"
    MODELS = "models"
    TMP_DIR = "tmp_dir"

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
                self.tmpDir = jsonDataSet[ConfigNameLabels.TMP_DIR.value]
                self.DLMap = {}

                i = 0
                DLKeys = jsonDataSet[ConfigNameLabels.MODELS.value].keys()

                # 모델 파일 루트 갖고오기
                for key in DLKeys:
                    self.DLMap[i+1] = jsonDataSet[ConfigNameLabels.MODELS.value][key]
                    i += 1

        except Exception as e:
            raise e

        self.fileRooot = configRoot

