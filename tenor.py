import random
import queue
import json
import requests
import discord
from discord.ext import commands, tasks
from pd import pd


trashbin = '💵'
abc = 'abcdefghijklmnopqrstuvwxyz'
eabc0 = '🅰 🅱 x x x x x x x x x x x x 🅾 x x x x x x x x x x x'.replace(' ', '')
eabc1 = '🇦 🇧 🇨 🇩 🇪 🇫 🇬 🇭 🇮 🇯 🇰 🇱 🇲 🇳 🇴 🇵 🇶 🇷 🇸 🇹 🇺 🇻 🇼 🇽 🇾 🇿'.replace(' ', '')
eabc2 = '🅐 🅑 🅒 🅓 🅔 🅕 🅖 🅗 🅘 🅙 🅚 🅛 🅜 🅝 🅞 🅟 🅠 🅡 🅢 🅣 🅤 🅥 🅦 🅧 🅨 🅩'.replace(' ', '')
emodic = {x[0]: x[1:] for x in zip(abc, eabc0, eabc1)}
slicenames = ['ab', 'cl', 'sos', 'ng', 'ok', 'up', 'cool', 'new', 'free', 'vs', 'x', '!!', '!?', 'm', 'id', 'p', 'wc', 'atm', 'abc', 'll', 'tm', 'c', 'r', 'end', 'back', 'on', 'top', 'soon', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', '!', '!', '?', '?', 'v', 'x', 'zzz', 'x', ]
slices = list(zip(
    slicenames, 
    ['🆎', '🆑', '🆘', '🆖', '🆗', '🆙', '🆒', '🆕', '🆓', '🆚', '❌', '‼️', '⁉️', '〽️', '🆔', '🅿️', '🚾', '🏧', '🔤', '⏸️', '™️', '©️', '®️', '🔚', '🔙', '🔛', '🔝', '🔜', '🔘', '⚪', '⚫', '🔴', '🔵', '🟤', '🟣', '🟢', '🟡', '🟠', '☮️', '⭕', '🔅', '🔆', '⏺️', '❗', '❕', '❓', '❔', '✅', '❎', '💤', '✖️', ]
))
#'0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟', '#️⃣', '*️⃣', 
async def setup(bot):
    l = tenor_cog(bot)
    await bot.add_cog(l)
    l.delete_msgs.start()
    print(''.join(slicenames))
    print(slices)

class tenor_cog(commands.Cog):
    def __init__(self, bot):
        print('tenor module loaded')
        self.q = queue.Queue()
        self.pd = pd('tenor.json')
        if 'score' not in self.pd:
            self.pd['score'] = {}
        self.bot = bot
        @bot.event
        async def on_raw_reaction_add(payload):
            tu = trashbin
            channel = await bot.fetch_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            om = await channel.fetch_message(message.reference.message_id)
            uid = payload.user_id
            user = await bot.fetch_user(uid)
            if user.bot:
                return
            omuid = om.author.id
            if uid != omuid:
                await channel.send(f'nah <@{uid}>, cant do it for <@{omuid}>')
                return
            if user.bot:
                return
            emoji = payload.emoji
            if emoji.name == tu:
                try:
                    msg = await channel.send(self.bot.cogs['Banking']._change(uid, -1))
                    await message.delete()
                    self.q.put(msg)
                except Exception as e:
                    await channel.send(str(e))

    @commands.Cog.listener()
    async def on_message(self, message):
        a = message.author
        if a.bot:
            return
        c = message.channel
        txt = message.content
        if txt[0] in ['.', ':']:
            return
        if message.guild.id not in [ 871762312208474133, 1029050954173132943]:
            return
        words = txt.split()
        if txt.startswith(str(self.bot.user.mention) + ' frp'):
            if c.id != 1085160288178941973:
                return
            alarm = 'alarm'
            with open('tenor', 'r') as f:
                key = f.read().replace('\n', '')
            n = 10
            query = f"https://g.tenor.com/v2/search?q={alarm}&key={key}&limit={n}"
            response = requests.get(query)
            data = response.json()
            url = random.choice(data['results'])
            await c.send(f'<@{451839413836840980}>\n' + url['url'])
        elif len(words) == 1:
            if len(message.mentions) == 0 and not message.reference:
                if not txt[1].isalnum():
                    return
                if txt.startswith('http'):
                    return
                sid = str(a.id)
                if sid not in self.pd['score']:
                    self.pd['score'][sid] = 0
                self.pd['score'][sid] += 1
                self.pd.sync()
                alarm = words[0]
                with open('tenor', 'r') as f:
                    key = f.read().replace('\n', '')
                n = 10
                query = f"https://g.tenor.com/v2/search?q={alarm}&key={key}&limit={n}"
                response = requests.get(query)
                data = response.json()
                url = random.choice(data['results'])
                txt = f'4o bot is on crusade to let people become better and enrich their speech ... by punishing one word messages\nyour score: {self.pd["score"][sid]}\n' + f'tap {trashbin} to pay 1 mil and remove this message\n' + url['url']
                msg = await message.reply(txt)
                await msg.add_reaction(trashbin)
            else:
                if message.reference:
                    ref_message = await c.fetch_message(message.reference.message_id)
                    l = get_emoji(txt.lower())
                    if l:
                        for i in l:
                            await ref_message.add_reaction(i)
                        await message.delete()
        else:
            for i in words:
                try:
                    if i[0] == '#':
                        alarm = i[1:]
                        with open('tenor', 'r') as f:
                            key = f.read().replace('\n', '')
                        n = 10
                        query = f"https://g.tenor.com/v2/search?q={alarm}&key={key}&limit={n}"
                        response = requests.get(query)
                        data = response.json()
                        url = random.choice(data['results'])
                        await c.send(url['url'])
                except:
                    pass

    @tasks.loop(seconds = 5)
    async def delete_msgs(self):
        try:
            await self.msg_to_delete.delete()
            self.msg_to_delete = None
        except Exception as e:
            pass
        try:
            msg = self.q.get(block = False)
            self.msg_to_delete = msg
        except:
            pass


def get_emoji(txt, carry = ''):
    if not txt:
        return carry
    for i in slices:
        if i[1][0] not in carry:
            if txt.startswith(i[0]):
                return get_emoji(txt[len(i[0]):], carry + i[1][0])
    for j in emodic[txt[0]]:
        if j == 'x':
            continue
        if j not in carry:
            return get_emoji(txt[1:], carry + j)
    return []
