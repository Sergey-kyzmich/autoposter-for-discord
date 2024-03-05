id = 679385458731384832
from subprocess import Popen
import sys
import time
import json
import os
derictori = os.getcwd().replace("\\", "/")+f"/baze/{id}/"
#from active import active
with open(derictori+"on_list.json", "r") as read_file:
    on_list = json.load(read_file)
for i in range(1, 9):
    if on_list[str(i)]==True:
        Popen([sys.executable,derictori+ str(i)+".py"])
while True:
    time.sleep(1000000)