from server.network import run as srun
from client.network import run as crun
import threading
import queue
import json
from client.graphics import main


what = int(input("0-server: \n$"))

if what == 0:
    network_thread, receive, send = srun("localhost")
else:
    main()

