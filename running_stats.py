import configparser
import datetime
import os

import fitbit
from plotly.graph_objs import Bar
from plotly.offline import plot

from running_object import get_runs


def get_week_number(date):
    """
    :param date date: date object
    :return: Number of the week
    :rtype: int
    """
    return date.isocalendar()[1]


config = configparser.ConfigParser()
folder_name = os.path.dirname(os.path.realpath(__file__))
config.read(folder_name + os.sep + 'fitbit_configs.ini', encoding='UTF-8')

CLIENT = config.get('DEFAULT', 'CLIENT')
SECRET = config.get('DEFAULT', 'SECRET')
ACCESS_TOKEN = config.get('DEFAULT', 'ACCESS_TOKEN')
REFRESH_TOKEN = config.get('DEFAULT', 'REFRESH_TOKEN')
authd_client = fitbit.Fitbit(CLIENT, SECRET,
                             access_token=ACCESS_TOKEN,
                             refresh_token=REFRESH_TOKEN)

runs = get_runs(authd_client)
weeks_accuracy = {}
for r in runs:
    # print("Date: {0}\tSpeed: {1:.2f}\tDistance: {2:.2f}\tDuration: {3}".format(r.date, r.get_speed(), r.distance,
    #                                                                            r.get_duration()))
    week_number = str(get_week_number(r.date))
    if week_number in weeks_accuracy:
        weeks_accuracy[week_number] += 1
    else:
        weeks_accuracy[week_number] = 1

week_keys = weeks_accuracy.keys()
sorted(week_keys)
x = []
y = []
for wn in week_keys:
    x.append(wn)
    y.append(weeks_accuracy[wn])

data = [Bar(
            x=x,
            y=y
    )]

plot(data, filename='basic-bar')
