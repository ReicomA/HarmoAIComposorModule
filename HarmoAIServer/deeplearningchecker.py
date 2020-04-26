from deeplearningProcessor import DeepLearningProcessor
from datastruc.requestdata import *
from dlprocess import DLprocess
import threading
from multiprocessing import Process
from serverconnection import ServerConnectionKeyLabels
import os.path
import os
import redis

class DeepLearningChecker(threading.Thread):

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


    def makeDLProcess(self):
        modelRoot = self.config.DLMap[self.requestData.genre]
        noteSize = self.requestData.noteSize
        resultTmpRoot = self.resultTmpRoot
        useGpuValue = self.config.useGpuValue
        
        dlProcess = Process(target=DLprocess, args=(modelRoot, noteSize, resultTmpRoot, useGpuValue,))

        return dlProcess

    def checkResult(self):
        return os.path.isfile(self.resultTmpRoot)

    def submit(self):
        try:
            # 파일 열고 string으로 받기
            datas = b""
            with open(self.resultTmpRoot, "rb") as f:
                bdata = f.read(1)
                while bdata != b"":
                    datas += bdata
                    bdata = f.read(1)
            
            pubObj = self.conn.conn.pubsub()
            self.conn.conn.publish(self.userSubKey, datas)
            
            os.remove(self.resultTmpRoot)
        except Exception as e:
            raise e
        
    
    # 쓰레드가 돌아가는 부분
    def run(self):

        # Process 생성 및 실행
        try:
            process = self.makeDLProcess()
            process.start()
            process.join()

            if self.checkResult() is True:
                self.submit()
                print("success")
            else:
                print("failed")
                
        except Exception as e:
            print(e)
            self.isShutdown = True

        self.isShutdown = True

    