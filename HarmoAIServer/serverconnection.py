import redis
from datastruc.config import Config
from datastruc.queue_connectiondata import ConnectionDataQueue
from datastruc.queue_requestdata import RequestDataQueue
from enum import Enum

# Redis Keys
class ServerConnectionKeyLabels(Enum):
    IPMAP = "IPMap"
    MAIN_PIPE = "DeepServerPipe"

class AdminIPMap(Enum):
    IP = "admin"
    VALUE = 0000

class ServerConnection:
    """
        Redis Server 통신용 클래스
        config: Server Config File
        userMap: 사용자 테이블
        connectionQueue: 연결 데이터 큐
        requestDataQueue: 요청 데이터 큐
        conn: StricRedis객체 연결이 종료된 경우 None 처리
        rawReader: 클라이언트로부터 데이터를 받을 때 사용하는 Subscribe(단방향 소켓이라 보면 된다.)
    """
    def __init__(self, config):
        if isinstance(config, Config) is False:
            raise TypeException("config must be Config")
        self.config = config
        self.userMap = {} # map[string]int
        self.connectionQueue = ConnectionDataQueue(self.config.maxQueueSize)
        self.requestDataQueue = RequestDataQueue(self.config.maxQueueSize)
        self.conn = None
        self.rawReader = None
    
    # 연결 시작
    def open(self):
        try:
            # 연결 시도
            self.conn = redis.StrictRedis(
                host=self.config.host,
                port=self.config.port,
                db=0,
                password=self.config.pswd,
                charset='utf-8'
            )

            # 기존의 IPMap이 존재하는지 확인(서버가 갑작스럽게 종료되는 경우)
            if self.conn.exists(ServerConnectionKeyLabels.IPMAP.value) == True:
                # TODO 데이터 갖고오기
                print("aleady exist")
            else:
                # 만들기
                self.conn.hset(ServerConnectionKeyLabels.IPMAP.value, AdminIPMap.IP.value, AdminIPMap.VALUE.value)
                # subscribe
                self.rawReader = self.conn.pubsub()
                self.rawReader.subscribe(ServerConnectionKeyLabels.MAIN_PIPE.value)
                
        except Exception as e:
            self.conn = None
            raise e
    
    # 연결 닫기
    def close(self, aleadyDisconnected=False):
        # ...

        # IpMAP 무효화
        if aleadyDisconnected is False:
            self.conn.delete(ServerConnectionKeyLabels.IPMAP.value)
            self.conn.connection_pool.disconnect()

        # 무효화
        self.conn = None
        self.rawReader = None

        # 큐 비우기
        self.connectionQueue.clear()
        self.requestDataQueue.clear()

    # 연결되어있는지 확인
    def isConnected(self):
        return self.conn != None

    def read(self):

        if self.isConnected() is False:
            raise Exception("disconnected with redis server")

        if self.rawReader == None:
            self.close(aleadyDisconnected=True)
            raise Exception("does not subscribe")
        
        # 데이터 확인
        rawData = self.rawReader.get_message()
        if rawData:
            return rawData['data']
        else:
            return None

    def send(self, pubChannel, data):

        if self.isConnected() is False:
            raise Exception("disconnected with redis server")
            
        try:
            resultInt = self.conn.publish(pubChannel, data)
            return resultInt == 1
        except Exception as e:
            raise e
