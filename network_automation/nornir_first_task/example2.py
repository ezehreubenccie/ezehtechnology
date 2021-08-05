import random
import time
from nornir import InitNornir

#nr = InitNornir()
#print(nr)
#print(type(nr))
#print(dir(nr))
#attribs = dir(nr)
#print(attribs)
#for attrib in attribs:
#    print(attrib)
def my_task(x1):
    time.sleep(random.random())
    print(x1.host)

def main():
    nr = InitNornir()
    nr.run(task=my_task)

if __name__== "__main__":
    main()
