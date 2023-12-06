import os
import runpy
import time

if __name__ == '__main__':
    os.chdir('../')
    directory = 'inputs'
    startTime = time.time()
    for filename in os.listdir(directory):
        pyFileName = 'src/' + filename + '.py'
        print(pyFileName)
        runpy.run_path(pyFileName)
    print("\033[96mTime to execute all: %s seconds\033[0m" % (time.time() - startTime))
