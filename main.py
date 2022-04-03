# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

arrival_time_threshold = 2
import datetime
import pandas as pd
# t1 = datetime.time.now() + datetime.timedelta(hours=3)
# t2 = datetime.time.now() + datetime.timedelta(minutes=60)
# print(t1)
# print(t2)

add_time = datetime.timedelta(hours=2)
t2 = datetime.datetime.now() + add_time
print(pd.to_datetime(t2).time())

print(add_time)


# HOW TO ADD TIME WITH TIME