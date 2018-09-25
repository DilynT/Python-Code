import discord
import random
import os
import requests
import json
import random

import settings
settings.init()

client = discord.Client()

@client.event
async def on_message(message):
    #declaring needed shortcuts and variables
    if message.author.bot:
        return

    command = message.content.startswith
    author = '<@' + message.author.id + '>'
    messageText = message.content
    speaker = message.author.id
    channel = message.channel
    send = client.send_message
    ttsCheck = False

    #check if this message is a PM
    if message.server is None:
        await send(channel, 'Are you threatening me, Master Jedi?')
        return

    #check if bot was mentioned (directly or indirectly)
    localID = "<@"
    localID += str(settings.BOTID)
    localID += ">"
    #Give command to the bot
    if command('Sheev') or command(localID) or command('sheev'):
        commandText=messageText.replace('Sheev ', "")
        commandText=messageText.replace('sheev ', "")
        localID+= ' '
        commandText=commandText.replace(localID, "")
        checkCommand=commandText.startswith
        #Repeat the message typed following the command
        if checkCommand('repeat'):
            commandText=commandText.replace('repeat', "", 1)
            await send(channel, commandText, tts=False)
            await client.delete_message(message)
            return
        #Versioning the fun way
        elif checkCommand('year'):
            await send(channel, settings.VERSION, tts=False)
            return
        #Send dm help message
        elif checkCommand('assistme'):
            helpfile = open('commands.txt', 'r')
            commands = helpfile.read()
            helpfile.close()
            await send(message.author, commands)
            await client.delete_message(message)
            return
        #Will shut down bot if owner of bot types command
        elif checkCommand('leaveus'):
            if(int(speaker)==int(settings.OWNER)):
                await send(channel, ('https://i.gyazo.com/b997977c902a2ab90ba9f09edfc2f72b.gif'), tts=False)
                exit()
            else:
                await send(channel, (author + 'https://i.gyazo.com/78756a27389e38fa08482b1968656758.gif'), tts=False)
                return
        #Post images/gifs from folder contained within directory
        elif checkCommand('shitpost'):
            filefrom = os.listdir("./Memes")
            imagest = random.choice(filefrom)
            filepath = "./Memes/" + imagest
            await client.send_file(message.channel, filepath)
            await client.delete_message(message)
        #Weather Report
        elif checkCommand('forecast'): # MultiDay Future Scan/Prediction
            city, state = commandText.replace('forecast ', "", 1).split(' ')
            url = 'http://api.wunderground.com/api/%s/forecast/q/%s/%s.json' % (settings.WUW_API_KEY, state, city)
            pullfrom = requests.get(url)
            data = json.loads(pullfrom.text)
            time1 = data['forecast']['txt_forecast']['forecastday'][1]['title']
            time2 = data['forecast']['txt_forecast']['forecastday'][2]['title']
            time3 = data['forecast']['txt_forecast']['forecastday'][3]['title']
            time4 = data['forecast']['txt_forecast']['forecastday'][4]['title']
            time5 = data['forecast']['txt_forecast']['forecastday'][5]['title']
            condition1 = data['forecast']['txt_forecast']['forecastday'][1]['fcttext']
            condition2 = data['forecast']['txt_forecast']['forecastday'][2]['fcttext']
            condition3 = data['forecast']['txt_forecast']['forecastday'][3]['fcttext']
            condition4 = data['forecast']['txt_forecast']['forecastday'][4]['fcttext']
            condition5 = data['forecast']['txt_forecast']['forecastday'][5]['fcttext']
            report = '```Future forecast for %s, %s:\n*%s: %s\n*%s: %s\n*%s: %s\n*%s: %s\n*%s: %s```' % (city, state, time1, condition1, time2, condition2, time3, condition3, time4, condition4, time5, condition5)
            #await send(channel, '```Keep in mind, that this information may be up to two hours behind. (That requires spending money on an API key for a discord bot)```')
            await send(channel, report)
        elif checkCommand('weather'):
            city, state = commandText.replace('weather ', "", 1).split(' ')
            url = 'http://api.wunderground.com/api/%s/conditions/q/%s/%s.json' % (settings.WUW_API_KEY, state, city)
            pullfrom = requests.get(url)
            data = json.loads(pullfrom.text)
            location = data['current_observation']['display_location']['full']
            temperature = data['current_observation']['temperature_string']
            humidity = data['current_observation']['relative_humidity']
            condition = data['current_observation']['weather']
            wind = data['current_observation']['wind_string']
            recordtime = data['current_observation']['observation_time']
            feelslike = data['current_observation']['feelslike_string']
            dewpoint = data['current_observation']['dewpoint_string']
            visibility = data['current_observation']['visibility_mi']
            report = '```%s:\nToday In %s Conditions are %s\nTemperature is: %s, Feels Like: %s\nHumidity is: %s, With  A Dewpoint of: %s\nWind: %s\nVisibility at: %smi```' % (recordtime, location, condition, temperature, feelslike, humidity, dewpoint, wind, visibility)
            #await send(channel, '```Keep in mind, that this information may be up to two hours behind. (That requires spending money on an API key for a discord bot)```')
            await send(channel, report)
        elif checkCommand('prequel'):
            postnum = random.randint(1,80)
            url = 'https://www.reddit.com/r/prequelmemes/hot.json?limit=80'
            pullfrom = requests.get(url)
            data = json.loads(pullfrom.text)
            title = data['data']['children'][postnum]['data']['title']
            user = data['data']['children'][postnum]['data']['author']
            post = data['data']['children'][postnum]['data']['url']
            finalpost = '`%s`\n%s\n`By: %s`' % (title, post, user)
            await send(channel, finalpost)
        else:
            print(commandText)
            await send(channel, '**Artistic Screeching**')

    else: 
        return


client.run(settings.TOKEN)