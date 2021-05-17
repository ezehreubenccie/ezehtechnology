import threading

#creating threads
def create_threads(dict1, function):

    threads = []

    for device in dict1:
        th = threading.Thread(target=function, args=(device,)) # args is a tuple with a single element
        th.start()
        threads.append(th)

    for th in threads:
        th.join()