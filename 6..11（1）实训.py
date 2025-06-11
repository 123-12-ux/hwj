import requests
from lxml import etree
import csv

def getWeather(url):
    weather_info = []
    headers = {
        'Cookie': 'UserId=17496278166884697; Hm_lvt_5326a74bb3e3143580750a123a85e7a1=1749627817; HMACCOUNT=760D599622098B6F; Hm_lvt_7c50c7060f1f743bccf8c150a646e90a=1749627817; Hm_lpvt_5326a74bb3e3143580750a123a85e7a1=1749627966; Hm_lpvt_7c50c7060f1f743bccf8c150a646e90a=1749627966',
        'referer': 'https://lishi.tianqi.com/shanghai/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0 Safari/537.36'
    }

    try:
        # 发起请求,接受响应数据
        response = requests.get(url=url, headers=headers)
        response.raise_for_status()  # 检查请求是否成功

        # 数据预处理
        resp_html = etree.HTML(response.text)

        # 修正xpath表达式
        resp_list = resp_html.xpath("//ul[@class='thrui']/li")

        if not resp_list:
            print(f"警告: 在 {url} 中未找到天气数据")
            return weather_info

        for li in resp_list:
            day_weather_info = {}

            # 日期
            date_text = li.xpath("./div[1]/text()")
            day_weather_info['date_time'] = date_text[0].split(' ')[0] if date_text else ""

            # 最高气温（处理摄氏度符号）
            high_text = li.xpath("./div[2]/text()")
            high = high_text[0] if high_text else ""
            day_weather_info['high'] = high.replace("℃", "").strip()

            # 最低气温
            low_text = li.xpath("./div[3]/text()")
            low = low_text[0] if low_text else ""
            day_weather_info['low'] = low.replace("℃", "").strip()

            # 天气
            weather_text = li.xpath("./div[4]/text()")
            day_weather_info['weather'] = weather_text[0] if weather_text else ""

            weather_info.append(day_weather_info)

    except Exception as e:
        print(f"获取{url}数据时出错: {e}")
        return []

    return weather_info


if __name__ == "__main__":
    weathers = []

    for month in range(1, 13):
        # 格式化月份为两位数字
        month_str = f"0{month}" if month < 10 else str(month)
        weather_time = f'2016{month_str}'

        print(f"正在获取{weather_time}的天气数据...")
        url = f'https://lishi.tianqi.com/shanghai/{weather_time}.html'
        weather = getWeather(url)

        # 存储数据
        weathers.extend(weather)  # 使用extend而不是append，避免嵌套列表

        # 打印进度
        print(f"{weather_time}获取完成，共{len(weather)}条记录")

    # 数据写入CSV
    try:
        with open('weather.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.writer(csvfile)
            # 写入列名
            writer.writerow(['日期', '最高气温', '最低气温', '天气'])

            # 写入数据
            for day_data in weathers:
                writer.writerow([
                    day_data['date_time'],
                    day_data['high'],
                    day_data['low'],
                    day_data['weather']
                ])

        print(f"数据已成功写入 weather.csv, 共{len(weathers)}条记录")

    except Exception as e:
        print(f"写入CSV文件时出错: {e}")