import RLClient
import time
for i in range(30):
    obs = RLClient.SocketClient('cur_price')
    time.sleep(2)
    print(obs)


