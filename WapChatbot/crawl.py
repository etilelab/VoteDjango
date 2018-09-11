import requests as r
import json
from datetime import *
from pprint import pprint

#현 시각 날씨 정보 코드
decoding_codes = {'T1H' : '기온',
                  'RN1' : '1시간 강수량',
                  'REH' : '습도',
                  'VEC' : '풍향',
                  'WSD' : '풍속'}


#현 날씨정보, 2중 구조를 가지는 코드들
decoding_codes_2layer = {'SKY' : ['구름', { '1' : '맑음',
                                           '2' : '구름조금',
                                           '3' : '구름많음',
                                           '4' : '흐림'}],
                         'PTY' : ['강수', { '0' : '비 안내림',
                                           '1' : '비',
                                           '2' : '비/눈',
                                           '3' : '눈'}],
                         'LGT' : ['낙뢰', { '0' : '낙뢰 없음',
                                           '1' : '낙뢰 있음'}]}
#일기예보 날씨정보 코드
decoding_codes_for_forecast = {'tmFc' : '발표시간',
                               'wd1' : '풍향',
                               'wf' : '날씨',
                               'ta' : '예상기온',
                               'mSt' : '강수 확률'}

decoding_codes_for_forecast_2layer = {'numEf' : ['예보 시간' , {0 : '오늘 오전',
                                                              1 : '오늘 오후'}],
                                      'wsIt' : ['풍속' , {1 : '약간 강',
                                                        2 : '강',
                                                        3 : '매우 강'}],
                                      'wfCd' : ['하늘', {'DB01' : '맑음',
                                                        'BD02' : '구름 조금',
                                                        'DB03' : '구름 많음',
                                                        'DB04' : '흐림'}],
                                      'mYn' : ['강수 형태', {0 : '강수없음',
                                                           1 : '비',
                                                           2 : '비/눈',
                                                           3 : '눈'}]}


def extract_from_json(response):
    weather_dict = json.loads(response)
    return weather_dict['response']['body']['items']['item']

def make_time_for_use():
    time_now = datetime.now()
    date_for_use = (time_now - timedelta(days = 1)).strftime("%Y%m%d") if time_now.strftime("%H") == '00' and int(time_now.strftime("%M")) < 40 else date.today().strftime("%Y%m%d")

    if int(time_now.strftime("%H")) == 0 and int(time_now.strftime("%M")) < 40:
        basetime = '2300'
    elif int(time_now.strftime("%M")) >= 40:
        basetime = time_now.strftime("%H00")
    else:
        basetime = (time_now - timedelta(hours = 1)).strftime("%H") + '00'

    return date_for_use, basetime


def get_weather_forecast():
    raw = r.get(f"http://newsky2.kma.go.kr/service/VilageFrcstDspthDocInfoService/WidOverlandForecast?ServiceKey=8dWQmx%2BNiHDmMCfGwZXFIVYPWv807wuz5H%2FE9GLP42G3Al662%2B1vgdjKnM3vPBO65garXv%2BCyBTu5oGKgCmZwg%3D%3D&regId=11H20201&_type=json")
    weather_info_raw = extract_from_json(raw.content)
    weather_info = []
    for i in weather_info_raw:
        try:
            weather_dict = {}
            for j in i.keys():
                if j in decoding_codes_for_forecast.keys():
                    weather_dict[decoding_codes_for_forecast[j]] = i[j]
                elif j in decoding_codes_for_forecast_2layer.keys():
                    weather_dict[decoding_codes_for_forecast_2layer[j][0]] = decoding_codes_for_forecast_2layer[j][1][i[j]]
            weather_info.append(weather_dict)
        except:
            continue

    return weather_info


def get_weather_now():
    weather_info = {}
    date_for_use, basetime = make_time_for_use()

    raw = r.get(f"http://newsky2.kma.go.kr/service/SecndSrtpdFrcstInfoService2/ForecastGrib?ServiceKey=8dWQmx%2BNiHDmMCfGwZXFIVYPWv807wuz5H%2FE9GLP42G3Al662%2B1vgdjKnM3vPBO65garXv%2BCyBTu5oGKgCmZwg%3D%3D&base_date={date_for_use}&base_time={basetime}&nx=98&ny=75&pageNo=1&numOfRows=10&_type=json")
    weather_info_raw = extract_from_json(raw.content)

    for info in weather_info_raw:
        if info['category'] in decoding_codes.keys():
            weather_info[decoding_codes[info['category']]] = info['obsrValue']

        elif info['category'] in decoding_codes_2layer.keys():
            weather_info[decoding_codes_2layer[info['category']][0]] = decoding_codes_2layer[info['category']][1][str(info['obsrValue'])]

    return weather_info, date_for_use, basetime
