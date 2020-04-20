from server import run as srun
from client.network import run as crun
import threading


what = int(input("0-server: \n$"))

if what == 0:
    network_thread = threading.Thread(target=srun, name="network")
    network_thread.start()
    print("server started!")
    network_thread.join()
    print("server Closed!")
else:
    network_thread = threading.Thread(target=crun, name="network")
    network_thread.start()
    print("server started!")
    network_thread.join()
    print("server Closed!")
