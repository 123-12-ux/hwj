import math
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

plt.rcParams['font.family'] = ['SimHei']


def tem_curve(data):
    """温度曲线绘制"""
    tem_low = list(data['最低气温'])
    tem_high = list(data['最高气温'])

    for i in range(len(tem_low)):  # 处理数据长度动态变化
        if pd.isna(tem_low[i]):  # 使用pandas的isna方法检查NaN
            tem_low[i] = tem_low[i - 1]  # 用前一个值填充
        if pd.isna(tem_high[i]):  # 使用pandas的isna方法检查NaN
            tem_high[i] = tem_high[i - 1]  # 用前一个值填充

    tem_high_ave = sum(tem_high) / len(tem_high)
    tem_low_ave = sum(tem_low) / len(tem_low)
    tem_max = max(tem_high)
    tem_max_data = tem_high.index(tem_max)
    tem_min = min(tem_low)
    tem_min_data = tem_low.index(tem_min)

    x = range(1, len(tem_high) + 1)
    plt.figure(1)
    plt.plot(x, tem_high, color='red', label='高温')
    plt.scatter(x, tem_high, color='red')
    plt.plot(x, tem_low, color='blue', label='低温')
    plt.scatter(x, tem_low, color='blue')

    plt.plot([1, len(tem_high)], [tem_high_ave, tem_high_ave], c='black', linestyle='--')
    plt.plot([1, len(tem_low)], [tem_low_ave, tem_low_ave], c='black', linestyle='--')
    plt.legend()
    plt.text(tem_max_data + 0.15, tem_max + 0.15, str(tem_max), ha='center', va='bottom', fontsize=10.5)
    plt.text(tem_min_data + 0.15, tem_min + 0.15, str(tem_min), ha='center', va='bottom', fontsize=10.5)
    plt.xticks(x)
    plt.title('未来14天高气温变化曲线图')
    plt.xlabel('未来天数/天')
    plt.ylabel('摄氏度/℃')
    plt.show()


def change_wind(wind):
    """改变风向"""
    wind_direction_map = {
        "北风": 90, "南风": 270, "西风": 180, "东风": 360,
        "东北风": 45, "西北风": 135, "西南风": 225, "东南风": 315
    }
    return [wind_direction_map.get(w, w) for w in wind]


def wind_radar(data):
    '''风向雷达图'''
    wind1 = list(data['风向1'])
    wind2 = list(data['风向2'])
    wind_speed = list(data['风级'])

    wind1 = change_wind(wind1)
    wind2 = change_wind(wind2)

    degs = np.arange(45, 361, 45)
    temp = []
    for deg in degs:
        speed = [wind_speed[i] for i in range(len(wind1)) if wind1[i] == deg or wind2[i] == deg]
        temp.append(sum(speed) / len(speed) if speed else 0)

    N = len(degs)
    theta = np.arange(np.pi / 8, 2 * np.pi + np.pi / 8, 2 * np.pi / N)
    radii = np.array(temp)
    plt.axes(polar=True)
    colors = [(1 - x / max(temp), 1 - x / max(temp), 0.6) for x in radii]
    plt.bar(theta, radii, width=(2 * np.pi / N), bottom=0.0, color=colors)
    plt.title('未来14天风级图', x=0.2, fontsize=20)
    plt.show()


def weather_pie(data):
    '''绘制天气饼图'''
    weather = list(data['天气'])
    dic_wea = {weather_type: weather.count(weather_type) for weather_type in set(weather)}

    explode = [0.01] * len(dic_wea)
    color = ['lightskyblue', 'silver', 'yellow', 'salmon', 'grey', 'lime', 'gold', 'red', 'green', 'pink']
    plt.pie(dic_wea.values(), explode=explode, labels=dic_wea.keys(), autopct='%1.1f%%', colors=color)
    plt.title('未来14天气候分布饼图')
    plt.show()


def main():
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    data14 = pd.read_csv('weather14.csv', encoding='gb2312')
    print(data14)
    tem_curve(data14)
    wind_radar(data14)
    weather_pie(data14)


if __name__ == '__main__':
    main()
