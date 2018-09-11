import discord
import asyncio
import crawl
import json
import timer

client = discord.Client()
channel_for_weather = discord.Object(id = '483473891365224468')
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(game = discord.Game(name = '왑봇 테스트중..'))

@client.event
async def on_message(message):
    if message.content.startswith('!날씨'):
        weather, date, time = crawl.get_weather_now()
        message_for_send = date + ' ' + time + '기준 현재 날씨입니다. \n'
        for i in weather.keys():
            message_for_send += (i + ' : ' + str(weather[i]) + '\n')

        await client.send_message(message.channel, message_for_send)


async def send_weather_forecast():
    while 1:
        weather_forecast = crawl.get_weather_forecast()
        await client.wait_until_ready()
        for i in weather_forecast:
            await client.send_message(channel_for_weather, json.dumps(i, ensure_ascii= False))

        seconds = timer.find_seconds_for_waiting()
        await client.send_message(channel_for_weather, f'{seconds}만큼 기다립니다')
        await asyncio.sleep(seconds)

client.loop.create_task(send_weather_forecast())
client.run('NDQ1NTg3NjU4OTcwODkwMjQx.Dl6iWQ.5ieRq0KZuwYyRd-Q7KTCn9yJS0k')
