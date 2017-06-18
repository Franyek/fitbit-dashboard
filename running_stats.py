import configparser
import datetime
import os

import fitbit
from plotly.graph_objs import Bar
from plotly.offline import plot

from running_object import Running


def get_week_number(date):
    """
    :param str date: String which is a date, format: YYYY-MM-DD
    :return: Number of the week
    :rtype: int
    """
    date_parts = date.split('-')
    d = datetime.date(int(date_parts[0]), int(date_parts[1]), int(date_parts[2]))
    return d.isocalendar()[1]


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

sorting = 'desc'
offset = 0
beforeDate = '2017-06-18'
runnings = []
ONE_MILE = 1.609344
response = authd_client.make_request(
    'https://api.fitbit.com/1/user/-/activities/list.json?beforeDate={beforeDate}&offset={offset}&limit=20&sort={sorting}'.format(
        offset=offset,
        beforeDate=beforeDate,
        sorting=sorting))
cnt = 1
for act in response['activities']:
    if (act['activityName'] == 'Run') and (act['logType'] == 'mobile_run'):
        runnings.append(Running(act['activeDuration'], act['distance'] * ONE_MILE, act['startTime'][0:10]))
while response['pagination']['next'] != '':
    url = response['pagination']['next']
    response = authd_client.make_request(url)
    cnt += 1
    print(cnt)
    for act in response['activities']:
        if (act['activityName'] == 'Run') and (act['logType'] == 'mobile_run'):
            runnings.append(Running(act['activeDuration'], act['distance'] * ONE_MILE, act['startTime'][0:10]))

weeks_accuracy = {}
for r in runnings:
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
