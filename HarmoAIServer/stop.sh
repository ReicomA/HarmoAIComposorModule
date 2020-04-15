echo "stop"
CONFIG_ROOT="config.json"

# get pid
python_pid=$(ps -au | grep "python harmoaiserver.py $CONFIG_ROOT$" | awk '{print $2}')


# TODO 전처리 필요


# 프로세스 종료
kill -15 $python_pid