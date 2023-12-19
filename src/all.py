import os
import runpy
import time

if __name__ == '__main__':
    os.chdir('../')
    startTime = time.time()
    for filename in os.listdir('./src'):
        if filename.split('.')[0].isnumeric():
            runpy.run_path('src/'+filename)
    print("\033[96mTime to execute all: %s seconds\033[0m" % (time.time() - startTime))
