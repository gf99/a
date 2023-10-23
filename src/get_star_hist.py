from github import Github
import pandas as pd
import numpy as np
import datetime
import sys
import re
import requests
import datetime
import pytz
from plot2svg import Bar, Text

token = sys.argv[1]


# %%


def get_star(repo_name="guofei9987/scikit-opt"):
    g = Github(token)

    repo = g.get_repo(repo_name)
    star_history = [[stargazer.user.login, stargazer.starred_at]
                    for stargazer in repo.get_stargazers_with_dates()]
    star_history = pd.DataFrame(star_history, columns=['login', 'time'])
    star_history.set_index(keys='time', inplace=True)

    return star_history


# %% 画出bar图

def bar(data, mark='█'):
    height, length = data.max(), data.shape[0]

    canvas = np.zeros(shape=(height, 3 * length))
    for i, j in enumerate(data):
        canvas[height - j:, 3 * i:3 * i + 2] = 1

    res = '\n'.join([''.join([mark if col == 1 else ' ' for col in row]) for row in canvas])
    return res


# %% 打印相关信息
def print_detail(star_history_dt, goal=2000):
    res = ''
    star_history_cumsum = star_history_dt.cumsum()
    star_today = star_history_cumsum.iloc[-1, 0]
    star_daily_avg = (star_today - star_history_cumsum.iloc[-201, 0]) / 200
    # %%

    res += '当前⭐️{}个，近200日{}⭐️/day\n'.format(star_today, star_daily_avg)

    # %%
    diff_stars = goal - star_today
    diff_days = diff_stars / star_daily_avg
    object_date = star_history_cumsum.index[-1].date() + datetime.timedelta(days=diff_days)

    # %%
    res += '距离{} ⭐️还有{}个，{}天，是{}\n'.format(goal
                                           , diff_stars
                                           , np.round(diff_days, 2), object_date)

    delta_date = datetime.date(year=2022, month=3, day=31) - star_history_cumsum.index[-1].date()
    delta_date = delta_date.days

    res += '距离2022年3月31日还有{}天（{}月），届时star数量是{}\n'.format(delta_date, delta_date / 30
                                                         , star_today + star_daily_avg * delta_date)
    return res


# %% sko

star_history = get_star("guofei9987/scikit-opt")
star_history_dt_sko = star_history.resample(rule='d').count()
data_sko = star_history_dt_sko.iloc[-26:, 0].values

star_history_cumsum_sko = star_history_dt_sko.cumsum()
star_today_sko = star_history_cumsum_sko.iloc[-1, 0]
star_daily_avg_sko = (star_today_sko - star_history_cumsum_sko.iloc[-201, 0]) / 200
res_sko = 'sko 当前⭐️{}个，近200日{}⭐️/day\n'.format(star_today_sko, star_daily_avg_sko)

# %%

star_history = get_star("guofei9987/blind_watermark")
star_history_dt_bw = star_history.resample(rule='d').count()
data_bw = star_history_dt_bw.iloc[-26:, 0].values

star_history_cumsum_bw = star_history_dt_bw.cumsum()
star_today_bw = star_history_cumsum_bw.iloc[-1, 0]
star_daily_avg_bw = (star_today_bw - star_history_cumsum_bw.iloc[-201, 0]) / 200
res_bw = 'bm 当前⭐️{}个，近200日{}⭐️/day'.format(star_today_bw, star_daily_avg_bw)

# %%
star_history_dt_total_ = pd.concat([star_history_dt_sko.cumsum(), star_history_dt_bw.cumsum()]
                                   , axis=1).fillna(method='ffill')

star_history_dt_total = star_history_dt_total_.iloc[:, 0] + star_history_dt_total_.iloc[:, 1]

latest_stars, latest_day = star_history_dt_total[-1], star_history_dt_total.index[-1]
star_everyday_200 = (star_history_dt_total[-1] - star_history_dt_total[-201]) / 200

# 这里用总的star数量，而不是两个相加
import requests,json
r = requests.get('https://www.guofei.site/pages/achievement.json')
star_cnt = json.loads(r.text)['star_cnt']
star_cnt = int(star_cnt)



diff_stars = 10000 - star_cnt
diff_days = diff_stars / star_everyday_200
# object_date = star_history_cumsum.index[-1].date() + datetime.timedelta(days=diff_days)

target_day = latest_day + datetime.timedelta(days=diff_days)

target = '还差{},是{}年后，是{}\n'.format(diff_stars, round(diff_days / 365, 3),
                                   target_day.strftime('%Y-%m-%d'))

# 图表名

Text(width=500, height=None, color="red",
     data=datetime.datetime.now(tz=pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S') \
          + target + res_sko + res_bw).save_svg('data/text.svg')

print(target)
print(res_sko)
print(res_bw)

Bar(width=500, height=None, color="red", data=data_sko).save_svg('data/sko.svg')
Bar(width=500, height=None, color="red", data=data_bw).save_svg('data/bw.svg')
