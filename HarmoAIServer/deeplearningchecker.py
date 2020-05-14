# -*- coding: utf-8 -*-
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

from deeplearningProcessor import DeepLearningProcessor
from datastruc.requestdata import *
from dlprocess import DLprocess
import threading
from multiprocessing import Process
from serverconnection import ServerConnectionKeyLabels
import os.path
import os
import redis

# 딥러닝 프로세스가 정상적으로 동작하는 지 확인하는 클래스
# 쓰레드 목적으로 돌아가므로 Thread 상속
class DeepLearningChecker(threading.Thread):
    """
        conn: Redis 연결부
        config: 설정 데이터
        requestData: 클라이언트로부터 받은 요청데이터
        userSubKey: 유저 subscribe Key (Redis에 저장되어있으므로 접속해서 구해야됨)
        resultTmpRoot = 결과물 파일루트
        isShutdown: 쓰레드 종료 여부 (DeepLearningManagement에서 관리)
    """
    def __init__(self, requestData, config, conn):
        threading.Thread.__init__(self)
        self.conn = conn
        self.config = config
        self.requestData = requestData
        self.userSubKey = self.conn.conn.hget(
            ServerConnectionKeyLabels.IPMAP.value, 
            self.requestData.ip).decode('utf-8')

        self.requestData = requestData
        self.resultTmpRoot = self.config.tmpDir + "/" + self.userSubKey + ".mid"
        self.isShutdown = True

    """ 딥러닝 프로세스 생성(시작 아님) """
    def makeDLProcess(self):
        modelRoot = self.config.DLMap[self.requestData.genre]
        noteSize = self.requestData.noteSize
        resultTmpRoot = self.resultTmpRoot
        useGpuValue = self.config.useGpuValue
        
        dlProcess = Process(target=DLprocess, args=(modelRoot, noteSize, resultTmpRoot, useGpuValue,))

        return dlProcess

    # 결과물이 추출되었는지 확인
    def checkResult(self):
        return os.path.isfile(self.resultTmpRoot)

    """  Redis를 경유하여 클라이언트에게 결과물 전송 """
    def submit(self):
        try:
            # 파일 열고 string으로 받기
            datas = b""
            with open(self.resultTmpRoot, "rb") as f:
                bdata = f.read(1)
                while bdata != b"":
                    datas += bdata
                    bdata = f.read(1)
            
            """ 해당 유저가 subscribe하고 있는 key를 통해 데이터 전달"""
            pubObj = self.conn.conn.pubsub()
            self.conn.conn.publish(self.userSubKey, datas)
            
            # 임시파일 삭제
            os.remove(self.resultTmpRoot)
        except Exception as e:
            raise e
        
    
    # 쓰레드가 돌아가는 부분
    def run(self):

        # Process 생성 및 실행
        try:
            process = self.makeDLProcess()
            process.start()

            # 프로세스 끝날 때 까지 기다림
            process.join()

            # 결과물 확인
            if self.checkResult() is True:
                self.submit() # 전송
                print("success")
            else:
                print("failed")
                
        except Exception as e:
            print(e)
            self.isShutdown = True

        self.isShutdown = True

    