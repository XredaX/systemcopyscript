from telethon import TelegramClient, events
from telethon.sessions import StringSession
import re
from configs import Config
from database import user
import os
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
            msg = event.raw_text
            image = event.message.media
            share = ""
            chat_id = event.chat_id
            datachannel = user.specifiChannel(collection = "channels", Owenr=str(admin), target=str(chat_id))
            if datachannel[1] > 0:
                msg = re.sub(r'^https?:\/\/t.me\/.*[\r\n]*', '', msg, flags=re.MULTILINE)
                channelsS = []
                for i in datachannel[0]:
                    channelsS.append(i["share"])
                    datawords = user.findwords(collection = "words", Owenr=str(admin), target=str(chat_id))
                    if datawords[1]>0:
                        for d in datawords[0]:
                            sh = d["objetT"]
                            if re.search(sh, msg):
                                msg = msg.replace(sh, "")
                    share = i["share"]
                    img = user.findwords(collection = "img", Owenr=str(admin), target=str(chat_id))
                    datapost = user.findpost(collection = "posts", Owenr=str(admin), target=str(chat_id), share=str(share))
                    if datapost[1]>0:
                        if datapost[0][0]['post'] != msg:
                            if img[1] == 0 :
                                try:
                                    await client.send_file(int(share), image, caption=msg)
                                except:
                                    await client.send_message(int(share), msg)
                            else:
                                await client.send_message(int(share), msg)
                            try:
                                if str(chat_id) == '-1001591094057':
                                   bot.send_message(-1001500845444, msg)
                                   
                                if str(chat_id) == '-1001605585529':
                                   bot.send_message(-1001749137545, msg)
                                   
                                if str(chat_id) == '-1001491411385':
                                   bot.send_message(-1001685452565, msg)
                                   
                                if str(chat_id) == '-10015910940571':
                                   bot.send_message(-1001644952320, msg)
                                   
                                msg = str(chat_id) + '\n\n' + msg
                                bot.send_message(-1001617820230, msg)
                            except:
                                pass
                            user.editpost(collection = "posts", Owenr=str(admin), target=str(chat_id), post=str(msg), share=str(share))
                    else:
                        if img[1] == 0 :
                            try:
                                await client.send_file(int(share), image, caption=msg)
                            except:
                                await client.send_message(int(share), msg)
                        else:
                            await client.send_message(int(share), msg)
                        try:
                            if str(chat_id) == '-1001591094057':
                                   bot.send_message(-1001500845444, msg)
                                   
                            if str(chat_id) == '-1001605585529':
                              bot.send_message(-1001749137545, msg)
                              
                            if str(chat_id) == '-1001491411385':
                              bot.send_message(-1001685452565, msg)
                              
                            if str(chat_id) == '-10015910940571':
                              bot.send_message(-1001644952320, msg)
                            msg = str(chat_id) + '\n\n' + msg
                            bot.send_message(-1001617820230, msg)
                        except:
                            pass
                        user.addpost(collection = "posts", Owenr=str(admin), share=str(share), post=str(msg), target=str(chat_id))
        else:
            os.system("python copymsg.py")
     except:
         pass

client.start()
client.run_until_disconnected()
