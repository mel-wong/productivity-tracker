# Contains methods for productivity tracker

import time
from datetime import datetime

import pandas
from win32gui import GetForegroundWindow, GetWindowText
from threading import Thread
from queue import Queue, Empty


# method to check user input to start/stop program
def user_input(q):
    while True:
        val = input('Enter Y to stop tracking: ')

        if val.lower() == 'y':
            print('Tracker Stopped')
            q.put('stop')
            break

        else:
            continue


# get the name of the open window
def get_window():
    return GetWindowText(GetForegroundWindow())


# check if the foreground window has changed
def window_changed(current_window, prev_window):
    if current_window == prev_window:
        return False
    elif current_window != prev_window:
        return True


# update hash table of windows and duration
def update_table(htable, window, duration):
    if htable.get(window) is None:
        htable[window] = duration
    else:
        htable[window] += duration


# print time spent on each window
def print_data(htable):
    print(htable.items())


def main_tracker(input_queue, prev_window, prev_end_time):

    while True:
        try:
            status = input_queue.get(block=True, timeout=1)
            input_queue.task_done()
            if status == 'stop':
                print('Tracker has stopped')
                print_data(data_table)
                break

        except Empty:
           # start_time = datetime.now()
            new_window = get_window()

            if window_changed(new_window, prev_window):
                end_time = datetime.now()
                duration = pandas.Series(end_time - prev_end_time)
                duration_float = float(duration.dt.seconds)
                prev_end_time = end_time
                prev_window = new_window

                update_table(data_table, new_window, duration_float)


if __name__ == '__main__':
    # key = window name, value = time spent on window
    data_table = dict()

    input_queue = Queue()

    # Keep asking to start
    while True:
        val = input('Start tracker? (Y): ')
        if val.lower() == 'y':
            break
        else:
            continue

    prev_window = get_window()
    update_table(data_table, prev_window, 0)
    prev_end_time = datetime.now()

    t1 = Thread(target=main_tracker,args=(input_queue,prev_window,prev_end_time))
    t1.start()

    t2 = Thread(target=user_input, args=(input_queue,))
    t2.start()

    input_queue.join()
    t2.join()
    t1.join()


