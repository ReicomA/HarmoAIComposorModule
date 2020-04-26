import threading
import time

from datastruc.queue_requestdata import *
from dlprocess import DLprocess
from serverconnection import ServerConnectionKeyLabels
from deeplearningchecker import DeepLearningChecker

class DeepLearningManagement(threading.Thread):

    def __init__(self, requestQueue, config, conn):
        # TODO 전처리 수행
        threading.Thread.__init__(self)
        self.requestQueue = requestQueue
        self.config = config
        self.conn = conn
        self.shutdownSignal = False

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

            checker = DeepLearningChecker(data, self.config, self.conn)
            checker.start()
            
            self.listMutex.acquire()
            self.deepLearningList.append(checker)
            self.listMutex.release()
            return True
    
    """ 진행중인 프로세스 관리 """
    def manageProcessList(self):
        if self.deepLearningList:
            for idx in range(0, len(self.deepLearningList)):
                if self.deepLearningList[idx].isShutdown is True:
                    self.listMutex.acquire()
                    del self.deepLearningList[idx]
                    self.listMutex.release()
    

    # 쓰레드가 시작될 때 작동
    def run(self):
        while self.shutdownSignal is False:
            
            # 딥러닝 리스트가 꽉 차있지 않는 경우에만 데이터를 읽어들인다.
            if len(self.deepLearningList) < self.config.useGpuValue:
                reqData = self.read()
                # 데이터를 불러들이는 데 성공한 경우
                if reqData != None:
                    self.generate(reqData)

            # 꺼져있는 딥러닝 확인 쓰레드가 있는지 확인
            self.manageProcessList()

            time.sleep(0.001)