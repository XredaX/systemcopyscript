from telethon import TelegramClient, events
from telethon.sessions import StringSession
import re
from configs import Config
from database import user
import os
from ticker_rules import rules


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
            with open('database.txt') as f:
                    contents = f.read()
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
            if coin == contents:
                f.close()
                pass
            else:
                datachannel = user.findsession(collection = "channels", Owenr=str(admin))
                targets = []
                share = ''
                for d in datachannel[0]:
                    targets.append(str(d["target"]))
                chat_id = event.chat_id
                if str(chat_id) in targets:
                    msg = re.sub(r'^https?:\/\/t.me\/.*[\r\n]*', '', msg, flags=re.MULTILINE)
                    datachannel = user.findsession(collection = "channels", Owenr=str(admin))
                    for i in datachannel[0]:
                        target = str(i["target"])
                        if str(target) == str(chat_id):
                            share = i["share"]
                            datawords = user.findwords(collection = "words", Owenr=str(admin), target=str(chat_id))
                            for d in datawords[0]:
                                sh = d["objetT"]
                                if re.search(sh, msg):
                                    msg = msg.replace(sh, "")

                            try:
                                await client.send_file(int(share), image, caption=msg)
                            except:
                                await client.send_message(int(share), msg)
                            with open('database.txt', 'w') as f1:
                                new_text = contents.replace(contents, coin)
                                f1.write(new_text)
                                f1.close()
                                f.close()
                            break   

        else:
            os.system("python copymsg.py")
     except:
         pass

client.start()
client.run_until_disconnected()
