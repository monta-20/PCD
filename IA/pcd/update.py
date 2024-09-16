import constants as ct
import databaseoperations as do
import model as m
from multiprocessing import Process
import time

def update_wrapper(name):
    do.UpdateAll(name)

if __name__ == "__main__":
    # Run UpdateAll for both updateNames in separate processes
    p1 = Process(target=update_wrapper, args=(ct.updateNames[0],))
    p2 = Process(target=update_wrapper, args=(ct.updateNames[1],))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    time.sleep(50)


    # Continue with the rest of your code
    do.NewsToVectorAll(10)
    m.UpdateAllForcast()



