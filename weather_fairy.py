import discord
import json
import time
import datetime
import scrapy
import requests
from bs4 import BeautifulSoup

client = discord.Client()

token = "Nzc2NzAwMTY5Mzg3MTE0NTE2.X64sZg.wyT_0kkUBLJCy65fI0vew4CLvXA"


def getWeather(place):
    if place == '명령어':
        return "입력 내용: !+(지역명)\n예시) !대전"
    if place == '날씨의 요정':
        return '날씨의 요정은 날씨 데이터를 기반으로 옷차림, 마스크, 선크림, 활동, 우산이 필요한지 아닌지의 정보를 알려주는 모바일 및 웹 디스코드에서 실행되는 애플리케이션입니다.\n 채팅창에 !명령어을 입력하여 어떻게 사용하면 되는지 확인해 보세요!'
    req = requests.get("https://search.naver.com/search.naver?query=" + place +"날씨")
    # query 위치에 = 지역+날씨 형태
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    # BeautifulSoup으로 html 소스 python 객체로 변환
    data1 = soup.find('div', {'class':'weather_box'})
    if data1 is None:
        return '😅찾을 수 없는 지역입니다'
    find_mintemp = data1.find('span',{'class': 'min'}).text
    find_maxtemp = data1.find('span',{'class': 'max'}).text
    
    # 미세먼지
    data2 = data1.findAll('dd')
    find_pm = data2[0].find('span', {'class':'num'}).text
    find_ultra_pm = data2[1].find('span', {'class':'num'}).text
    find_ultra_violet = data1.find('span', {'class': 'indicator'}).find('span', {'class': 'num'}).text    
    find_cast = data1.find('p', {'class': 'cast_txt'}).text
    information = '👕옷차림\n'
    information += get_clothes(find_mintemp, find_maxtemp)
    information += ('\n\n😷마스크\n' + get_mask(find_pm, find_ultra_pm))
    information += ('\n\n🌞선크림\n' + get_sunblock(find_ultra_violet))
    information += ('\n\n🏃‍♀️오늘의 추천 활동!\n' + get_activity(find_cast))
    if '비' in find_cast:
        information += '\n\n☔우산 챙기는거 잊지 마세요!'

    return information

def return_clothes_index(index):
    if index <= 4:
        return 0
    elif index <= 8:
        return 1
    elif index <= 11:
        return 2
    elif index <= 16:
        return 3
    elif index <= 19:
        return 4
    elif index <= 22:
        return 5
    elif index <= 27:
        return 6
    else:
        return 7
        
def get_clothes(mintemp, maxtemp):
    min_index = return_clothes_index(int(mintemp[:-1]))
    max_index = return_clothes_index(int(maxtemp[:-1]))

    return_clothes = ''
    for i in range(min_index, max_index + 1):
        f = open('./clothes/' + str(i) + '.txt', 'rb')
        return_clothes += (f.readline().decode('utf-8') + ' ')
        f.close()

    return return_clothes

def get_mask(pm, ultra_pm):
    pm = int(pm[:-3])
    ultra_pm = int(ultra_pm[:-3])   
    return_mask = ''
    if 81 < pm or 36<= ultra_pm:
        return_mask = 'KF94 이상'
    elif 31 < pm or 16<= ultra_pm:
        return_mask = 'KF84 이상'
    else:
        return_mask = '오늘은 미세먼지 지수가 좋아요!\n 그래도 코로나 예방을 위해 쓰는 건 어떨까요?'
    return return_mask

def get_sunblock(ultra_violet):
    ultra_violet = int(ultra_violet)
    return_sunblock =''
    if 6 <= ultra_violet:
        return_sunblock = 'SPF: 50 이상\n PA: +++'
    elif 3 <= ultra_violet:
        return_sunblock = 'SPF: 30 이상\n PA: ++'
    else:
        return_sunblock ='SPF: 10 내외\n PA: +'
    return return_sunblock
    # ultra_violet = int(ultra_violet)
    # if 6 <= ultra_violet:
    #     return 'SPF: 50 이상\n PA: +++'
    # elif 3 <= ultra_violet:
    #     return 'SPF: 30 이상\n PA: ++'
    # else:
    #     return 'SPF: 10 내외\n PA: +'
    
def get_activity(cast):
    return_activity = ''
    if '맑음' in cast:
        return_activity += '오늘은 날씨가 맑아요!\n'
        f = open('./activity/맑음.txt', 'rb')
        return_activity += (f.readline().decode('utf-8') + ' 어떠세요?\n')
        f.close()
    elif '흐림' in cast:
        return_activity += '오늘은 날씨가 흐려요!\n'
        f = open('./activity/흐림.txt', 'rb')
        return_activity += (f.readline().decode('utf-8') + ' 어떠세요?\n')
        f.close()
    return return_activity

@client.event
async def on_ready():
    # print(client.user.id)
    print("ready")
    game = discord.Game("날씨 메시지")
    await client.change_presence(status=discord.Status.online, activity=game)

@client.event
async def on_message(message):
    if message.content.startswith("!"):
        await message.channel.send(getWeather(message.content[1:]))
    # if message.content.startswith("!"):
    #     if message.content.startswith("!명령어"):
    #         await message.channel.send("!+(지역명)\n예시) !대전")
    #     else:
    #         await message.channel.send(getWeather(message.content[1:]))
    # if message.content.startswith("!명령어"):
    #     await message.channel.send("!+(지역명)\n예시) !대전")
    # elif message.content.startswith("!"):
    #     await message.channel.send(getWeather(message.content[1:]))


client.run(token)
