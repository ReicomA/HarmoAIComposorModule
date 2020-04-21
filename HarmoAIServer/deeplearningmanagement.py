import threading
import time

from datastruc.queue_requestdata import *

class DeepLearningManagement(threading.Thread):

    def __init__(self, requestQueue, config):
        # TODO 전처리 수행
        threading.Thread.__init__(self)
        self.requestQueue = requestQueue
        self.config = config
        self.conn = connection
        self.shutdownSignal = False
        self.deepLearningList = []
        self.readyQueue = RequestDataQueue(self.config.maxSize)

    # 쓰레드 종료
    def shutdown(self):
        self.shutdownSignal = True

    # 데이터 읽어오기
    def read(self):
        return self.requestQueue.get()