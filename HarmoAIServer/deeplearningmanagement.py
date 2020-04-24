import threading
import time

from datastruc.queue_requestdata import *

class DeepLearningManagement(threading.Thread):

    def __init__(self, requestQueue, config, conn):
        # TODO 전처리 수행
        threading.Thread.__init__(self)
        self.requestQueue = requestQueue
        self.config = config
        self.conn = conn
        self.shutdownSignal = False
        self.conn = conn

        self.deepLearningList = []
        self.listMutex = threading.Lock()

    # 쓰레드 종료
    def shutdown(self):
        self.shutdownSignal = True

    # 데이터 읽어오기
    def read(self):
        return self.requestQueue.get()

    """
    딥러닝 모듈 실행
    리스트가 다 찬 경우 False
    리스트가 비어있어서 프로세스를 실행한 경우 True
    """
    def generate(self, data):

        """ 진행되고 있는 딥러닝 상태 확인 """
        if len(self.deepLearningList) >= self.config.useGpuValue:
            return False
        else:
            """ TODO 딥러닝 프로세스 실행 """
            print("deepLearning Start!")
            # 딥러닝 리스트에 추가
            self.listMutex.acquire()
            self.deepLearningList.append(data)
            self.listMutex.release()
            print(self.deepLearningList)
            return True
    
    """
        보통 딥러닝 프로세스는 딥러닝 수행이 끝나면
        저절로 프로세스가 사라진다.
        그러나 리스트에서는 남을 수 있으므로 ip를 식별자로 잡고 제거한다.
    """
    def delProcessInfo(self, targetIp):
        """ TODO 데이터 문법 판정 """

        for idx in range(0, len(self.deepLearningList)):
            if self.deepLearningList[idx].ip == targetIp:

                self.listMutex.acquire()
                del self.deepLearningList[idx]
                self.listMutex.release()

                print("deep learning End!")
                print(self.deepLearningList)
                return True
        return False 

    # 쓰레드가 시작될 때 작동
    def run(self):
        while self.shutdownSignal is False:
            
            # 딥러닝 리스트가 비어있는 경우에만 데이터를 읽어들인다.
            if len(self.deepLearningList) < self.config.useGpuValue:
                reqData = self.read()
                # 데이터를 불러들이는 데 성공한 경우
                if reqData != None:
                    self.generate(reqData)
                else:
                    time.sleep(0.001)
                    continue
            else:
                time.sleep(0.001)
                continue