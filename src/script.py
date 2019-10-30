import os
import time

for it in range(3,10):
	os.system('python src/main.py '+str(it))
	time.sleep(5)