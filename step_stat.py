import configparser
import datetime
import os

import fitbit
from plotly.graph_objs import Scatter
from plotly.offline import plot
import plotly.graph_objs as go

from running_object import get_runs

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

activities_steps = authd_client.time_series('activities/steps', period='3m')
activities_runs = get_runs(authd_client)

run_dates = [run.date for run in activities_runs]
run_steps = [run.step for run in activities_runs]
run_dicts = dict(zip(run_dates, run_steps))

holiday_first_date = datetime.date(2017, 8, 21)
invalid_dates = [holiday_first_date + datetime.timedelta(days=x) for x in range(0, 7)]
invalid_dates.append(datetime.date(2017, 9, 21))
invalid_dates.append(datetime.date(2017, 9, 22))
invalid_dates.append(datetime.date(2017, 9, 25))
di = {}
for a in activities_steps['activities-steps']:
    dm = a['dateTime']
    date_parts = dm.split('-')
    today = datetime.date(int(date_parts[0]), int(date_parts[1]), int(date_parts[2]))
    if (today.weekday() < 5) and today not in invalid_dates and int(a['value']) != 0:
        di[today] = [a['value']]

ordered_dates = di.keys()
sorted(ordered_dates)
sepfile = []
y_run_steps_steps = []
good_days_cnt = 0
steps_sum = 0
for date in ordered_dates:
    daily_steps = int(di[date][0])
    good_days_cnt = good_days_cnt + 1 if daily_steps > 8500 else good_days_cnt
    steps_sum += daily_steps
    sepfile.append((date, daily_steps))
    if date in run_dicts:
        y_run_steps_steps.append(int(di[date][0])-run_dicts[date])
    else:
        y_run_steps_steps.append(di[date][0])

x_all_steps_dates = [date for (date, value) in sepfile]
y_all_steps_steps = [value for (date, value) in sepfile]

# Create a trace
all_steps = Scatter(
    x=x_all_steps_dates,
    y=y_all_steps_steps,
    mode='lines+markers',
    name='Daily steps',
    fill='tonexty'
)

run_steps = Scatter(
    x=x_all_steps_dates,
    y=y_run_steps_steps,
    mode='lines+markers',
    name='Run steps',
    fill='tozeroy'
)

reference_line = Scatter(
    x=x_all_steps_dates,
    y=[8500] * len(x_all_steps_dates),
    name='Reference line',
    line=dict(
        color=('rgb(205, 12, 24)'),
        width=5)
)

good_days_description="8500 steps days: <b>{}/{}</b>".format(good_days_cnt, len(x_all_steps_dates))
avg_steps_description="Average daily steps: <b>{}</b>".format(round(steps_sum / len(x_all_steps_dates), 2))

data = [all_steps, run_steps, reference_line]

layout = go.Layout(
    annotations=[
        dict(
            showarrow=False,
            x=0.1004254919715793,
            y=1.16191064079952971,
            xref='paper',
            yref='paper',
            align = "left",
            text=good_days_description
        ),
        dict(
            showarrow=False,
            x=0.1004254919715793,
            y=1.10191064079952971,
            xref='paper',
            yref='paper',
            align = "left",
            text=avg_steps_description
        )
    ]
)
fig = go.Figure(data=data, layout=layout)
plot(fig, filename='simple-annotation.html')
