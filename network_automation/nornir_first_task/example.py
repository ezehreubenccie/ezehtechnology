from nornir import InitNornir


def my_task(task):
    print(task.host)

def main():
    nr = InitNornir
    nr.run(task=my_task)

if __name__== "__main__":
    main()
