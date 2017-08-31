import config
import requests
import json
import crypto
import random


# 获取随机的移动端UserAgent
def make_random_useragent():
    return random.choice(config.CONFIG_USERAGENT_PHONE)


# 根据公交车线路来获得公交车详情
def find_bus_line_detail(linename):
    url = config.WEB_PATH + config.BUS_LINE_DETAIL
    # # 不使用代理
    # proxies = {
    #     # 'http': 'http://127.0.0.1:8888',
    #     # 'https': 'https://127.0.0.1:8888',
    #     'http': '',
    #     'https': '',
    # }

    params = crypto.encode(json.dumps({'linename': linename}, ensure_ascii=False, separators=(',', ':')))
    response = requests.get(url,
                            headers={"User-Agent": make_random_useragent()},
                            params={'params': params})

    # proxies=proxies)

    result = response.json()
    return render(result)


def render(result):
    if result['status'] == 'n':
        return '查询错误'

    stations_list = {}
    buses_list = {}

    for data in result['data']['list']:
        # start_time = data['SBCSJ']   # 早班车
        # finish_time = data['MBCSJ']  # 末班车

        start_station = data['SSTATION_NAME_ID']    # 起点
        finish_station = data['FSTATION_NAME_ID']   # 终点
        direction = start_station + '->' + finish_station   # 方向

        stations_list[direction] = \
            [station['STATIONNAME'] for station in data['stationlist']]    # 获得所有的站点名
        buses_list[direction] = {}

        # 行进中公交列表
        for bus in data['buslist']:
            hphm = bus['hphm']   # 车牌号
            station_name = bus['stationname']  # 所在站点
            if station_name in buses_list[direction]:
                buses_list[direction][station_name].append(hphm)
            else:
                buses_list[direction][station_name] = [hphm]

    view_list = []

    for direction, stations in stations_list.items():
        view = '方向:%s\n' % direction
        seq = 0
        last_station = None
        for station in stations:
            if last_station is not None:
                if station in buses_list[direction]:
                    view += last_station + str(buses_list[direction][station])
                else:
                    view += last_station + ' '
            seq += 1
            last_station = station
        view += last_station

        view_list.append(view)

    return '%s\n%s' % (view_list[0], view_list[1])


if __name__ == '__main__':
    res = find_bus_line_detail('1路')
    print(res)


