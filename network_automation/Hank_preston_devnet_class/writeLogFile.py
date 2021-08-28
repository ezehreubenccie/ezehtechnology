#!/usr/bin/env python

from datetime import datetime

log_file = 'logfile.log'

def read_log(log):
    with open(log) as f:
       print(f.read())

def write_log(log, name):
    log_time = str(datetime.now())
    with open(log, 'a') as f:
        f.writelines('Entry logged at: {} by {}\n'.format(log_time, name))


if __name__ == '__main__':
    name = input('What is your name? ')

    print('Adding new log entry')
    write_log(log_file, name)
    print("")
    print('Log File Contents')
    print('-----------------')
    read_log(log_file)
