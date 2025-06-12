import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def wind_radar(data):
    wind = list(data['风力方向'])
    wind_speed = list(data['风级'])
    for i in range(len(wind)):  # 用 len(wind) 来避免硬编码
        if wind[i] == '北风':
            wind[i] = 90
        elif wind[i] == '南风':
            wind[i] = 270
        elif wind[i] == '西风':
            wind[i] = 180
        elif wind[i] == '东风':
            wind[i] = 360
        elif wind[i] == '东北风':
            wind[i] = 45
        elif wind[i] == '西北风':
            wind[i] = 135
        elif wind[i] == '西南风':
            wind[i] = 225
        elif wind[i] == '东南风':
            wind[i] = 315

    degs = np.arange(45, 361, 45)
    temp = []
    for deg in degs:
        speed = []
        for i in range(len(wind)):
            if wind[i] == deg:
                speed.append(wind_speed[i])
        if len(speed) == 0:
            temp.append(0)
        else:
            temp.append(sum(speed) / len(speed))

    print(temp)

    N = 8
    theta = np.arange(0. + np.pi / 8, 2 * np.pi + np.pi / 8, 2 * np.pi / 8)
    radii = np.array(temp)

    plt.axes(polar=True)
    colors = [(1 - x / max(temp), 1 - x / max(temp), 0.6) for x in radii]
    plt.bar(theta, radii, width=(2 * np.pi / N), bottom=0.0, color=colors)

    plt.title('一天风级图', x=0.2, fontdict={'size': 20})  # 修正字体字典
    plt.show()


def calc_corr(a, b):
    a_avg = sum(a) / len(a)
    b_avg = sum(b) / len(b)
    cov_ab = sum([(x - a_avg) * (y - b_avg) for x, y in zip(a, b)])
    sq = math.sqrt(sum([(x - a_avg) ** 2 for x in a]) * sum([(x - b_avg) ** 2 for x in b]))
    corr_factor = cov_ab / sq
    return corr_factor


def corr_tem_hum(data):
    tem = data['温度']
    hum = data['相对湿度']
    plt.scatter(tem, hum, color='blue')
    plt.title('温湿度相关性分析图')
    plt.xlabel('温度/℃')
    plt.ylabel('相对湿度/%')
    plt.text(20, 40, '相关系数为:' + str(calc_corr(tem, hum)), fontdict={'size': 10, 'color': 'red'})
    plt.show()
    print('相关系数为:' + str(calc_corr(tem, hum)))


def main():
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    data1 = pd.read_csv('weather1.csv', encoding='gb2312')
    print(data1)
    # tem_curve(data1)
    # hum_curve(data1)
    # air_curve(data1)
    wind_radar(data1)
    corr_tem_hum(data1)


if __name__ == '__main__':
    main()
