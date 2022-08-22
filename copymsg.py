from telethon import TelegramClient, events
from telethon.sessions import StringSession
import re
from configs import Config
from database import user
import os
from ticker_rules import rules
from telegram import *

token = "5751463403:AAGnnZNt2wyBYu2Rc26ENaj2wt52rcaj8ns"
bot = Bot(token=token)

print("start")
admin = Config.ADMIN_ID
api_id = '14607067'
api_hash = '70733cc9c675ed296a399e0a82a9b8d9'
datasession = user.findsession(collection = "sessions", Owenr=str(admin))
string = datasession[0][0]['Session']
client = TelegramClient(StringSession(string), api_id, api_hash)


@client.on(events.NewMessage)
async def handlmsg(event):
     try:
        datasession = user.findsession(collection = "sessions", Owenr=str(admin))
        string1 = datasession[0][0]['Session']

        if str(string1) == str(string):
            coin = ""
            msg = event.raw_text
            image = event.message.media
            share = ""
            chat_id = event.chat_id
            res = msg.split()
            for r in res:
                cleanString = re.sub('\W+','', r).upper()
                if re.search("USDT", cleanString):
                    for t in rules:
                        if cleanString == t:
                            coin = cleanString
                    break
                else:
                    cleanString = cleanString+"USDT"
                    for t in rules:
                        if cleanString == t:
                            coin = cleanString
            msg = re.sub(r'^https?:\/\/t.me\/.*[\r\n]*', '', msg, flags=re.MULTILINE)
            datawords = user.findwords(collection = "words", Owenr=str(admin), target=str(chat_id))
            if datawords[1]>0:
                for d in datawords[0]:
                    sh = d["objetT"]
                    if re.search(sh, msg):
                        msg = msg.replace(sh, "")
            targets = []
            share = ''
            datachannel = user.findsession(collection = "channels", Owenr=str(admin))
            for d in datachannel[0]:
                targets.append(str(d["target"]))
            if str(chat_id) in targets:
                datachannel = user.findsession(collection = "channels", Owenr=str(admin))
                for i in datachannel[0]:
                    target = str(i["target"])
                    if str(target) == str(chat_id):
                        share = i["share"]
                        break
            datapost = user.findpost(collection = "posts", Owenr=str(admin), share=str(chat_id))
            msg1 = ""
            try:
                for dialog in await client.get_dialogs():
                    if dialog.is_channel and dialog.id == int(target):
                        msg1 = dialog.name+"\n\n"+msg 
            except:
                pass
            if datapost[1]>0:
                if datapost[0][0]['post'] != msg:
                    try:
                        await client.send_file(int(share), image, caption=msg)
                    except:
                        await client.send_message(int(share), msg)
                    try:
                        bot.send_message(-1001617820230, msg1)
                    except:
                        pass
                    user.editpost(collection = "posts", Owenr=str(admin), share=str(chat_id), post=str(msg))
            else:
                try:
                    await client.send_file(int(share), image, caption=msg)
                except:
                    await client.send_message(int(share), msg)
                try:
                    bot.send_message(-1001617820230, msg1)
                except:
                    pass
                user.addpost(collection = "posts", Owenr=str(admin), share=str(chat_id), post=str(msg))
        else:
            os.system("python copymsg.py")
     except:
         pass

client.start()
client.run_until_disconnected()
